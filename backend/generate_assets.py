#!/usr/bin/env python3
"""
Generate placeholder frame images for all series and view types.
This creates PNG files with the naming convention: series-{series_id}-{view_type}.png
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# Frame series to generate images for
FRAME_SERIES = {
    "80": "Series 80",
    "86": "Series 86",
    "65": "Series 65",
    "135": "Series 135",
    "MD100H": "MD100H",
    "68": "Series 68",
    "58": "Series 58",
    "150": "Series 150",
    "4518": "Series 4518",
}

# View types to generate for each series
VIEW_TYPES = ["HEAD", "SILL", "JAMB"]

# Colors for each view type
VIEW_COLORS = {
    "HEAD": (52, 152, 219),      # Blue
    "SILL": (231, 76, 60),       # Red
    "JAMB": (46, 204, 113),      # Green
    "ELEVATION": (243, 156, 18), # Orange
    "PLAN": (155, 89, 182),      # Purple
}

# Image dimensions
IMAGE_WIDTH = 400
IMAGE_HEIGHT = 300
BORDER_WIDTH = 3

def create_placeholder_image(series_id: str, view_type: str) -> Image.Image:
    """Create a placeholder image for a frame series and view type."""
    color = VIEW_COLORS.get(view_type, (100, 100, 100))
    border_color = tuple(max(0, c - 50) for c in color)
    
    # Create image with border
    img = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw colored border
    draw.rectangle(
        [(0, 0), (IMAGE_WIDTH - 1, IMAGE_HEIGHT - 1)],
        outline=border_color,
        width=BORDER_WIDTH
    )
    
    # Draw inner colored rectangle
    inner_margin = 20
    draw.rectangle(
        [(inner_margin, inner_margin), 
         (IMAGE_WIDTH - inner_margin, IMAGE_HEIGHT - inner_margin)],
        fill=color,
        outline=border_color,
        width=2
    )
    
    # Add text
    try:
        # Try to use a system font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        title_font = font
    
    # Series name
    series_text = f"Series {series_id}"
    draw.text((IMAGE_WIDTH // 2 - 60, IMAGE_HEIGHT // 2 - 40), 
              series_text, fill='white', font=font)
    
    # View type
    view_text = view_type.upper()
    draw.text((IMAGE_WIDTH // 2 - 40, IMAGE_HEIGHT // 2 + 20), 
              view_text, fill='white', font=title_font)
    
    return img


def generate_all_images():
    """Generate all placeholder images."""
    # Get the static/frames directory
    static_dir = Path(__file__).parent / "static" / "frames"
    
    # Create directory if it doesn't exist
    static_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating images to: {static_dir}")
    print(f"{'Series':<12} {'View Type':<12} {'Status':<15}")
    print("-" * 40)
    
    generated_count = 0
    skipped_count = 0
    
    for series_id, series_name in FRAME_SERIES.items():
        for view_type in VIEW_TYPES:
            # Sanitize series_id: remove "Series " prefix if present
            clean_series_id = series_id.replace("Series ", "").strip()
            # Create filename using dash convention to match existing files
            filename = f"series-{clean_series_id}-{view_type.lower()}.png"
            filepath = static_dir / filename
            
            # Check if file already exists
            if filepath.exists():
                print(f"{series_id:<12} {view_type:<12} {'EXISTING':<15}")
                skipped_count += 1
                continue
            
            try:
                # Create and save image
                img = create_placeholder_image(series_id, view_type)
                img.save(str(filepath), 'PNG')
                print(f"{series_id:<12} {view_type:<12} {'CREATED':<15}")
                generated_count += 1
            except Exception as e:
                print(f"{series_id:<12} {view_type:<12} {'ERROR':<15} - {e}")
    
    print("-" * 40)
    print(f"Total generated: {generated_count}")
    print(f"Total existing:  {skipped_count}")
    print(f"Total images:    {generated_count + skipped_count}")
    
    # Also create thumbnail images (use HEAD view)
    print("\nGenerating thumbnails...")
    thumbnail_count = 0
    
    for series_id in FRAME_SERIES.keys():
        # Sanitize series_id: remove "Series " prefix if present
        clean_series_id = series_id.replace("Series ", "").strip()
        thumbnail_filename = f"series-{clean_series_id}-thumbnail.png"
        thumbnail_filepath = static_dir / thumbnail_filename
        
        if thumbnail_filepath.exists():
            continue
        
        try:
            # Use HEAD view as thumbnail (resized)
            img = create_placeholder_image(series_id, "HEAD")
            img_small = img.resize((150, 100))
            img_small.save(str(thumbnail_filepath), 'PNG')
            print(f"  {series_id}: THUMBNAIL CREATED")
            thumbnail_count += 1
        except Exception as e:
            print(f"  {series_id}: THUMBNAIL ERROR - {e}")
    
    print(f"\nThumbnails generated: {thumbnail_count}")
    print("\n✓ Image generation complete!")
    print(f"✓ All images saved to: {static_dir}")


if __name__ == "__main__":
    print("=" * 60)
    print("Raven Shop Frame Images Generator")
    print("=" * 60)
    print()
    generate_all_images()
