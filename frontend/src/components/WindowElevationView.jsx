import React from 'react';
import PropTypes from 'prop-types';

/**
 * Arrow component for dimension annotations - Larger, more prominent
 */
const DimensionArrow = ({ x, y, rotation }) => (
  <polygon
    points="0,0 -45,22 -45,-22"
    transform={`translate(${x}, ${y}) rotate(${rotation})`}
    fill="black"
    stroke="black"
    strokeWidth="2"
    strokeLinejoin="miter"
  />
);

DimensionArrow.propTypes = {
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
  rotation: PropTypes.number.isRequired,
};

/**
 * A component that renders a technical elevation drawing of a window using SVG.
 * Designed to fit responsibly into any parent container (Canvas).
 */
const WindowElevationView = ({ 
  width = 609.6, 
  height = 1524, 
  gridCols = 2, 
  gridRows = 3 
}) => {
  // Helper function to convert millimeters to inches
  const toInches = (val) => `${(val / 25.4).toFixed(2)}"`;

  // Padding allows space for the dimension lines outside the frame
  const padding = 300;
  
  // The viewBox defines the "coordinate system" of the drawing
  const viewBoxWidth = width + (padding * 2);
  const viewBoxHeight = height + (padding * 2);

  const styles = {
    frame: { stroke: 'black', strokeWidth: 10, fill: 'none' }, 
    grid: { stroke: 'black', strokeWidth: 5, fill: 'none' }, // Where I can add window fill color (like a light blue)
    dimensionLine: { stroke: 'black', strokeWidth: 4 },
    dimensionText: { 
      fontFamily: 'Arial, sans-serif', 
      fontSize: 120, 
      fontWeight: 'bold',
      textAnchor: 'middle', 
      fill: 'black' 
    },
  };

  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg
        width="100%"
        height="100%"
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`}
        preserveAspectRatio="xMidYMid meet" 
        xmlns="http://www.w3.org/2000/svg"
        style={{ overflow: 'hidden' }}
      >
        {/* Main Window Frame */}
        <rect x={padding} y={padding} width={width} height={height} {...styles.frame} />

        {/* Heavy Outer Architectural Border with 12px Gap - More Pronounced */}
        <rect
          x={padding - 48}
          y={padding - 48}
          width={width + 96}
          height={height + 96}
          fill="none"
          stroke="#000"
          strokeWidth="13"
          style={{ pointerEvents: 'none' }}
        />

        {/* Grid Lines (Muntins) */}
        {Array.from({ length: gridCols - 1 }).map((_, i) => {
          const colNum = i + 1;
          const x = padding + (width / gridCols) * colNum;
          return <line key={`vertical-col-${colNum}`} x1={x} y1={padding} x2={x} y2={padding + height} {...styles.grid} />;
        })}
        {Array.from({ length: gridRows - 1 }).map((_, i) => {
          const rowNum = i + 1;
          const y = padding + (height / gridRows) * rowNum;
          return <line key={`horizontal-row-${rowNum}`} x1={padding} y1={y} x2={padding + width} y2={y} {...styles.grid} />;
        })}

        {/* Top Dimension (Width) */}
        <g transform={`translate(${padding}, ${padding - 150})`}>
          <line x1={0} y1={0} x2={width} y2={0} {...styles.dimensionLine} />
          <DimensionArrow x={0} y={0} rotation={180} />
          <DimensionArrow x={width} y={0} rotation={0} />
          <text x={width / 2} y={-35} {...styles.dimensionText}>{toInches(width)}</text>
        </g>

        {/* Left Dimension (Height) */}
        <g transform={`translate(${padding - 150}, ${padding})`}>
          <line x1={0} y1={0} x2={0} y2={height} {...styles.dimensionLine} />
          <DimensionArrow x={0} y={0} rotation={-90} />
          <DimensionArrow x={0} y={height} rotation={90} />
          <text 
            x={-40} 
            y={height / 2} 
            transform={`rotate(-90, -40, ${height / 2})`} 
            {...styles.dimensionText}
          >
            {toInches(height)}
          </text>
        </g>
      </svg>
    </div>
  );
};

WindowElevationView.propTypes = {
  width: PropTypes.number,
  height: PropTypes.number,
  gridCols: PropTypes.number,
  gridRows: PropTypes.number,
};

WindowElevationView.defaultProps = {
  width: 609.6,
  height: 1524,
  gridCols: 2,
  gridRows: 3,
};

export default WindowElevationView;
