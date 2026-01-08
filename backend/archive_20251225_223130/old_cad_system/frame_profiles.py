"""
Frame Profile Definitions
Exact geometric data for each frame series used in Raven shop drawings
"""

# All dimensions in millimeters unless specified
FRAME_PROFILES = {
    '80': {
        'name': 'Series 80',
        'description': 'Fixed Window Profile',
        'total_width': 619,  # mm
        'frame_face_width': 80,
        'segments': [80, 34, 24, 196, 33, 34, 24, 58, 80],  # Left to right positions
        'nail_fin': {
            'width': 30,
            'height': 30,
            'offset': 40,  # distance from frame outer edge
            'position': 'outside'
        },
        'thermal_breaks': [
            {'start': 80 + 34, 'width': 24, 'offset': 30},
            {'start': 80 + 34 + 24 + 196 + 33, 'width': 24, 'offset': 30}
        ],
        'glass_pocket': {
            'start': 80 + 34,
            'width': 196,
            'depth': 27
        },
        'horizontal_section': {
            'segments': [40, 86, 64],  # Typical horizontal cross-section
            'total': 190
        },
        'label_dimensions': {
            'top': '40-30',
            'left': '80-34-24-196-33-34-24-58-80',
            'bottom': '40-30-40-30',
            'right': '33-619'
        }
    },
    
    '86': {
        'name': 'Series 86',
        'description': 'Casement Window Profile',
        'total_width': 650,
        'frame_face_width': 86,
        'segments': [86, 16, 40, 30, 64, 86],
        'nail_fin': {
            'width': 30,
            'height': 30,
            'offset': 40,
            'position': 'outside'
        },
        'thermal_breaks': [
            {'start': 86 + 16, 'width': 40, 'offset': 20}
        ],
        'glass_pocket': {
            'start': 86 + 16,
            'width': 40,
            'depth': 30
        },
        'hinge_pocket': {
            'width': 30,
            'depth': 20,
            'position': 'left_or_right'  # Depends on casement direction
        },
        'horizontal_section': {
            'segments': [40, 100, 64],
            'total': 204
        },
        'label_dimensions': {
            'top': '40-30',
            'left': '86-16-40-30-64',
            'bottom': '40-30-40-30',
            'right': '30-650'
        }
    },
    
    '135': {
        'name': 'Series 135',
        'description': 'Sliding Door Profile',
        'total_width': 1100,  # Typical
        'frame_face_width': 135,
        'segments': [36, 73, 6, 73, 36, 135, 45],
        'nail_fin': {
            'width': 30,
            'height': 30,
            'offset': 40,
            'position': 'outside'
        },
        'thermal_breaks': [
            {'start': 36 + 73, 'width': 6, 'offset': 30},
            {'start': 36 + 73 + 6 + 73, 'width': 36, 'offset': 30}
        ],
        'track_channels': [
            {'position': 36 + 73, 'width': 6, 'depth': 15},
            {'position': 36 + 73 + 6 + 73 + 36, 'width': 6, 'depth': 15}
        ],
        'threshold': {
            'height': 50,  # mm - "High Threshold"
            'width': 135,
            'label': 'High Threshold: 50MM'
        },
        'horizontal_section': {
            'segments': [40, 140, 80],
            'total': 260
        },
        'label_dimensions': {
            'top': '40-30',
            'left': '36-73-6-73-36-135-45',
            'bottom': '40-30-40-30',
            'right': '50-1100'
        }
    }
}


def get_profile(series_number):
    """Get frame profile by series number"""
    series_str = str(series_number).replace('Series ', '').strip()
    return FRAME_PROFILES.get(series_str, FRAME_PROFILES['80'])


def get_series_list():
    """Get list of available series"""
    return list(FRAME_PROFILES.keys())


# Color definitions for drawing
PROFILE_COLORS = {
    'frame_outline': (0, 0, 0),  # Black, RGB
    'thermal_break': (1, 0, 0, 0.2),  # Red with transparency
    'nail_flange_fill': (1, 0, 0, 0.3),  # Red with transparency
    'nail_flange_outline': (1, 0, 0),  # Solid red
    'hatching': (0.7, 0.7, 0.7),  # Gray
    'glass_pocket': (0.9, 0.9, 1.0)  # Light blue
}


# Hatching pattern for section drawings
HATCHING_PATTERN = {
    'angle': 45,  # degrees
    'spacing': 3,  # mm between lines
    'line_width': 0.3  # pt
}


# Line weights for different elements
LINE_WEIGHTS = {
    'page_border': 1.5,
    'frame_outline': 1.2,
    'mullion': 0.8,
    'dimension': 0.7,
    'label_box': 0.5,
    'hatching': 0.3,
    'hidden_line': 0.5
}


# Dash patterns
DASH_PATTERNS = {
    'glass_pocket': [2, 2],  # 2mm dash, 2mm gap
    'centerline': [5, 2, 1, 2]  # Long-short pattern
}
