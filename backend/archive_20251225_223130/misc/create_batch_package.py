#!/usr/bin/env python3
"""
Create a batch PDF package combining all generated drawings
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os
from pathlib import Path
from datetime import datetime
import glob

try:
    from PyPDF2 import PdfMerger
except ImportError:
    print("Installing PyPDF2...")
    os.system("pip install PyPDF2")
    from PyPDF2 import PdfMerger

def create_cover_page(filename, project_name, customer_name, item_count):
    """Create a professional cover page"""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=32,
        textColor=colors.HexColor('#1a3a52'),
        spaceAfter=6,
        alignment=1,  # center
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=18,
        textColor=colors.HexColor('#333333'),
        spaceAfter=24,
        alignment=1,
        fontName='Helvetica'
    )
    
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#555555'),
        spaceAfter=12,
        alignment=0
    )
    
    # Add spacing
    story.append(Spacer(1, 1.5*inch))
    
    # Company name
    story.append(Paragraph("RAVEN CUSTOM GLASS", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Subtitle
    story.append(Paragraph("Professional Shop Drawing Package", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Project info
    info_data = [
        ['Project:', project_name],
        ['Customer:', customer_name],
        ['Date Generated:', datetime.now().strftime("%B %d, %Y")],
        ['Total Items:', str(item_count)],
        ['Document Type:', 'Technical Drawing Package'],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 12),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 12),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a3a52')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#333333')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 1*inch))
    
    # Footer info
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#999999'),
        alignment=1
    )
    
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(
        "This document contains professional technical drawings for window and door products. "
        "All dimensions are in inches unless otherwise noted. "
        "For installation, refer to manufacturer specifications.",
        footer_style
    ))
    
    doc.build(story)
    return filename

def create_toc_page(filename, pdf_files):
    """Create a table of contents page"""
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a3a52'),
        spaceAfter=20,
        fontName='Helvetica-Bold'
    )
    
    # Title
    story.append(Paragraph("TABLE OF CONTENTS", title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Build TOC table
    toc_data = [['Item #', 'Product', 'Dimensions', 'File']]
    
    for idx, pdf_file in enumerate(pdf_files, 1):
        basename = os.path.basename(pdf_file)
        # Parse filename: updated-Evergreen-Cr_Window-ITEM-23_ELEV.pdf
        parts = basename.replace('.pdf', '').split('_')
        if len(parts) >= 2:
            product_type = parts[1].split('-')[0]  # Window or Door
            item_num = parts[1].split('-')[1]      # Item number
            dimensions = "36\" x 48\""  # Default from sheet
        else:
            product_type = "Window"
            item_num = str(idx)
            dimensions = "36\" x 48\""
        
        toc_data.append([
            str(idx),
            f"{product_type} {item_num}",
            dimensions,
            f"Page {idx + 1}"
        ])
    
    toc_table = Table(toc_data, colWidths=[0.8*inch, 1.5*inch, 1.5*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a52')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(toc_table)
    
    doc.build(story)
    return filename

def merge_pdfs(output_filename, input_pdfs):
    """Merge multiple PDFs into one"""
    merger = PdfMerger()
    
    valid_pdfs = []
    for pdf in input_pdfs:
        if os.path.exists(pdf):
            try:
                merger.append(pdf)
                valid_pdfs.append(pdf)
            except Exception as e:
                print(f"⚠ Skipping corrupted PDF: {os.path.basename(pdf)} - {str(e)[:50]}")
    
    if valid_pdfs:
        merger.write(output_filename)
        merger.close()
        return output_filename
    else:
        print("❌ No valid PDFs to merge")
        return None

def create_batch_package(drawings_dir='./drawings', output_name='Evergreen_Creek_Batch_Package'):
    """Create a complete batch PDF package"""
    
    print("📦 Creating Batch PDF Package")
    print("=" * 60)
    
    # Find all PDFs
    pdf_files = sorted(glob.glob(os.path.join(drawings_dir, 'updated-Evergreen-Cr_Window-*.pdf')))
    
    if not pdf_files:
        print("❌ No PDF files found in", drawings_dir)
        return None
    
    print(f"✓ Found {len(pdf_files)} drawings")
    
    # Create temporary files for cover and TOC
    cover_file = os.path.join(drawings_dir, '_cover.pdf')
    toc_file = os.path.join(drawings_dir, '_toc.pdf')
    
    print(f"✓ Creating cover page...")
    create_cover_page(
        cover_file,
        project_name='updated Evergreen Creek',
        customer_name='Evergreen Creek',
        item_count=len(pdf_files)
    )
    
    print(f"✓ Creating table of contents...")
    create_toc_page(toc_file, pdf_files)
    
    # Merge all PDFs
    all_files = [cover_file, toc_file] + pdf_files
    output_path = os.path.join(drawings_dir, f'{output_name}.pdf')
    
    print(f"✓ Merging {len(all_files)} documents...")
    result = merge_pdfs(output_path, all_files)
    
    if not result:
        print("❌ Failed to merge PDFs")
        return None
    
    # Get file size
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # Convert to MB
    
    print("=" * 60)
    print(f"✓ BATCH PACKAGE CREATED SUCCESSFULLY!")
    print(f"\n📄 Output File: {output_name}.pdf")
    print(f"📊 File Size: {file_size:.2f} MB")
    print(f"📑 Total Pages: {len(all_files) + len(pdf_files) - 2}")  # Approximate
    print(f"📋 Contents:")
    print(f"   • Cover Page")
    print(f"   • Table of Contents")
    print(f"   • {len(pdf_files)} Professional Drawings")
    print(f"\n📁 Location: {output_path}")
    
    # Cleanup temporary files
    try:
        os.remove(cover_file)
        os.remove(toc_file)
    except:
        pass
    
    return output_path

if __name__ == '__main__':
    package = create_batch_package()
    
    if package and os.path.exists(package):
        print(f"\n✅ Ready for distribution!")
        print(f"   - Print direct to PDF printers")
        print(f"   - Email to customers")
        print(f"   - Archive in project folders")
