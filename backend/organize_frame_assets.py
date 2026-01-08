#!/usr/bin/env python3
"""
Frame Assets Organization Script
Organizes frame PNG files into the correct backend/static/frames/ directory structure

This script helps organize frame cross-section PNG files from any source directory
into the expected format for the drawing preview system.

Expected file naming conventions:
- Input: "86-head.png" or "series-86-head.png"
- Output: "backend/static/frames/series-86-head.png"

Supported frame sections: HEAD, SILL, JAMB
Supported series: 65, 80, 86, 135, and others
"""

import os
import shutil
from pathlib import Path
import re
from typing import Optional, Tuple

class FrameAssetOrganizer:
    """Organizes frame PNG assets into the correct directory structure"""
    
    def __init__(self, source_dir: str = "source_frames", output_dir: Optional[str] = None):
        """
        Initialize the organizer
        
        Args:
            source_dir: Directory containing source frame PNG files
            output_dir: Target directory (defaults to backend/static/frames)
        """
        self.source_dir = Path(source_dir)
        
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Default to backend/static/frames
            script_dir = Path(__file__).parent
            self.output_dir = script_dir / "static" / "frames"
        
        self.organized_count = 0
        self.skipped_count = 0
        self.error_count = 0
    
    def parse_filename(self, filename: str) -> Optional[Tuple[str, str]]:
        """
        Parse frame filename to extract series and section
        
        Args:
            filename: PNG filename to parse
            
        Returns:
            Tuple of (series, section) or None if invalid format
        """
        # Remove .png extension
        base = filename.replace('.png', '').replace('.PNG', '')
        
        # Pattern 1: "series-86-head" or "86-head"
        match = re.match(r'(?:series-)?(\d+)-([a-z]+)', base.lower())
        if match:
            series, section = match.groups()
            section = section.lower()
            
            # Validate section type
            if section in ['head', 'sill', 'jamb']:
                return series, section
        
        # Pattern 2: "Series_86_a" or "Series_86_b" (map letter to section)
        match = re.match(r'(?:series_)?(\d+)_([a-z])', base.lower())
        if match:
            series, letter = match.groups()
            # Map letters to sections: a=head, b=sill, c=jamb, d=thumbnail
            section_map = {'a': 'head', 'b': 'sill', 'c': 'jamb', 'd': 'thumbnail'}
            if letter in section_map:
                section = section_map[letter]
                return series, section
        
        return None
    
    def organize(self):
        """
        Organize all frame assets from source to output directory
        """
        print("\n" + "="*60)
        print("FRAME ASSETS ORGANIZATION SCRIPT")
        print("="*60)
        
        # Check source directory
        if not self.source_dir.exists():
            print(f"\n❌ Source directory not found: {self.source_dir}")
            print(f"   Creating: {self.source_dir}")
            self.source_dir.mkdir(parents=True, exist_ok=True)
            print(f"   Please add your frame PNG files to: {self.source_dir.absolute()}")
            print("\n   Expected file names:")
            print("   - 86-head.png  or  series-86-head.png")
            print("   - 86-sill.png  or  series-86-sill.png")
            print("   - 86-jamb.png  or  series-86-jamb.png")
            return
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📁 Source directory:  {self.source_dir.absolute()}")
        print(f"📁 Output directory:  {self.output_dir.absolute()}")
        
        # Find all PNG files
        png_files = list(self.source_dir.glob('*.png')) + list(self.source_dir.glob('*.PNG'))
        
        if not png_files:
            print(f"\n⚠️  No PNG files found in {self.source_dir}")
            return
        
        print(f"\n🔍 Found {len(png_files)} PNG file(s)")
        print("-" * 60)
        
        # Process each PNG file
        for png_file in png_files:
            self._process_file(png_file)
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"✅ Organized:  {self.organized_count} file(s)")
        print(f"⏭️  Skipped:    {self.skipped_count} file(s)")
        print(f"❌ Errors:     {self.error_count} file(s)")
        print("="*60 + "\n")
        
        if self.organized_count > 0:
            print("✅ Frame assets organized successfully!")
            print("   Restart the backend server to load frame images:")
            print("   uvicorn main:app --reload")
        
    def _process_file(self, file_path: Path):
        """Process a single frame PNG file"""
        
        # Parse filename
        result = self.parse_filename(file_path.name)
        
        if not result:
            print(f"⏭️  SKIPPED: {file_path.name}")
            print("   Reason: Invalid filename format")
            print("   Expected: 'series-86-head.png' or '86-head.png'")
            self.skipped_count += 1
            return
        
        series, section = result
        target_filename = f"series-{series}-{section}.png"
        target_path = self.output_dir / target_filename
        
        try:
            # Copy or overwrite file
            shutil.copy2(file_path, target_path)
            print(f"✅ ORGANIZED: {file_path.name}")
            print(f"   → {target_filename}")
            self.organized_count += 1
            
        except Exception as e:
            print(f"❌ ERROR:     {file_path.name}")
            print(f"   Reason: {str(e)}")
            self.error_count += 1

def main():
    """Main entry point"""
    import sys
    
    # Optional: accept source directory as argument
    source_dir = sys.argv[1] if len(sys.argv) > 1 else "source_frames"
    
    organizer = FrameAssetOrganizer(source_dir=source_dir)
    organizer.organize()

if __name__ == "__main__":
    main()
