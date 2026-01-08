-- ========================================
-- Raven Custom Glass - Database Initialization
-- PostgreSQL 15+
-- ========================================

-- Enable UUID extension for generating unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ========================================
-- REFERENCE TABLES FOR ACCURATE DRAWINGS
-- ========================================

-- Frame Series Reference Data
CREATE TABLE IF NOT EXISTS frame_series (
    id SERIAL PRIMARY KEY,
    series_name VARCHAR(50) NOT NULL UNIQUE,
    series_code VARCHAR(20) NOT NULL UNIQUE,
    frame_width_mm DECIMAL(10, 2) NOT NULL,
    sash_width_mm DECIMAL(10, 2),
    nail_fin_width_mm DECIMAL(10, 2) DEFAULT 30.00,
    nail_fin_height_mm DECIMAL(10, 2) DEFAULT 30.00,
    thermal_break BOOLEAN DEFAULT TRUE,
    glass_pocket_depth_mm DECIMAL(10, 2),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Window/Door Configuration Types
CREATE TABLE IF NOT EXISTS configuration_types (
    id SERIAL PRIMARY KEY,
    config_name VARCHAR(100) NOT NULL UNIQUE,
    config_code VARCHAR(20) NOT NULL,
    panel_count INTEGER NOT NULL,
    operable_panels INTEGER NOT NULL,
    panel_indicator_style VARCHAR(50),
    requires_mullions BOOLEAN DEFAULT FALSE,
    requires_hardware BOOLEAN DEFAULT TRUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Glass Types Reference
CREATE TABLE IF NOT EXISTS glass_types (
    id SERIAL PRIMARY KEY,
    glass_name VARCHAR(100) NOT NULL UNIQUE,
    glass_code VARCHAR(20) NOT NULL,
    thickness_mm DECIMAL(5, 2),
    u_factor DECIMAL(5, 3),
    shgc DECIMAL(5, 3),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Hardware Options Reference
CREATE TABLE IF NOT EXISTS hardware_options (
    id SERIAL PRIMARY KEY,
    hardware_name VARCHAR(100) NOT NULL,
    hardware_type VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(100),
    model_number VARCHAR(50),
    finish VARCHAR(50),
    applicable_configs TEXT[],
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Frame Colors Reference
CREATE TABLE IF NOT EXISTS frame_colors (
    id SERIAL PRIMARY KEY,
    color_name VARCHAR(100) NOT NULL UNIQUE,
    color_code VARCHAR(20),
    hex_value VARCHAR(7),
    rgb_value VARCHAR(50),
    finish_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for reference tables
CREATE INDEX idx_frame_series_code ON frame_series(series_code);
CREATE INDEX idx_config_types_code ON configuration_types(config_code);
CREATE INDEX idx_glass_types_code ON glass_types(glass_code);
CREATE INDEX idx_hardware_type ON hardware_options(hardware_type);
CREATE INDEX idx_frame_colors_code ON frame_colors(color_code);

-- ========================================
-- MAIN APPLICATION TABLES
-- ========================================
-- (These will be created by SQLAlchemy/Alembic)
-- Tables: projects, windows, doors
-- ========================================

COMMENT ON TABLE frame_series IS 'Reference data for frame profiles (Series 80, 86, 135, etc.)';
COMMENT ON TABLE configuration_types IS 'Reference data for window/door configurations (Fixed, Casement, Slider, etc.)';
COMMENT ON TABLE glass_types IS 'Reference data for glass specifications';
COMMENT ON TABLE hardware_options IS 'Reference data for hardware options (locks, handles, hinges)';
COMMENT ON TABLE frame_colors IS 'Reference data for frame color finishes';
