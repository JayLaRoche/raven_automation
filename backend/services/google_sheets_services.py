import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class GoogleSheetsService:
    """Service for reading Raven Custom Glass project data from Google Sheets"""
    
    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")
        self.sheet_id = os.getenv("GOOGLE_SHEET_ID")
        self.sheet_name = os.getenv("GOOGLE_SHEET_NAME", "Sheet1")
        
        if not self.credentials_path or not self.sheet_id:
            raise ValueError("Missing Google Sheets configuration in .env")
        
        # Define the scope
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
        ]
        
        # Authenticate
        creds = Credentials.from_service_account_file(
            self.credentials_path,
            scopes=scopes
        )
        self.client = gspread.authorize(creds)
        self.spreadsheet = self.client.open_by_key(self.sheet_id)
    
    def get_worksheet(self, name: str = None):
        """Get a specific worksheet or the default one"""
        if name:
            return self.spreadsheet.worksheet(name)
        return self.spreadsheet.worksheet(self.sheet_name)
    
    def get_available_sheets(self) -> List[str]:
        """Get list of all available sheet names in the spreadsheet"""
        return [ws.title for ws in self.spreadsheet.worksheets()]
    
    def parse_project_data(self, po_number: str, sheet_name: str = None) -> Optional[Dict]:
        """
        Parse all data for a given PO number from the Google Sheet
        Returns structured data ready for database insertion
        """
        try:
            worksheet = self.get_worksheet(sheet_name)
            all_records = worksheet.get_all_records()
            
            project_data = {
                'po_number': po_number,
                'billing_address': None,
                'shipping_address': None,
                'windows': [],
                'doors': []
            }
            
            # Find rows matching this PO number
            matching_rows = [row for row in all_records if row.get('PO') == po_number]
            
            if not matching_rows:
                raise ValueError(f"No project found with PO number: {po_number}")
            
            # Extract metadata from first row
            first_row = matching_rows[0]
            project_data['billing_address'] = first_row.get('Billing address', '')
            project_data['shipping_address'] = first_row.get('Shipping address', '')
            
            # Parse each row
            for row in matching_rows:
                product_type = row.get('TYPE OF PRODUCT', '').strip().lower()
                
                if 'window' in product_type:
                    window_data = self._parse_window_row(row)
                    if window_data:
                        project_data['windows'].append(window_data)
                elif 'door' in product_type:
                    door_data = self._parse_door_row(row)
                    if door_data:
                        project_data['doors'].append(door_data)
            
            return project_data
            
        except Exception as e:
            print(f"Error parsing project data for {po_number}: {e}")
            raise
    
    def _parse_window_row(self, row: Dict) -> Optional[Dict]:
        """Parse a window row from the sheet"""
        try:
            return {
                'item_number': row.get('ITEM #', row.get('item', '')).strip(),
                'room': row.get('room', '').strip(),
                'width_inches': self._parse_float(row.get('Width (inches)', row.get('width', 36))),
                'height_inches': self._parse_float(row.get('Height (inches)', row.get('height', 48))),
                'window_type': row.get('TYPE OF PRODUCT', row.get('type', 'Fixed')).strip(),
                'frame_series': row.get('Frame Series', 'Series 6000').strip(),
                'swing_direction': row.get('Swing Direction', 'Out').strip(),
                'quantity': self._parse_int(row.get('quantity:', row.get('quantity', 1))),
                'frame_color': row.get('Frame color', 'White').strip(),
                'glass_type': row.get('Glass', 'Low-E').strip(),
                'grids': row.get('GRIDS', row.get('grids', '')).strip(),
                'screen': row.get('SCREEN', row.get('Screen Spec', 'None')).strip(),
                'hardware': row.get('Hardware', 'Standard').strip(),
            }
        except Exception as e:
            print(f"Error parsing window row: {e}")
            return None
    
    def _parse_door_row(self, row: Dict) -> Optional[Dict]:
        """Parse a door row from the sheet"""
        try:
            return {
                'item_number': row.get('ITEM #', row.get('item', '')).strip(),
                'room': row.get('room', '').strip(),
                'width_inches': self._parse_float(row.get('Width (inches)', row.get('width', 36))),
                'height_inches': self._parse_float(row.get('Height (inches)', row.get('height', 80))),
                'door_type': row.get('TYPE OF PRODUCT', row.get('type', 'Swing Door')).strip(),
                'panel_type': row.get('PANEL TYPE', row.get('panel_type', 'Single')).strip(),
                'frame_series': row.get('Frame Series', 'Series 6000').strip(),
                'swing_direction': row.get('Swing Direction', 'Out').strip(),
                'quantity': self._parse_int(row.get('quantity:', row.get('quantity', 1))),
                'frame_color': row.get('Frame color', 'White').strip(),
                'glass_type': row.get('Glass', 'Low-E').strip(),
                'threshold': row.get('THRESHOLD', row.get('threshold', 'Standard')).strip(),
                'sill_pan_depth': self._parse_float(row.get('Sill Pan Depth mm', 0)),
                'sill_pan_length': self._parse_float(row.get('Sill Pan Length mm', 0)),
                'hardware': row.get('Hardware', 'Standard').strip(),
            }
        except Exception as e:
            print(f"Error parsing door row: {e}")
            return None
    
    def get_all_po_numbers(self) -> List[str]:
        """Get list of all unique PO numbers in the sheet"""
        try:
            worksheet = self.get_worksheet()
            all_records = worksheet.get_all_records()
            po_numbers = list(set([row.get('PO', '').strip() for row in all_records if row.get('PO')]))
            return sorted(po_numbers)
            
        except Exception as e:
            print(f"Error fetching PO numbers: {e}")
            raise
    
    @staticmethod
    def _parse_float(value) -> Optional[float]:
        """Safely parse a float value"""
        if value is None or value == '':
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_int(value, default=1) -> int:
        """Safely parse an integer value"""
        if value is None or value == '':
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default


# Singleton instance
_sheets_service = None

def get_sheets_service() -> GoogleSheetsService:
    """Get or create the Google Sheets service singleton"""
    global _sheets_service
    if _sheets_service is None:
        _sheets_service = GoogleSheetsService()
    return _sheets_service
