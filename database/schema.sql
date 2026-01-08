-- ========================================
-- RAVEN CUSTOM GLASS - CAD COMPONENT DATABASE SCHEMA
-- PostgreSQL 15+
-- ========================================

-- Enable UUID extension for generating unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- FRAME CROSS-SECTIONS LIBRARY
-- ========================================

-- Frame cross-sections library (head, sill, jamb, etc.)
CREATE TABLE IF NOT EXISTS frame_cross_sections (
    id SERIAL PRIMARY KEY,
    series_name VARCHAR(10) NOT NULL,        -- '80', '86', '65', '135', '68', 'MD100H', etc.
    view_type VARCHAR(50) NOT NULL,          -- 'head', 'sill', 'jamb', 'horizontal', 'vertical'
    configuration VARCHAR(50) DEFAULT 'standard',  -- 'single', 'double', 'slider_track', 'mullion', etc.
    image_path VARCHAR(500) NOT NULL,        -- 'assets/frames/series_65/head_single.png'
    image_filename VARCHAR(255),             -- 'head_single.png'
    dimensions JSONB,                         -- {width: 67, height: 29, frame_depth: 50.3}
    anchor_points JSONB,                      -- For precise CAD placement {top_left: [0,0], center: [33.5,14.5]}
    line_weights JSONB,                       -- CAD line weight standards {outer: 2.0, inner: 0.5, dimension: 0.25}
    notes TEXT,                               -- Additional notes or specifications
    is_active BOOLEAN DEFAULT TRUE,           -- For soft deletion
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(series_name, view_type, configuration)
);

CREATE INDEX idx_series_lookup ON frame_cross_sections(series_name, view_type);
CREATE INDEX idx_configuration ON frame_cross_sections(configuration);
CREATE INDEX idx_active ON frame_cross_sections(is_active);

COMMENT ON TABLE frame_cross_sections IS 'Library of frame profile cross-sections for CAD drawing generation';
COMMENT ON COLUMN frame_cross_sections.dimensions IS 'JSON: {width_mm, height_mm, frame_depth_mm, glass_pocket_depth}';
COMMENT ON COLUMN frame_cross_sections.anchor_points IS 'JSON: Reference points for CAD alignment';

-- ========================================
-- CAD DRAWING COMPONENTS
-- ========================================

-- Reusable CAD drawing components (elevations, details, symbols)
CREATE TABLE IF NOT EXISTS cad_components (
    id SERIAL PRIMARY KEY,
    component_type VARCHAR(50) NOT NULL,     -- 'elevation', 'plan', 'silhouette', 'detail', 'symbol'
    component_name VARCHAR(100) NOT NULL,    -- 'casement_swing_left', 'fixed_elevation', etc.
    category VARCHAR(50),                     -- 'window', 'door', 'hardware', 'general'
    svg_data BYTEA,                          -- SVG vector data for scalable rendering
    png_data BYTEA,                          -- Rasterized preview
    metadata JSONB,                          -- {scale: 1.0, units: 'mm', line_weight: 0.5}
    thumbnail BYTEA,                         -- Small preview image
    tags TEXT[],                             -- Searchable tags ['casement', 'operable', 'left_hand']
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_component_type ON cad_components(component_type);
CREATE INDEX idx_category ON cad_components(category);
CREATE INDEX idx_tags ON cad_components USING GIN(tags);

COMMENT ON TABLE cad_components IS 'Reusable CAD drawing elements and symbols';

-- ========================================
-- PRODUCT CONFIGURATIONS
-- ========================================

-- Window/Door configurations (cached from Google Sheets)
CREATE TABLE IF NOT EXISTS product_configs (
    id SERIAL PRIMARY KEY,
    item_number VARCHAR(50) NOT NULL,
    product_type VARCHAR(50) NOT NULL,       -- 'CASEMENT', 'FIXED', 'SLIDER', 'HINGED_DOOR', etc.
    frame_series VARCHAR(10) NOT NULL,       -- Links to frame_cross_sections.series_name
    width_inches DECIMAL(6,2) NOT NULL,
    height_inches DECIMAL(6,2) NOT NULL,
    configuration JSONB,                      -- {panels: 2, notation: 'XO', swing: 'left', track: 'double'}
    specifications JSONB,                     -- {glass: 'Low-E', color: 'Bronze', grids: 'Colonial'}
    project_id INTEGER,                       -- Links to projects table
    sheet_row_number INTEGER,                 -- Original row in Google Sheets
    is_door BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(item_number, project_id)
);

CREATE INDEX idx_product_type ON product_configs(product_type);
CREATE INDEX idx_frame_series ON product_configs(frame_series);
CREATE INDEX idx_project_id ON product_configs(project_id);

COMMENT ON TABLE product_configs IS 'Product specifications cached from Google Sheets';

-- ========================================
-- PROJECTS
-- ========================================

-- Projects (linked to Google Sheets)
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    po_number VARCHAR(100),
    client_info JSONB,                       -- {name, address, contact, billing_address}
    sheet_url TEXT,                          -- Link to Google Sheet
    sheet_id VARCHAR(100),                   -- Google Sheet ID
    sheet_name VARCHAR(100),                 -- Sheet tab name
    last_synced TIMESTAMP,
    sync_status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'syncing', 'synced', 'error'
    sync_error TEXT,                         -- Error message if sync failed
    item_count INTEGER DEFAULT 0,            -- Number of items in project
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_po_number ON projects(po_number);
CREATE INDEX idx_sync_status ON projects(sync_status);
CREATE INDEX idx_last_synced ON projects(last_synced);

COMMENT ON TABLE projects IS 'Project metadata with Google Sheets synchronization status';

-- ========================================
-- DRAWING TEMPLATES
-- ========================================

-- Drawing layout templates
CREATE TABLE IF NOT EXISTS drawing_templates (
    id SERIAL PRIMARY KEY,
    template_name VARCHAR(100) NOT NULL UNIQUE,
    template_type VARCHAR(50) NOT NULL,      -- 'window', 'door', 'custom'
    page_size VARCHAR(20) DEFAULT 'A3',      -- 'A3', 'A4', 'Letter', 'Legal'
    orientation VARCHAR(20) DEFAULT 'landscape', -- 'landscape', 'portrait'
    layout_config JSONB NOT NULL,            -- {zones: [...], margins: {...}, title_block: {...}}
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_template_type ON drawing_templates(template_type);
CREATE INDEX idx_is_default ON drawing_templates(is_default);

COMMENT ON TABLE drawing_templates IS 'Drawing layout templates for different product types';

-- ========================================
-- GENERATED DRAWINGS
-- ========================================

-- Generated drawings tracking
CREATE TABLE IF NOT EXISTS generated_drawings (
    id SERIAL PRIMARY KEY,
    product_config_id INTEGER REFERENCES product_configs(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    drawing_number VARCHAR(50),
    file_path VARCHAR(500) NOT NULL,         -- Path to generated PDF
    file_size_kb INTEGER,
    template_used INTEGER REFERENCES drawing_templates(id),
    generation_params JSONB,                 -- Parameters used for generation
    preview_image BYTEA,                     -- Thumbnail preview
    generated_by VARCHAR(100),               -- User or system identifier
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_product_config ON generated_drawings(product_config_id);
CREATE INDEX idx_project ON generated_drawings(project_id);
CREATE INDEX idx_drawing_number ON generated_drawings(drawing_number);

COMMENT ON TABLE generated_drawings IS 'History of generated drawings with metadata';

-- ========================================
-- USER PREFERENCES
-- ========================================

-- Application user preferences
CREATE TABLE IF NOT EXISTS user_preferences (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL UNIQUE,    -- System username or email
    default_series VARCHAR(10),               -- Default frame series
    default_template INTEGER REFERENCES drawing_templates(id),
    ui_settings JSONB,                        -- {theme: 'dark', panel_width: 300, recent_projects: [...]}
    export_settings JSONB,                    -- {default_format: 'PDF', dpi: 300, color_mode: 'RGB'}
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

COMMENT ON TABLE user_preferences IS 'Desktop application user preferences and settings';

-- ========================================
-- SEED DATA FOR DRAWING TEMPLATES
-- ========================================

-- Default window template
INSERT INTO drawing_templates (template_name, template_type, page_size, orientation, layout_config, is_default)
VALUES (
    'Standard Window Drawing',
    'window',
    'A3',
    'landscape',
    '{
        "zones": [
            {"name": "elevation", "x": 0.45, "y": 0.3, "width": 0.4, "height": 0.6},
            {"name": "cross_section_head", "x": 0.05, "y": 0.75, "width": 0.3, "height": 0.15},
            {"name": "cross_section_sill", "x": 0.05, "y": 0.55, "width": 0.3, "height": 0.15},
            {"name": "cross_section_jamb", "x": 0.05, "y": 0.35, "width": 0.3, "height": 0.15},
            {"name": "title_block", "x": 0.7, "y": 0.05, "width": 0.25, "height": 0.15},
            {"name": "specifications", "x": 0.05, "y": 0.05, "width": 0.3, "height": 0.25}
        ],
        "margins": {"top": 0.02, "bottom": 0.02, "left": 0.02, "right": 0.02},
        "title_block": {"company": "Raven Custom Glass", "show_logo": true}
    }'::jsonb,
    true
) ON CONFLICT (template_name) DO NOTHING;

-- Default door template
INSERT INTO drawing_templates (template_name, template_type, page_size, orientation, layout_config, is_default)
VALUES (
    'Standard Door Drawing',
    'door',
    'A3',
    'landscape',
    '{
        "zones": [
            {"name": "elevation", "x": 0.4, "y": 0.2, "width": 0.35, "height": 0.7},
            {"name": "cross_section_head", "x": 0.05, "y": 0.75, "width": 0.3, "height": 0.15},
            {"name": "cross_section_sill", "x": 0.05, "y": 0.55, "width": 0.3, "height": 0.15},
            {"name": "cross_section_jamb", "x": 0.05, "y": 0.35, "width": 0.3, "height": 0.15},
            {"name": "title_block", "x": 0.7, "y": 0.05, "width": 0.25, "height": 0.15},
            {"name": "specifications", "x": 0.05, "y": 0.05, "width": 0.3, "height": 0.25}
        ],
        "margins": {"top": 0.02, "bottom": 0.02, "left": 0.02, "right": 0.02},
        "title_block": {"company": "Raven Custom Glass", "show_logo": true}
    }'::jsonb,
    true
) ON CONFLICT (template_name) DO NOTHING;

-- ========================================
-- FUNCTIONS AND TRIGGERS
-- ========================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to all tables
CREATE TRIGGER update_frame_cross_sections_updated_at BEFORE UPDATE ON frame_cross_sections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cad_components_updated_at BEFORE UPDATE ON cad_components
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_configs_updated_at BEFORE UPDATE ON product_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_drawing_templates_updated_at BEFORE UPDATE ON drawing_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_preferences_updated_at BEFORE UPDATE ON user_preferences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ========================================
-- SAMPLE DATA FOR DEVELOPMENT
-- ========================================

-- Sample frame cross-sections (placeholder paths - images need to be created)
INSERT INTO frame_cross_sections (series_name, view_type, configuration, image_path, image_filename, dimensions, anchor_points, line_weights, notes)
VALUES
    ('65', 'head', 'single', 'assets/frames/series_65/head_single.png', 'head_single.png', 
     '{"width_mm": 67, "height_mm": 29, "frame_depth_mm": 50.3, "glass_pocket_depth": 25}'::jsonb,
     '{"top_left": [0, 0], "center": [33.5, 14.5], "glass_center": [33.5, 14.5]}'::jsonb,
     '{"outer": 2.0, "inner": 0.5, "dimension": 0.25}'::jsonb,
     'Series 65 head section for single panel configurations'),
    
    ('65', 'sill', 'single', 'assets/frames/series_65/sill_single.png', 'sill_single.png',
     '{"width_mm": 67, "height_mm": 35, "frame_depth_mm": 50.3, "drainage_slope": 5}'::jsonb,
     '{"top_left": [0, 0], "center": [33.5, 17.5]}'::jsonb,
     '{"outer": 2.0, "inner": 0.5, "dimension": 0.25}'::jsonb,
     'Series 65 sill section with weep drainage'),
    
    ('80', 'head', 'fixed', 'assets/frames/series_80/head_fixed.png', 'head_fixed.png',
     '{"width_mm": 80, "height_mm": 40, "frame_depth_mm": 55, "glass_pocket_depth": 28}'::jsonb,
     '{"top_left": [0, 0], "center": [40, 20]}'::jsonb,
     '{"outer": 2.0, "inner": 0.5, "dimension": 0.25}'::jsonb,
     'Series 80 fixed window head section'),
    
    ('86', 'jamb', 'casement', 'assets/frames/series_86/jamb_casement.png', 'jamb_casement.png',
     '{"width_mm": 86, "height_mm": 48, "frame_depth_mm": 62, "hinge_clearance": 15}'::jsonb,
     '{"top_left": [0, 0], "center": [43, 24]}'::jsonb,
     '{"outer": 2.0, "inner": 0.5, "dimension": 0.25}'::jsonb,
     'Series 86 casement jamb with hinge clearance'),
    
    ('135', 'sill', 'door', 'assets/frames/series_135/sill_door.png', 'sill_door.png',
     '{"width_mm": 135, "height_mm": 65, "frame_depth_mm": 78, "threshold_height": 20}'::jsonb,
     '{"top_left": [0, 0], "center": [67.5, 32.5]}'::jsonb,
     '{"outer": 2.5, "inner": 0.5, "dimension": 0.25}'::jsonb,
     'Series 135 patio door sill with integrated threshold')
ON CONFLICT (series_name, view_type, configuration) DO NOTHING;

-- ========================================
-- VIEWS FOR COMMON QUERIES
-- ========================================

-- View for complete frame cross-section sets
CREATE OR REPLACE VIEW v_frame_series_complete AS
SELECT 
    series_name,
    COUNT(*) as view_count,
    ARRAY_AGG(DISTINCT view_type ORDER BY view_type) as available_views,
    ARRAY_AGG(DISTINCT configuration ORDER BY configuration) as configurations,
    MAX(updated_at) as last_updated
FROM frame_cross_sections
WHERE is_active = TRUE
GROUP BY series_name;

COMMENT ON VIEW v_frame_series_complete IS 'Summary of available views for each frame series';

-- View for project sync status
CREATE OR REPLACE VIEW v_project_status AS
SELECT 
    p.id,
    p.project_name,
    p.po_number,
    p.sync_status,
    p.last_synced,
    p.item_count,
    COUNT(pc.id) as cached_items,
    COUNT(gd.id) as generated_drawings
FROM projects p
LEFT JOIN product_configs pc ON pc.project_id = p.id
LEFT JOIN generated_drawings gd ON gd.project_id = p.id
GROUP BY p.id, p.project_name, p.po_number, p.sync_status, p.last_synced, p.item_count;

COMMENT ON VIEW v_project_status IS 'Project overview with sync and drawing counts';
