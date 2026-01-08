"""
Database Query Functions
Common database operations for CAD components and products
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseQueries:
    """Database query helper functions"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_product_types(self) -> List[str]:
        """Get all distinct product types"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT DISTINCT product_type 
                FROM product_configs 
                ORDER BY product_type
            """)
            results = cur.fetchall()
            cur.close()
            
            return [row['product_type'] for row in results]
        except Exception as e:
            logger.error(f"Failed to get product types: {e}")
            return ['FIXED', 'CASEMENT', 'DOUBLE CASEMENT', 'SLIDER', 'HINGED DOOR']
        finally:
            self.db_manager.return_connection(conn)
    
    def get_projects(self, limit: int = 100) -> List[Dict]:
        """Get recent projects"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM v_project_status
                ORDER BY last_synced DESC NULLS LAST
                LIMIT %s
            """, (limit,))
            results = cur.fetchall()
            cur.close()
            
            return [dict(row) for row in results]
        except Exception as e:
            logger.error(f"Failed to get projects: {e}")
            return []
        finally:
            self.db_manager.return_connection(conn)
    
    def get_product_config(self, item_number: str, project_id: Optional[int] = None) -> Optional[Dict]:
        """Get product configuration by item number"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            if project_id:
                cur.execute("""
                    SELECT * FROM product_configs
                    WHERE item_number = %s AND project_id = %s
                """, (item_number, project_id))
            else:
                cur.execute("""
                    SELECT * FROM product_configs
                    WHERE item_number = %s
                    ORDER BY created_at DESC
                    LIMIT 1
                """, (item_number,))
            
            result = cur.fetchone()
            cur.close()
            
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get product config: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def save_product_config(self, config: Dict) -> int:
        """Save or update product configuration"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            query = """
                INSERT INTO product_configs (
                    item_number, product_type, frame_series, 
                    width_inches, height_inches, configuration, 
                    specifications, project_id, is_door
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (item_number, project_id) 
                DO UPDATE SET
                    product_type = EXCLUDED.product_type,
                    frame_series = EXCLUDED.frame_series,
                    width_inches = EXCLUDED.width_inches,
                    height_inches = EXCLUDED.height_inches,
                    configuration = EXCLUDED.configuration,
                    specifications = EXCLUDED.specifications,
                    is_door = EXCLUDED.is_door,
                    updated_at = NOW()
                RETURNING id
            """
            
            cur.execute(query, (
                config.get('item_number'),
                config.get('product_type'),
                config.get('frame_series'),
                config.get('width_inches'),
                config.get('height_inches'),
                config.get('configuration'),
                config.get('specifications'),
                config.get('project_id'),
                config.get('is_door', False)
            ))
            
            result = cur.fetchone()
            conn.commit()
            cur.close()
            
            return result['id'] if result else None
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to save product config: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def get_drawing_template(self, template_type: str = 'window') -> Optional[Dict]:
        """Get default drawing template"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM drawing_templates
                WHERE template_type = %s AND is_default = TRUE
                LIMIT 1
            """, (template_type,))
            
            result = cur.fetchone()
            cur.close()
            
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get drawing template: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def save_generated_drawing(self, drawing_info: Dict) -> int:
        """Save generated drawing metadata"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            query = """
                INSERT INTO generated_drawings (
                    product_config_id, project_id, drawing_number,
                    file_path, file_size_kb, template_used,
                    generation_params, generated_by
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            cur.execute(query, (
                drawing_info.get('product_config_id'),
                drawing_info.get('project_id'),
                drawing_info.get('drawing_number'),
                drawing_info.get('file_path'),
                drawing_info.get('file_size_kb'),
                drawing_info.get('template_used'),
                drawing_info.get('generation_params'),
                drawing_info.get('generated_by', 'PyQt Desktop App')
            ))
            
            result = cur.fetchone()
            conn.commit()
            cur.close()
            
            return result['id'] if result else None
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to save generated drawing: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user preferences"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM user_preferences
                WHERE user_id = %s
            """, (user_id,))
            
            result = cur.fetchone()
            cur.close()
            
            return dict(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get user preferences: {e}")
            return None
        finally:
            self.db_manager.return_connection(conn)
    
    def save_user_preferences(self, user_id: str, preferences: Dict) -> bool:
        """Save user preferences"""
        conn = self.db_manager.get_connection()
        
        try:
            cur = conn.cursor()
            
            query = """
                INSERT INTO user_preferences (
                    user_id, default_series, default_template,
                    ui_settings, export_settings
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    default_series = EXCLUDED.default_series,
                    default_template = EXCLUDED.default_template,
                    ui_settings = EXCLUDED.ui_settings,
                    export_settings = EXCLUDED.export_settings,
                    updated_at = NOW()
            """
            
            cur.execute(query, (
                user_id,
                preferences.get('default_series'),
                preferences.get('default_template'),
                preferences.get('ui_settings'),
                preferences.get('export_settings')
            ))
            
            conn.commit()
            cur.close()
            
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Failed to save user preferences: {e}")
            return False
        finally:
            self.db_manager.return_connection(conn)
