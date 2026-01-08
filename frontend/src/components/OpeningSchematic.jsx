import React from 'react'

/**
 * OpeningSchematic Component
 *
 * Renders a schematic diagram showing how a window or door opens based on its type.
 * Includes visual representations (human figure, swing arc, slide indicators, etc.)
 *
 * @param {string} type - Opening type: 'casement', 'fixed', 'double-hung', 'sliding', 'patio-door', 'awning'
 * @param {number} width - Width of the schematic in pixels (default: 200)
 * @param {number} height - Height of the schematic in pixels (default: 150)
 */
export default function OpeningSchematic({ type = 'fixed', width = 200, height = 150 }) {
  const svgProps = {
    width,
    height,
    viewBox: `0 0 ${width} ${height}`,
    xmlns: 'http://www.w3.org/2000/svg',
    style: { border: '1px solid #ccc', backgroundColor: '#f9f9f9' },
  }

  // Fixed Window - Just a rectangle with no movement
  if (type === 'fixed' || type === 'FIXED') {
    return (
      <svg {...svgProps}>
        <rect x="20" y="20" width="160" height="110" fill="none" stroke="#000" strokeWidth="2" />
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          FIXED
        </text>
      </svg>
    )
  }

  // Casement Window - Side-hinged with swing arc
  if (type === 'casement' || type === 'CASEMENT') {
    return (
      <svg {...svgProps}>
        {/* Frame */}
        <rect x="20" y="20" width="160" height="110" fill="none" stroke="#000" strokeWidth="2" />

        {/* Sash/Panel (left side) */}
        <rect x="25" y="25" width="75" height="100" fill="#e3f2fd" stroke="#000" strokeWidth="1.5" />

        {/* Hinge line (right edge of sash) */}
        <line x1="100" y1="25" x2="100" y2="125" stroke="#666" strokeWidth="2" strokeDasharray="5,5" />

        {/* Swing arc */}
        <path
          d="M 100 75 A 50 50 0 0 0 150 75"
          fill="none"
          stroke="#2196F3"
          strokeWidth="2"
          strokeDasharray="4,4"
          markerEnd="url(#arrowhead)"
        />

        {/* Arrow */}
        <defs>
          <marker id="arrowhead" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#2196F3" />
          </marker>
        </defs>

        {/* Label */}
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          CASEMENT
        </text>
      </svg>
    )
  }

  // Double-Hung Window - Vertically sliding sashes
  if (type === 'double-hung' || type === 'DOUBLE-HUNG') {
    return (
      <svg {...svgProps}>
        {/* Frame */}
        <rect x="20" y="20" width="160" height="110" fill="none" stroke="#000" strokeWidth="2" />

        {/* Top sash */}
        <rect x="25" y="25" width="150" height="40" fill="#e3f2fd" stroke="#000" strokeWidth="1.5" />

        {/* Bottom sash */}
        <rect x="25" y="65" width="150" height="50" fill="#b3e5fc" stroke="#000" strokeWidth="1.5" />

        {/* Horizontal divider line */}
        <line x1="25" y1="65" x2="175" y2="65" stroke="#999" strokeWidth="1" strokeDasharray="3,3" />

        {/* Up/down arrows */}
        <path d="M 180 40 L 190 30 L 185 35" fill="none" stroke="#2196F3" strokeWidth="1.5" />
        <path d="M 180 85 L 190 95 L 185 90" fill="none" stroke="#2196F3" strokeWidth="1.5" />

        {/* Label */}
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          DOUBLE-HUNG
        </text>
      </svg>
    )
  }

  // Sliding Window - Horizontal sliding
  if (type === 'sliding' || type === 'SLIDING') {
    return (
      <svg {...svgProps}>
        {/* Frame */}
        <rect x="20" y="20" width="160" height="110" fill="none" stroke="#000" strokeWidth="2" />

        {/* Fixed pane (left) */}
        <rect x="25" y="25" width="70" height="100" fill="#c8e6c9" stroke="#000" strokeWidth="1.5" />

        {/* Sliding pane (middle) */}
        <rect x="100" y="25" width="70" height="100" fill="#e3f2fd" stroke="#000" strokeWidth="1.5" />

        {/* Vertical divider */}
        <line x1="95" y1="25" x2="95" y2="125" stroke="#999" strokeWidth="1" strokeDasharray="3,3" />

        {/* Left/right arrows */}
        <path d="M 75 130 L 65 140 L 70 135" fill="none" stroke="#2196F3" strokeWidth="1.5" />
        <path d="M 140 130 L 150 140 L 145 135" fill="none" stroke="#2196F3" strokeWidth="1.5" />

        {/* Label */}
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          SLIDING
        </text>
      </svg>
    )
  }

  // Patio Door - Sliding with larger frame
  if (type === 'patio-door' || type === 'PATIO-DOOR') {
    return (
      <svg {...svgProps}>
        {/* Frame */}
        <rect x="10" y="20" width="180" height="110" fill="none" stroke="#000" strokeWidth="3" />

        {/* Fixed panel (left) */}
        <rect x="15" y="25" width="80" height="100" fill="#c8e6c9" stroke="#000" strokeWidth="2" />

        {/* Sliding panel (right) */}
        <rect x="100" y="25" width="85" height="100" fill="#e3f2fd" stroke="#000" strokeWidth="2" />

        {/* Divider */}
        <line x1="95" y1="25" x2="95" y2="125" stroke="#999" strokeWidth="1.5" strokeDasharray="4,4" />

        {/* Sliding direction indicator */}
        <path d="M 100 135 L 130 135" stroke="#2196F3" strokeWidth="2" markerEnd="url(#arrowhead2)" />

        <defs>
          <marker id="arrowhead2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
            <polygon points="0 0, 10 3, 0 6" fill="#2196F3" />
          </marker>
        </defs>

        {/* Label */}
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          PATIO DOOR
        </text>
      </svg>
    )
  }

  // Awning Window - Top-hinged outward opening
  if (type === 'awning' || type === 'AWNING') {
    return (
      <svg {...svgProps}>
        {/* Frame */}
        <rect x="20" y="20" width="160" height="110" fill="none" stroke="#000" strokeWidth="2" />

        {/* Sash/Panel (hinged at top) */}
        <polygon points="25,30 175,30 150,85 50,85" fill="#e3f2fd" stroke="#000" strokeWidth="1.5" />

        {/* Hinge line (top edge) */}
        <line x1="25" y1="30" x2="175" y2="30" stroke="#666" strokeWidth="2" />

        {/* Opening arc (outward) */}
        <path
          d="M 100 30 A 60 60 0 0 0 100 -30"
          fill="none"
          stroke="#2196F3"
          strokeWidth="2"
          strokeDasharray="4,4"
        />

        {/* Label */}
        <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="12" fill="#666">
          AWNING
        </text>
      </svg>
    )
  }

  // Unknown type - placeholder
  return (
    <svg {...svgProps}>
      <rect x="20" y="20" width="160" height="110" fill="none" stroke="#999" strokeWidth="2" strokeDasharray="5,5" />
      <text x={width / 2} y={height / 2} textAnchor="middle" fontSize="12" fill="#999">
        Unknown Type
      </text>
      <text x={width / 2} y={height - 10} textAnchor="middle" fontSize="10" fill="#ccc">
        {type || 'N/A'}
      </text>
    </svg>
  )
}
