"""
Frame Library Loader
Dynamically loads frame cross-sections from PostgreSQL with caching
"""

from functools import lru_cache
from PIL import Image
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class FrameLibrary:
    """
    Frame cross-section library with intelligent caching
    Loads frame images and metadata from PostgreSQL
    """
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.project_root = Path(__file__).parent.parent.parent
        logger.info("FrameLibrary initialized")
    
    @lru_cache(maxsize=128)
    def get_cross_section(
        self, 
        series: str, 
        view_type: str, 
        configuration: str = 'standard'
    ) -> Optional[Dict]:
        """
        Dynamically retrieve cross-section based on parameters
        
        Args:
            series: Frame series (e.g., '65', '80', '86', '135')
            view_type: View type ('head', 'sill', 'jamb', 'horizontal', 'vertical')
            configuration: Configuration type ('standard', 'single', 'double', etc.)
        
        Returns:
            Dictionary with image, dimensions, and anchor points, or None if not found
        """
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            query = """
                SELECT image_path, dimensions, anchor_points, line_weights, notes
                FROM frame_cross_sections
                WHERE series_name = %s 
                  AND view_type = %s 
                  AND configuration = %s
                  AND is_active = TRUE
            """
            cur.execute(query, (series, view_type, configuration))
            
            result = cur.fetchone()
            cur.close()
            
            if result:
                image_path = result['image_path']
                dimensions = result['dimensions']
                anchor_points = result['anchor_points']
                line_weights = result['line_weights']
                notes = result['notes']
                
                # Construct full path
                full_path = self.project_root / image_path
                
                # Check if image exists
                if not full_path.exists():
                    logger.warning(f"Image not found: {full_path}")
                    return {
                        'image': None,
                        'dimensions': dimensions,
                        'anchor_points': anchor_points,
                        'line_weights': line_weights,
                        'notes': notes,
                        'path': image_path,
                        'exists': False
                    }
                
                # Load image
                try:
                    img = Image.open(full_path)
                    return {
                        'image': img,
                        'dimensions': dimensions,
                        'anchor_points': anchor_points,
                        'line_weights': line_weights,
                        'notes': notes,
                        'path': image_path,
                        'exists': True
                    }
                except Exception as e:
                    logger.error(f"Failed to load image {full_path}: {e}")
                    return None
            
            logger.debug(f"No cross-section found: {series}/{view_type}/{configuration}")
            return None
            
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def get_all_views_for_series(
        self, 
        series: str, 
        configuration: str = 'standard'
    ) -> Dict[str, Dict]:
        """
        Get all cross-sections for a series (head, sill, jamb, etc.)
        
        Args:
            series: Frame series
            configuration: Configuration type
        
        Returns:
            Dictionary keyed by view_type with cross-section data
        """
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            query = """
                SELECT view_type, image_path, dimensions, anchor_points, line_weights
                FROM frame_cross_sections
                WHERE series_name = %s 
                  AND configuration = %s
                  AND is_active = TRUE
                ORDER BY view_type
            """
            cur.execute(query, (series, configuration))
            
            results = cur.fetchall()
            cur.close()
            
            views = {}
            for row in results:
                view_type = row['view_type']
                image_path = row['image_path']
                dimensions = row['dimensions']
                anchor_points = row['anchor_points']
                line_weights = row['line_weights']
                
                full_path = self.project_root / image_path
                
                if full_path.exists():
                    try:
                        img = Image.open(full_path)
                        views[view_type] = {
                            'image': img,
                            'dimensions': dimensions,
                            'anchor_points': anchor_points,
                            'line_weights': line_weights,
                            'path': image_path,
                            'exists': True
                        }
                    except Exception as e:
                        logger.error(f"Failed to load image {full_path}: {e}")
                else:
                    logger.warning(f"Image not found: {full_path}")
                    views[view_type] = {
                        'image': None,
                        'dimensions': dimensions,
                        'anchor_points': anchor_points,
                        'line_weights': line_weights,
                        'path': image_path,
                        'exists': False
                    }
            
            return views
            
        except Exception as e:
            logger.error(f"Failed to get all views for series {series}: {e}")
            return {}
        finally:
            self.db_manager.return_connection(conn)
    
    def get_available_series(self) -> List[str]:
        """Get list of available frame series"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT series_name 
                FROM frame_cross_sections 
                WHERE is_active = TRUE
                ORDER BY series_name
            """)
            
            results = cur.fetchall()
            cur.close()
            
            return [row['series_name'] for row in results]
            
        except Exception as e:
            logger.error(f"Failed to get available series: {e}")
            return []
        finally:
            self.db_manager.return_connection(conn)
    
    def get_view_types_for_series(self, series: str) -> List[str]:
        """Get available view types for a specific series"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT view_type 
                FROM frame_cross_sections 
                WHERE series_name = %s AND is_active = TRUE
                ORDER BY view_type
            """, (series,))
            
            results = cur.fetchall()
            cur.close()
            
            return [row['view_type'] for row in results]
            
        except Exception as e:
            logger.error(f"Failed to get view types for series {series}: {e}")
            return []
        finally:
            self.db_manager.return_connection(conn)
    
    def clear_cache(self):
        """Clear the LRU cache"""
        self.get_cross_section.cache_clear()
        logger.info("Frame library cache cleared")
    
    def get_cache_info(self):
        """Get cache statistics"""
        return self.get_cross_section.cache_info()
