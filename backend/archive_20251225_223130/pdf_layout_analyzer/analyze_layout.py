#!/usr/bin/env python3
"""
PDF Layout Analyzer - Command Line Tool
Analyzes reference PDFs and generates visual layout templates

Usage:
    python analyze_layout.py path/to/reference.pdf
    python analyze_layout.py path/to/reference.pdf --output templates/custom.json
    python analyze_layout.py --create-default templates/default.json
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.pdf_layout_analyzer import PDFLayoutAnalyzer, analyze_pdf
from app.services.visual_template_generator import create_default_template


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze PDF layout and generate visual templates'
    )
    parser.add_argument(
        'pdf_path',
        nargs='?',
        help='Path to reference PDF file'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output path for template JSON (default: templates/<pdf_name>.json)'
    )
    parser.add_argument(
        '--create-default',
        action='store_true',
        help='Create a default template instead of analyzing a PDF'
    )
    
    args = parser.parse_args()
    
    # Create default template
    if args.create_default:
        output_path = args.output or 'templates/default_layout.json'
        create_default_template(output_path)
        return 0
    
    # Analyze PDF
    if not args.pdf_path:
        parser.print_help()
        return 1
    
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"❌ Error: PDF file not found: {pdf_path}")
        return 1
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_name = pdf_path.stem + '_layout.json'
        output_path = Path('templates') / output_name
    
    print(f"\n📄 Analyzing PDF: {pdf_path.name}")
    print(f"📁 Output: {output_path}")
    print()
    
    try:
        # Run analysis
        template = analyze_pdf(str(pdf_path), str(output_path))
        
        print("\n" + "=" * 70)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 70)
        print(f"\nTemplate: {template['template_name']}")
        print(f"Page Format: {template['page']['format']}")
        print(f"Zones: {len(template['zones'])}")
        print(f"Visual Elements: {len(template['visual_elements'])}")
        
        print("\nZone Layout:")
        for zone_name, zone_config in template['zones'].items():
            print(f"  • {zone_name}: {zone_config['width_percent']:.1f}% width")
        
        print(f"\n✅ Template saved to: {output_path}")
        print("\nNext steps:")
        print("1. Review the generated template JSON")
        print("2. Edit if needed (it's human-readable)")
        print("3. Use with: ProfessionalDrawingGenerator(template='path/to/template.json')")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error analyzing PDF: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
