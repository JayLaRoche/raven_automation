"""
Reference Data Validator
Validates window/door data against PostgreSQL reference tables
Ensures accurate drawings by checking frame series, glass types, hardware, and colors
"""
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text


class ReferenceDataValidator:
    """Validate drawing data against reference tables"""
    
    def __init__(self, db: Session):
        self.db = db
        self._load_reference_data()
    
    def _load_reference_data(self):
        """Load all reference data into memory for fast validation"""
        # Frame Series
        result = self.db.execute(text("SELECT series_name, series_code FROM frame_series"))
        self.valid_frame_series = {row[0] for row in result}
        self.valid_frame_codes = {row[1] for row in result}
        
        # Configuration Types
        result = self.db.execute(text("SELECT config_name, config_code FROM configuration_types"))
        self.valid_configurations = {row[0] for row in result}
        self.valid_config_codes = {row[1] for row in result}
        
        # Glass Types
        result = self.db.execute(text("SELECT glass_name, glass_code FROM glass_types"))
        self.valid_glass_types = {row[0] for row in result}
        self.valid_glass_codes = {row[1] for row in result}
        
        # Hardware Options
        result = self.db.execute(text("SELECT hardware_name FROM hardware_options"))
        self.valid_hardware = {row[0] for row in result}
        
        # Frame Colors
        result = self.db.execute(text("SELECT color_name, color_code FROM frame_colors"))
        self.valid_colors = {row[0] for row in result}
        self.valid_color_codes = {row[1] for row in result}
    
    def validate_window(self, window_data: Dict) -> Tuple[bool, List[str]]:
        """
        Validate window data against reference tables
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate frame series
        frame_series = window_data.get('frame_series')
        if frame_series and frame_series not in self.valid_frame_series:
            suggestion = self._find_closest_match(frame_series, self.valid_frame_series)
            errors.append(f"Invalid frame series '{frame_series}'. Did you mean '{suggestion}'?")
        
        # Validate configuration
        config = window_data.get('configuration') or window_data.get('window_type')
        if config and config not in self.valid_configurations:
            suggestion = self._find_closest_match(config, self.valid_configurations)
            errors.append(f"Invalid configuration '{config}'. Did you mean '{suggestion}'?")
        
        # Validate glass type
        glass = window_data.get('glass_type')
        if glass and glass not in self.valid_glass_types:
            suggestion = self._find_closest_match(glass, self.valid_glass_types)
            errors.append(f"Invalid glass type '{glass}'. Did you mean '{suggestion}'?")
        
        # Validate hardware
        hardware = window_data.get('hardware')
        if hardware and hardware not in self.valid_hardware:
            suggestion = self._find_closest_match(hardware, self.valid_hardware)
            errors.append(f"Invalid hardware '{hardware}'. Did you mean '{suggestion}'?")
        
        # Validate frame color
        color = window_data.get('frame_color')
        if color and color not in self.valid_colors:
            suggestion = self._find_closest_match(color, self.valid_colors)
            errors.append(f"Invalid frame color '{color}'. Did you mean '{suggestion}'?")
        
        return (len(errors) == 0, errors)
    
    def validate_door(self, door_data: Dict) -> Tuple[bool, List[str]]:
        """Validate door data against reference tables"""
        # Doors use same validation as windows
        return self.validate_window(door_data)
    
    def get_default_values(self, configuration: str = None) -> Dict:
        """
        Get default/recommended values from reference data
        
        Args:
            configuration: Window/door configuration type
        
        Returns:
            Dictionary of default values
        """
        defaults = {}
        
        # Default frame series based on configuration
        if configuration:
            if 'Slider' in configuration or 'Sliding' in configuration:
                defaults['frame_series'] = 'Series 90'
            elif 'Casement' in configuration or 'Awning' in configuration:
                defaults['frame_series'] = 'Series 86'
            elif 'Fixed' in configuration:
                defaults['frame_series'] = 'Series 80'
            elif 'Door' in configuration or 'Bifold' in configuration:
                defaults['frame_series'] = 'Series 135'
            else:
                defaults['frame_series'] = 'Series 80'
        
        # Default glass type
        defaults['glass_type'] = 'Low-E Dual Pane'
        
        # Default color
        defaults['frame_color'] = 'White'
        
        # Default hardware based on configuration
        if configuration:
            if 'Slider' in configuration:
                defaults['hardware'] = 'Slider Window Lock'
            elif 'Casement' in configuration:
                defaults['hardware'] = 'Standard Casement Lock'
            elif 'Door' in configuration:
                defaults['hardware'] = 'Sliding Door Lock'
        
        return defaults
    
    def auto_correct(self, window_data: Dict) -> Dict:
        """
        Auto-correct invalid values with closest matches
        
        Args:
            window_data: Window/door data dictionary
        
        Returns:
            Corrected data dictionary
        """
        corrected = window_data.copy()
        
        # Auto-correct frame series
        if 'frame_series' in corrected and corrected['frame_series'] not in self.valid_frame_series:
            corrected['frame_series'] = self._find_closest_match(
                corrected['frame_series'], 
                self.valid_frame_series
            )
        
        # Auto-correct configuration
        config_key = 'configuration' if 'configuration' in corrected else 'window_type'
        if config_key in corrected and corrected[config_key] not in self.valid_configurations:
            corrected[config_key] = self._find_closest_match(
                corrected[config_key], 
                self.valid_configurations
            )
        
        # Auto-correct glass type
        if 'glass_type' in corrected and corrected['glass_type'] not in self.valid_glass_types:
            corrected['glass_type'] = self._find_closest_match(
                corrected['glass_type'], 
                self.valid_glass_types
            )
        
        # Auto-correct hardware
        if 'hardware' in corrected and corrected['hardware'] not in self.valid_hardware:
            corrected['hardware'] = self._find_closest_match(
                corrected['hardware'], 
                self.valid_hardware
            )
        
        # Auto-correct color
        if 'frame_color' in corrected and corrected['frame_color'] not in self.valid_colors:
            corrected['frame_color'] = self._find_closest_match(
                corrected['frame_color'], 
                self.valid_colors
            )
        
        return corrected
    
    def _find_closest_match(self, value: str, valid_set: set) -> str:
        """Find closest matching value using simple string similarity"""
        if not value or not valid_set:
            return list(valid_set)[0] if valid_set else None
        
        value_lower = value.lower()
        
        # Exact match (case-insensitive)
        for valid in valid_set:
            if valid.lower() == value_lower:
                return valid
        
        # Partial match (contains)
        for valid in valid_set:
            if value_lower in valid.lower() or valid.lower() in value_lower:
                return valid
        
        # Return first valid option as fallback
        return list(valid_set)[0]
    
    def get_reference_summary(self) -> Dict:
        """Get summary of all available reference data"""
        return {
            'frame_series': sorted(list(self.valid_frame_series)),
            'configurations': sorted(list(self.valid_configurations)),
            'glass_types': sorted(list(self.valid_glass_types)),
            'hardware': sorted(list(self.valid_hardware)),
            'colors': sorted(list(self.valid_colors))
        }
    
    def get_compatible_hardware(self, configuration: str) -> List[str]:
        """Get hardware options compatible with a configuration"""
        result = self.db.execute(text("""
            SELECT hardware_name 
            FROM hardware_options 
            WHERE :config = ANY(applicable_configs)
            ORDER BY hardware_name
        """), {'config': configuration})
        
        return [row[0] for row in result]
