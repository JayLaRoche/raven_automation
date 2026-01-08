-- ========================================
-- Raven Custom Glass - Reference Data Seed
-- Accurate base data for professional drawings
-- ========================================

-- ========================================
-- FRAME SERIES DATA
-- ========================================
INSERT INTO frame_series (series_name, series_code, frame_width_mm, sash_width_mm, nail_fin_width_mm, nail_fin_height_mm, thermal_break, glass_pocket_depth_mm, description) VALUES
('Series 80', '80', 80.00, 40.00, 30.00, 30.00, TRUE, 25.00, 'Standard fixed window frame - aluminum with thermal break'),
('Series 86', '86', 86.00, 48.00, 30.00, 30.00, TRUE, 28.00, 'Casement/awning frame - operable windows with multi-point locks'),
('Series 135', '135', 135.00, 65.00, 30.00, 30.00, TRUE, 35.00, 'Heavy-duty patio door frame - commercial grade'),
('Series 90', '90', 90.00, 45.00, 30.00, 30.00, TRUE, 26.00, 'Slider frame - horizontal sliding windows'),
('Series 200', '200', 200.00, 80.00, 40.00, 40.00, TRUE, 40.00, 'Commercial storefront door - heavy-duty')
ON CONFLICT (series_code) DO NOTHING;

-- ========================================
-- CONFIGURATION TYPES DATA
-- ========================================
INSERT INTO configuration_types (config_name, config_code, panel_count, operable_panels, panel_indicator_style, requires_mullions, requires_hardware, description) VALUES
('Fixed', 'FX', 1, 0, 'text_F_centered', FALSE, FALSE, 'Non-operable fixed window'),
('Single Casement', 'CS', 1, 1, 'diagonal_line', FALSE, TRUE, 'Single operable casement window - left or right swing'),
('Double Casement', 'DCS', 2, 2, 'diagonal_line', TRUE, TRUE, 'Two operable casement panels with center mullion'),
('Awning', 'AW', 1, 1, 'horizontal_pivot', FALSE, TRUE, 'Top-hinged outward opening window'),
('Hopper', 'HP', 1, 1, 'horizontal_pivot_bottom', FALSE, TRUE, 'Bottom-hinged inward opening window'),
('Slider 2-Panel', 'SL2', 2, 1, 'arrows', TRUE, TRUE, 'Two-panel horizontal slider - one fixed, one operable'),
('Slider 3-Panel', 'SL3', 3, 1, 'arrows', TRUE, TRUE, 'Three-panel slider - X-O-X configuration'),
('Slider 4-Panel', 'SL4', 4, 2, 'arrows', TRUE, TRUE, 'Four-panel slider - X-O-O-X configuration'),
('Pivot', 'PV', 1, 1, 'center_pivot', FALSE, TRUE, 'Center-pivoting window'),
('Bifold', 'BF', 2, 2, 'bifold_icon', TRUE, TRUE, 'Bifold door - two panels folding'),
('Accordion', 'AC', 4, 4, 'accordion_icon', TRUE, TRUE, 'Multi-panel accordion/folding door'),
('Sliding Door 2-Panel', 'SD2', 2, 1, 'arrows', TRUE, TRUE, 'Patio door - two panels, one operable'),
('Sliding Door 3-Panel', 'SD3', 3, 2, 'arrows', TRUE, TRUE, 'Patio door - three panels, center operable')
ON CONFLICT (config_name) DO NOTHING;

-- ========================================
-- GLASS TYPES DATA
-- ========================================
INSERT INTO glass_types (glass_name, glass_code, thickness_mm, u_factor, shgc, description) VALUES
('Single Pane Clear', 'SPC', 3.00, 1.04, 0.86, 'Single 1/8" clear glass'),
('Dual Pane Clear', 'DPC', 25.00, 0.48, 0.70, '1" insulated unit - 2 panes clear glass with air gap'),
('Low-E Dual Pane', 'LED', 25.00, 0.29, 0.56, '1" insulated unit - Low-E coating, argon fill'),
('Low-E Triple Pane', 'LET', 38.00, 0.20, 0.47, '1.5" insulated unit - 3 panes with Low-E, argon fill'),
('Tempered Clear', 'TC', 6.00, 1.04, 0.84, 'Tempered safety glass - 1/4" thick'),
('Laminated Safety', 'LS', 6.35, 0.90, 0.75, 'Laminated safety glass with PVB interlayer'),
('Obscure/Frosted', 'OF', 6.00, 1.04, 0.78, 'Privacy glass - textured or frosted'),
('Tinted Bronze', 'TB', 6.00, 0.98, 0.64, 'Bronze tinted glass - heat reduction'),
('Impact Resistant', 'IR', 9.00, 0.55, 0.62, 'Hurricane impact resistant - laminated dual pane')
ON CONFLICT (glass_name) DO NOTHING;

-- ========================================
-- HARDWARE OPTIONS DATA
-- ========================================
INSERT INTO hardware_options (hardware_name, hardware_type, manufacturer, model_number, finish, applicable_configs, description) VALUES
('Standard Casement Lock', 'Lock', 'Truth Hardware', 'T2000', 'White', ARRAY['CS', 'DCS', 'AW'], 'Multi-point casement lock with keeper'),
('Heavy-Duty Casement Lock', 'Lock', 'Truth Hardware', 'T3000', 'Bronze', ARRAY['CS', 'DCS'], 'Commercial grade multi-point lock'),
('Sliding Door Lock', 'Lock', 'Ashland Hardware', 'SDL-100', 'Satin Nickel', ARRAY['SD2', 'SD3'], 'Mortise lock for sliding patio doors'),
('Slider Window Lock', 'Lock', 'Prime-Line', 'SWL-50', 'White', ARRAY['SL2', 'SL3', 'SL4'], 'Cam-action sliding window lock'),
('Casement Operator', 'Operator', 'Truth Hardware', 'CO-200', 'White', ARRAY['CS', 'DCS'], 'Fold-down handle casement operator'),
('Awning Operator', 'Operator', 'Truth Hardware', 'AO-150', 'White', ARRAY['AW'], 'Push-bar awning window operator'),
('Bifold Hardware Set', 'Hardware Set', 'Johnson Hardware', 'BF-2000', 'Aluminum', ARRAY['BF'], 'Complete bifold door hardware kit - hinges, track, handle'),
('Accordion Track System', 'Track System', 'National Guard', 'AC-500', 'Bronze', ARRAY['AC'], 'Heavy-duty accordion door track and carriers'),
('Door Handle Set', 'Handle', 'Ashland Hardware', 'DH-300', 'Satin Nickel', ARRAY['SD2', 'SD3'], 'Interior/exterior patio door handle set'),
('Hinges - Casement', 'Hinge', 'Truth Hardware', 'H-400', 'Stainless', ARRAY['CS', 'DCS', 'AW'], 'Concealed casement window hinges - set of 2'),
('Hinges - Awning', 'Hinge', 'Truth Hardware', 'H-350', 'Stainless', ARRAY['AW', 'HP'], 'Top-hung awning hinges'),
('Multipoint Lock Kit', 'Lock Kit', 'Truth Hardware', 'MPL-500', 'White', ARRAY['CS', 'DCS'], 'Complete multi-point lock system with 3 locking points')
ON CONFLICT DO NOTHING;

-- ========================================
-- FRAME COLORS DATA
-- ========================================
INSERT INTO frame_colors (color_name, color_code, hex_value, rgb_value, finish_type) VALUES
('White', 'WHT', '#FFFFFF', '255,255,255', 'Powder Coat'),
('Bronze', 'BRZ', '#614E1A', '97,78,26', 'Anodized'),
('Black', 'BLK', '#000000', '0,0,0', 'Powder Coat'),
('Silver', 'SLV', '#C0C0C0', '192,192,192', 'Anodized'),
('Beige/Tan', 'BGE', '#D2B48C', '210,180,140', 'Powder Coat'),
('Gray', 'GRY', '#808080', '128,128,128', 'Powder Coat'),
('Dark Bronze', 'DBR', '#3E2723', '62,39,35', 'Anodized'),
('Champagne', 'CHP', '#F7E7CE', '247,231,206', 'Anodized'),
('Custom Color', 'CUS', NULL, NULL, 'Custom Match')
ON CONFLICT (color_name) DO NOTHING;

-- ========================================
-- VERIFICATION
-- ========================================
-- Show counts of inserted reference data
DO $$
BEGIN
    RAISE NOTICE 'Reference Data Inserted:';
    RAISE NOTICE '- Frame Series: %', (SELECT COUNT(*) FROM frame_series);
    RAISE NOTICE '- Configuration Types: %', (SELECT COUNT(*) FROM configuration_types);
    RAISE NOTICE '- Glass Types: %', (SELECT COUNT(*) FROM glass_types);
    RAISE NOTICE '- Hardware Options: %', (SELECT COUNT(*) FROM hardware_options);
    RAISE NOTICE '- Frame Colors: %', (SELECT COUNT(*) FROM frame_colors);
END $$;
