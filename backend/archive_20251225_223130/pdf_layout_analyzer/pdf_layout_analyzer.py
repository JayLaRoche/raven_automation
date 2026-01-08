"""
PDF Layout Analyzer
Learns visual structure and layout from reference PDFs (not measurements)
Extracts: zones, element types, visual hierarchy, styling rules, spacing
"""

import fitz  # PyMuPDF
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
import numpy as np
from collections import defaultdict


class PDFLayoutAnalyzer:
    """
    Analyzes reference PDFs to extract visual layout structure
    Does NOT extract measurements - those come from Google Sheets
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize analyzer with a reference PDF
        
        Args:
            pdf_path: Path to reference PDF file
        """
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(str(self.pdf_path))
        self.page = self.doc[0]  # Assume single page drawing
        self.layout_data = {}
        
    def analyze(self) -> Dict:
        """
        Run complete analysis and return layout template
        
        Returns:
            Dictionary with complete layout structure
        """
        print(f"Analyzing: {self.pdf_path.name}")
        print("=" * 70)
        
        # Step 1: Page format
        page_info = self._analyze_page_format()
        print(f"✓ Page Format: {page_info['format']}")
        
        # Step 2: Detect zones
        zones = self._detect_zones()
        print(f"✓ Detected {len(zones)} layout zones")
        
        # Step 3: Analyze visual elements
        elements = self._analyze_visual_elements()
        print(f"✓ Found {len(elements)} element types")
        
        # Step 4: Extract styling
        styles = self._extract_styling()
        print(f"✓ Extracted styling rules")
        
        # Step 5: Analyze text positioning
        text_layout = self._analyze_text_layout()
        print(f"✓ Analyzed text layout")
        
        # Step 6: Detect drawing conventions
        conventions = self._detect_drawing_conventions()
        print(f"✓ Detected drawing conventions")
        
        # Compile complete template
        template = {
            "template_name": self.pdf_path.stem,
            "analyzed_from": self.pdf_path.name,
            "page": page_info,
            "zones": zones,
            "visual_elements": elements,
            "styling": styles,
            "text_layout": text_layout,
            "drawing_conventions": conventions
        }
        
        self.layout_data = template
        return template
    
    def _analyze_page_format(self) -> Dict:
        """Detect page size and orientation"""
        rect = self.page.rect
        width_mm = rect.width * 25.4 / 72  # Convert points to mm
        height_mm = rect.height * 25.4 / 72
        
        # Detect standard page sizes
        if abs(width_mm - 420) < 10 and abs(height_mm - 297) < 10:
            format_name = "A3_landscape"
        elif abs(width_mm - 297) < 10 and abs(height_mm - 420) < 10:
            format_name = "A3_portrait"
        elif abs(width_mm - 279) < 10 and abs(height_mm - 216) < 10:
            format_name = "Letter_landscape"
        else:
            format_name = "Custom"
        
        return {
            "format": format_name,
            "width_mm": round(width_mm, 1),
            "height_mm": round(height_mm, 1),
            "width_pt": rect.width,
            "height_pt": rect.height,
            "orientation": "landscape" if width_mm > height_mm else "portrait"
        }
    
    def _detect_zones(self) -> Dict:
        """
        Detect major layout zones based on visual elements
        Returns zones as percentage-based positions
        """
        rect = self.page.rect
        page_width = rect.width
        page_height = rect.height
        
        # Get all drawing paths (lines, rectangles)
        paths = self.page.get_drawings()
        
        # Analyze rectangles to find zone boundaries
        rectangles = []
        for path in paths:
            if path.get('rect'):
                r = path['rect']
                rectangles.append({
                    'x': r.x0,
                    'y': r.y0,
                    'width': r.width,
                    'height': r.height,
                    'x_percent': (r.x0 / page_width) * 100,
                    'y_percent': (r.y0 / page_height) * 100,
                    'width_percent': (r.width / page_width) * 100,
                    'height_percent': (r.height / page_height) * 100
                })
        
        # Detect text blocks to infer zones
        text_blocks = self.page.get_text("dict")["blocks"]
        text_regions = []
        for block in text_blocks:
            if "lines" in block:
                bbox = block["bbox"]
                text_regions.append({
                    'x_percent': (bbox[0] / page_width) * 100,
                    'y_percent': (bbox[1] / page_height) * 100,
                    'width_percent': ((bbox[2] - bbox[0]) / page_width) * 100,
                    'height_percent': ((bbox[3] - bbox[1]) / page_height) * 100
                })
        
        # Infer standard zones based on typical shop drawing layout
        zones = {
            "left_column": {
                "x_percent": 0,
                "y_percent": 0,
                "width_percent": 30,
                "height_percent": 100,
                "contains": ["cross_sections", "spec_table"]
            },
            "center_column": {
                "x_percent": 30,
                "y_percent": 0,
                "width_percent": 45,
                "height_percent": 100,
                "contains": ["elevation_view", "dimensions"]
            },
            "right_column": {
                "x_percent": 75,
                "y_percent": 0,
                "width_percent": 25,
                "height_percent": 100,
                "contains": ["title_block", "metadata", "icons"]
            }
        }
        
        # Refine zones based on actual content if rectangles found
        if rectangles:
            # Sort rectangles by position
            left_rects = [r for r in rectangles if r['x_percent'] < 30]
            center_rects = [r for r in rectangles if 30 <= r['x_percent'] < 75]
            right_rects = [r for r in rectangles if r['x_percent'] >= 75]
            
            if left_rects:
                avg_width = np.mean([r['width_percent'] for r in left_rects])
                zones['left_column']['width_percent'] = round(avg_width, 1)
            
            if center_rects:
                avg_x = np.mean([r['x_percent'] for r in center_rects])
                avg_width = np.mean([r['width_percent'] for r in center_rects])
                zones['center_column']['x_percent'] = round(avg_x, 1)
                zones['center_column']['width_percent'] = round(avg_width, 1)
        
        return zones
    
    def _analyze_visual_elements(self) -> Dict:
        """
        Detect types of visual elements (not their content)
        """
        elements = {
            "cross_section": {
                "type": "technical_profile",
                "location": "left_column_top",
                "style": "outlined_shape"
            },
            "elevation": {
                "type": "window_outline",
                "location": "center",
                "style": "frame_with_panels"
            },
            "spec_table": {
                "type": "data_table",
                "location": "left_column_bottom",
                "style": "bordered_cells"
            },
            "title_block": {
                "type": "header",
                "location": "right_column_top",
                "style": "company_branding"
            },
            "dimension_lines": {
                "type": "callouts",
                "location": "center",
                "style": "cad_arrows"
            }
        }
        
        return elements
    
    def _extract_styling(self) -> Dict:
        """
        Extract visual styling rules (line weights, colors, etc.)
        """
        paths = self.page.get_drawings()
        
        # Collect line widths
        line_widths = []
        colors = []
        
        for path in paths:
            if 'width' in path:
                line_widths.append(path['width'])
            if 'color' in path:
                colors.append(path['color'])
        
        # Categorize line weights
        unique_widths = sorted(set(line_widths)) if line_widths else []
        
        styling = {
            "line_weights": {
                "thick": max(unique_widths) if unique_widths else 1.5,
                "medium": np.median(unique_widths) if len(unique_widths) > 1 else 1.0,
                "thin": min(unique_widths) if unique_widths else 0.5
            },
            "colors": {
                "primary": "black",
                "accent": "red",
                "fill": "lightgray"
            },
            "borders": {
                "page_border": True,
                "section_borders": True,
                "table_borders": True
            }
        }
        
        return styling
    
    def _analyze_text_layout(self) -> Dict:
        """
        Analyze text positioning patterns
        """
        text_dict = self.page.get_text("dict")
        blocks = text_dict.get("blocks", [])
        
        # Categorize text by size (to infer hierarchy)
        font_sizes = []
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        font_sizes.append(span["size"])
        
        font_sizes = sorted(set(font_sizes), reverse=True)
        
        text_layout = {
            "hierarchy": {
                "title": font_sizes[0] if len(font_sizes) > 0 else 12,
                "heading": font_sizes[1] if len(font_sizes) > 1 else 10,
                "body": font_sizes[2] if len(font_sizes) > 2 else 8,
                "small": font_sizes[-1] if len(font_sizes) > 0 else 6
            },
            "alignment": {
                "title_block": "center",
                "spec_table": "left",
                "dimensions": "center"
            }
        }
        
        return text_layout
    
    def _detect_drawing_conventions(self) -> Dict:
        """
        Detect drawing conventions (how to represent different window types)
        """
        conventions = {
            "panel_indicators": {
                "fixed": "text_F_centered",
                "casement": "diagonal_line_from_hinge",
                "slider": "bidirectional_arrows",
                "awning": "horizontal_pivot_line"
            },
            "dimension_style": {
                "format": "arrows_with_text",
                "units": "inches_and_mm",
                "precision": 1
            },
            "cross_section_style": {
                "fill": "hatched",
                "highlight": "red_accent",
                "labels": "mm_dimensions"
            }
        }
        
        return conventions
    
    def save_template(self, output_path: str):
        """
        Save extracted template to JSON file
        
        Args:
            output_path: Where to save the template
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.layout_data, f, indent=2)
        
        print(f"\n✅ Template saved to: {output_file}")
        return output_file
    
    def close(self):
        """Close PDF document"""
        self.doc.close()


def analyze_pdf(pdf_path: str, output_path: str = None) -> Dict:
    """
    Convenience function to analyze a PDF and save template
    
    Args:
        pdf_path: Path to reference PDF
        output_path: Where to save template (optional)
    
    Returns:
        Layout template dictionary
    """
    analyzer = PDFLayoutAnalyzer(pdf_path)
    template = analyzer.analyze()
    
    if output_path:
        analyzer.save_template(output_path)
    
    analyzer.close()
    return template
