"""Frame series API endpoints with minimal dependencies."""

from fastapi import APIRouter
from pathlib import Path
import logging

router = APIRouter(prefix="/api/frames", tags=["frames"])
logger = logging.getLogger(__name__)

# Frame series configuration
FRAME_SERIES = {
    "80": {"name": "Series 80", "color": "#3498db"},
    "86": {"name": "Series 86", "color": "#3498db"},
    "65": {"name": "Series 65", "color": "#3498db"},
    "135": {"name": "Series 135", "color": "#3498db"},
    "MD100H": {"name": "MD100H", "color": "#3498db"},
    "68": {"name": "Series 68", "color": "#3498db"},
    "58": {"name": "Series 58", "color": "#3498db"},
    "150": {"name": "Series 150", "color": "#3498db"},
    "4518": {"name": "Series 4518", "color": "#3498db"},
}

# View types configuration
VIEW_TYPES = {
    "HEAD": {"label": "Head", "color": "#3498db", "required": True},
    "SILL": {"label": "Sill", "color": "#e74c3c", "required": True},
    "JAMB": {"label": "Jamb", "color": "#2ecc71", "required": False},
    "ELEVATION": {"label": "Elevation", "color": "#f39c12", "required": False},
    "PLAN": {"label": "Plan", "color": "#9b59b6", "required": False},
}


def get_assets_dir() -> Path:
    """Get path to static frames directory."""
    return Path(__file__).parent.parent / "static" / "frames"


def get_frame_library_dir() -> Path:
    """Get path to frame_library directory."""
    return Path(__file__).parent.parent / "frame_library"


def check_image_exists(series_id: str, view_type: str) -> bool:
    """Check if image file exists for series and view type in either location."""
    # Check standard naming in static/frames (series-86-head.png)
    assets_dir = get_assets_dir()
    SERIES_PREFIX = "Series "
    clean_series_id = series_id.replace(SERIES_PREFIX, "").strip()
    filename = f"series-{clean_series_id}-{view_type.lower()}.png"
    filepath = assets_dir / filename
    if filepath.exists():
        return True
    
    # Check variant naming in frame_library (Series_86_a.PNG)
    library_dir = get_frame_library_dir()
    # For variants like a, b, c, d check if any exist
    if view_type.lower() in ['head', 'sill', 'jamb', 'elevation', 'plan']:
        # These are standard views - check first variant
        variant_filename = f"Series_{clean_series_id}_a.PNG"
        variant_filepath = library_dir / variant_filename
        return variant_filepath.exists()
    
    return False


def get_image_url(series_id: str, view_type: str):
    """Get image URL for series and view type, checking both locations."""
    # Check standard naming in static/frames
    assets_dir = get_assets_dir()
    SERIES_PREFIX = "Series "
    clean_series_id = series_id.replace(SERIES_PREFIX, "").strip()
    filename = f"series-{clean_series_id}-{view_type.lower()}.png"
    filepath = assets_dir / filename
    
    if filepath.exists():
        # Return full URL with backend host for cross-origin requests
        return f"http://localhost:8000/static/frames/series-{clean_series_id}-{view_type.lower()}.png"
    
    # Check variant naming in frame_library
    library_dir = get_frame_library_dir()
    if view_type.lower() in ['head', 'sill', 'jamb', 'elevation', 'plan']:
        # Map view types to variant letters (use 'a' variant as default/thumbnail)
        variant_filename = f"Series_{clean_series_id}_a.PNG"
        variant_filepath = library_dir / variant_filename
        
        if variant_filepath.exists():
            # Return full URL with backend host for cross-origin requests
            return f"http://localhost:8000/frame-library/Series_{clean_series_id}_a.PNG"
    
    return None


def get_series_images(series_id: str):
    """Get all available images for a series."""
    return {
        view_type: {
            "view_type": view_type,
            "label": VIEW_TYPES[view_type]["label"],
            "color": VIEW_TYPES[view_type]["color"],
            "url": get_image_url(series_id, view_type),
            "exists": check_image_exists(series_id, view_type),
        }
        for view_type in VIEW_TYPES.keys()
    }


@router.get("/series")
def get_series():
    """Get list of available frame series."""
    try:
        return {"series": list(FRAME_SERIES.keys())}
    except Exception as e:
        logger.error(f"Error getting series: {e}")
        return {"series": list(FRAME_SERIES.keys())}


@router.get("/test")
def test_endpoint():
    """Simple test endpoint."""
    return {"status": "test works"}


@router.get("/series-with-images")
def get_series_with_images():
    """Get all series with their available images (multi-view support)."""
    try:
        series_list = []
        for series_id in FRAME_SERIES.keys():
            series_data = {
                "id": series_id,
                "name": FRAME_SERIES[series_id]["name"],
                "images": get_series_images(series_id),
                "thumbnail": get_image_url(series_id, "HEAD"),
            }
            series_list.append(series_data)
        
        return {
            "series": series_list,
            "view_types": VIEW_TYPES,
            "total": len(series_list),
        }
    except Exception as e:
        logger.error(f"Error getting series with images: {e}")
        return {
            "series": [
                {
                    "id": sid,
                    "name": FRAME_SERIES[sid]["name"],
                    "images": get_series_images(sid),
                    "thumbnail": get_image_url(sid, "HEAD"),
                }
                for sid in FRAME_SERIES.keys()
            ],
            "view_types": VIEW_TYPES,
            "total": len(FRAME_SERIES),
        }


@router.get("/view-types")
def get_view_types():
    """Get view type configuration."""
    return VIEW_TYPES


@router.get("/check-images")
def check_images():
    """Check which images exist and provide diagnostics."""
    try:
        total_possible = len(FRAME_SERIES) * len(VIEW_TYPES)
        existing_count = 0
        missing_list = []
        
        for series_id in FRAME_SERIES.keys():
            for view_type in VIEW_TYPES.keys():
                if check_image_exists(series_id, view_type):
                    existing_count += 1
                else:
                    missing_list.append(f"{series_id}-{view_type}")
        
        return {
            "total_possible": total_possible,
            "existing": existing_count,
            "missing": len(missing_list),
            "completion_percentage": round((existing_count / total_possible) * 100, 1),
            "missing_images": missing_list[:10],  # Return first 10 missing
        }
    except Exception as e:
        logger.error(f"Error checking images: {e}")
        return {
            "error": str(e),
            "total_possible": len(FRAME_SERIES) * len(VIEW_TYPES),
        }


@router.get("/series/{series_id}")
def get_series_detail(series_id: str):
    """Get details for a specific series including all available images."""
    if series_id not in FRAME_SERIES:
        return {"error": f"Series {series_id} not found"}, 404
    
    return {
        "id": series_id,
        "name": FRAME_SERIES[series_id]["name"],
        "images": get_series_images(series_id),
    }


@router.get("/series/{series_id}/images/{view_type}")
def get_series_image(series_id: str, view_type: str):
    """Get image info for specific series and view type."""
    if series_id not in FRAME_SERIES:
        return {"error": f"Series {series_id} not found"}, 404
    
    if view_type.upper() not in VIEW_TYPES:
        return {"error": f"View type {view_type} not found"}, 404
    
    view_upper = view_type.upper()
    return {
        "series_id": series_id,
        "view_type": view_upper,
        "label": VIEW_TYPES[view_upper]["label"],
        "color": VIEW_TYPES[view_upper]["color"],
        "url": get_image_url(series_id, view_upper),
        "exists": check_image_exists(series_id, view_upper),
    }


@router.get("/series/{series_id}/variants")
def get_series_variants(series_id: str):
    """Get all variant images (a, b, c, d, f, g) for a specific series from frame_library."""
    if series_id not in FRAME_SERIES:
        return {"error": f"Series {series_id} not found"}, 404
    
    library_dir = get_frame_library_dir()
    clean_series_id = series_id.replace("Series ", "").strip()
    
    variants = []
    variant_letters = ['a', 'b', 'c', 'd', 'f', 'g']
    
    for letter in variant_letters:
        filename = f"Series_{clean_series_id}_{letter}.PNG"
        filepath = library_dir / filename
        
        if filepath.exists():
            variants.append({
                "variant": letter,
                "url": f"http://localhost:8000/frame-library/{filename}",
                "filename": filename,
            })
    
    return {
        "series_id": series_id,
        "series_name": FRAME_SERIES[series_id]["name"],
        "variants": variants,
        "total": len(variants),
    }
