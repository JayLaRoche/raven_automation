/**
 * Plan View Image Mapping Utility
 * Maps product types and configurations to exact O-Icon_library filenames
 * 
 * Images are served from: {VITE_API_URL}/static/O-Icon_library/
 * IMPORTANT: Filenames use uppercase .PNG extension
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const BASE_URL = `${API_URL}/static/O-Icon_library`;

/**
 * Get the Plan View image URL for a given product type and configuration
 * Uses switch logic to map to exact filenames in O-Icon_library
 * 
 * @param productType - The selected product type (e.g., 'Casement', 'Hinged Door')
 * @param configuration - The configuration string (e.g., 'Left Inswing', 'Right', etc.)
 * @returns The full image URL string or null if no image is available
 */
export function getPlanViewImage(productType: string | undefined, configuration: string = ''): string | null {
  if (!productType) return null;

  // Parse configuration to extract handing and swing
  const isLeft = configuration.includes('Left');
  const isRight = configuration.includes('Right');
  const isInswing = configuration.includes('Inswing');
  const isOutswing = configuration.includes('Outswing');

  let filename: string | null = null;

  // Use switch to map to exact O-Icon_library filenames (uppercase .PNG extension)
  switch (productType) {
    // WINDOWS
    case 'Fixed':
      filename = 'W-Fixed_O.PNG';
      break;

    case 'Casement':
      if (isLeft) {
        filename = 'W-Left_Casement_O.PNG';
      } else if (isRight) {
        filename = 'W-Right_Casement_O.PNG';
      }
      break;

    case 'Double Casement':
      filename = 'W-Double_Casement_O.PNG';
      break;

    case 'Slider':
      filename = 'W-Slider_O.PNG'; // Add if available in your library
      break;

    case 'Hung':
      filename = 'W-Hung_O.PNG'; // Add if available in your library
      break;

    case 'Double Hung':
      filename = 'W-Double_Hung_O.PNG'; // Add if available in your library
      break;

    case 'Accordian':
      filename = 'W-Accordian_O.PNG'; // Add if available in your library
      break;

    case 'Awning':
      filename = 'W-Awning_O.PNG'; // Add if available in your library
      break;

    case 'Curtain Wall':
      filename = 'W-Curtain_Wall_O.PNG'; // Add if available in your library
      break;

    // DOORS
    case 'Double Door (French)':
      // CRITICAL: French doors use the same image as Double Casement windows
      filename = 'W-Double_Casement_O.PNG';
      break;

    case 'Hinged Door':
      if (isLeft && isInswing) {
        filename = 'D-Hinged_Door_IN_L.PNG';
      } else if (isRight && isInswing) {
        filename = 'D-Hinged_Door_IN_R.PNG';
      } else if (isLeft && isOutswing) {
        filename = 'D-Hinged_Door_OUT_L.PNG';
      } else if (isRight && isOutswing) {
        filename = 'D-Hinged_Door_OUT_R.PNG';
      }
      break;

    case '2 Panel Slider':
      filename = 'D-2_Panel_Slider.PNG';
      break;

    case '3 Track 3 Panel':
      filename = 'D-3_Track_3_Panel_Slider.PNG'; // Add if available in your library
      break;

    case '4 Track 4 Panel':
      filename = 'D-4_Track_4_Panel_Slider.PNG';
      break;

    case '4 Panel meet in the middle':
      filename = 'D-4_Panel_Meet_Middle.PNG'; // Add if available in your library
      break;

    default:
      return null;
  }

  // Return full URL if filename exists
  return filename ? `${BASE_URL}/${filename}` : null;
}

/**
 * Check if a product type has a plan view image available
 * @param productType - The selected product type
 * @param configuration - The configuration string
 * @returns true if an image URL is available
 */
export function hasPlanViewImage(productType: string | undefined, configuration: string = ''): boolean {
  return getPlanViewImage(productType, configuration) !== null;
}
