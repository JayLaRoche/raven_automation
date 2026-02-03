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
 * Arrow pointing right for slider panels
 */
const SlideArrow = ({ x, y, width = 40, height = 20 }) => (
  <g>
    {/* Arrow shaft */}
    <line x1={x - width / 2} y1={y} x2={x + width / 2} y2={y} stroke="black" strokeWidth="3" />
    {/* Arrow head */}
    <polygon points={`${x + width / 2},${y} ${x + width / 2 - 12},${y - 8} ${x + width / 2 - 12},${y + 8}`} fill="black" stroke="black" strokeWidth="1" />
  </g>
);

SlideArrow.propTypes = {
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
  width: PropTypes.number,
  height: PropTypes.number,
};

/**
 * Handle rectangle for doors
 */
const DoorHandle = ({ x, y, width = 6, height = 40 }) => (
  <rect x={x - width / 2} y={y - height / 2} width={width} height={height} fill="black" stroke="black" strokeWidth="1" />
);

DoorHandle.propTypes = {
  x: PropTypes.number.isRequired,
  y: PropTypes.number.isRequired,
  width: PropTypes.number,
  height: PropTypes.number,
};

/**
 * A component that renders a technical elevation drawing of a window using SVG.
 * Designed to fit responsibly into any parent container (Canvas).
 * 
 * Enhanced to support:
 * - Door types with thicker thresholds (bottom frame)
 * - Slider doors with directional arrows
 * - Fixed panels with "F" label
 * - Hinged doors with handles
 */
const WindowElevationView = ({ parameters = {}, selectedFrameView }) => {
  // Extract values from parameters object and convert inches to mm
  const width = parameters.width ? parameters.width * 25.4 : 609.6
  const height = parameters.height ? parameters.height * 25.4 : 1524
  const gridCols = 2
  const gridRows = 3
  const productType = parameters.productType || ''
  const configuration = parameters.configuration || ''
  const panelCount = parameters.panelCount || 1
  const handleSide = parameters.handleSide || ''
  
  // Parse swing direction from configuration
  const swingDirection = configuration.includes('Left') ? 'Left' : 
                        configuration.includes('Right') ? 'Right' : 'Right'
  const isInswing = configuration.includes('Inswing')
  const isOutswing = configuration.includes('Outswing')
  
  // Helper function to convert millimeters to inches
  const toInches = (val) => `${(val / 25.4).toFixed(2)}"`;

  // Clamp panelCount between 1 and 6
  const validPanelCount = Math.min(Math.max(panelCount, 1), 6);
  
  // Calculate width per panel for mulling
  const panelWidth = width / validPanelCount;

  // Padding allows space for the dimension lines outside the frame
  const padding = 300;
  
  // The viewBox defines the "coordinate system" of the drawing
  const viewBoxWidth = width + (padding * 2);
  const viewBoxHeight = height + (padding * 2);

  // Determine if this is a door type
  const isDoorType = productType?.toLowerCase().includes('door') || productType?.toLowerCase().includes('slider');
  
  // Threshold line weight - thicker for doors
  const thresholdWeight = isDoorType ? 20 : 10;

  const styles = {
    frame: { stroke: 'black', strokeWidth: 10, fill: 'none' }, 
    grid: { stroke: 'black', strokeWidth: 5, fill: 'none' },
    dimensionLine: { stroke: 'black', strokeWidth: 4 },
    dimensionText: { 
      fontFamily: 'Arial, sans-serif', 
      fontSize: 120, 
      fontWeight: 'bold',
      textAnchor: 'middle', 
      fill: 'black' 
    },
    handleText: {
      fontFamily: 'Arial, sans-serif',
      fontSize: 80,
      fontWeight: 'bold',
      textAnchor: 'middle',
      textAlignmentBaseline: 'middle',
      fill: 'black'
    }
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
        {/* Main Window Frame - Single outer frame */}
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

        {/* Door Threshold - Thicker bottom frame for doors */}
        {isDoorType && (
          <rect 
            x={padding} 
            y={padding + height - thresholdWeight} 
            width={width} 
            height={thresholdWeight} 
            fill="black" 
          />
        )}

        {/* Panel Loop - Draws mullions and grid lines for each panel */}
        {Array.from({ length: validPanelCount }).map((_, panelIndex) => {
          const xOffset = padding + (panelIndex * panelWidth);
          
          return (
            <g key={`panel-${panelIndex}`}>
              {/* Mullion (vertical divider) - Only draw between panels, not after last one */}
              {panelIndex > 0 && (
                <line
                  x1={xOffset}
                  y1={padding}
                  x2={xOffset}
                  y2={padding + height}
                  stroke="black"
                  strokeWidth="10"
                  fill="none"
                />
              )}

              {/* Grid Lines (Muntins) for this panel */}
              {/* Vertical grid lines within panel */}
              {Array.from({ length: gridCols - 1 }).map((_, i) => {
                const colNum = i + 1;
                const x = xOffset + (panelWidth / gridCols) * colNum;
                return (
                  <line
                    key={`panel-${panelIndex}-vertical-col-${colNum}`}
                    x1={x}
                    y1={padding}
                    x2={x}
                    y2={padding + height - (isDoorType ? thresholdWeight : 0)}
                    {...styles.grid}
                  />
                );
              })}

              {/* Horizontal grid lines within panel */}
              {Array.from({ length: gridRows - 1 }).map((_, i) => {
                const rowNum = i + 1;
                const y = padding + (height / gridRows) * rowNum;
                return (
                  <line
                    key={`panel-${panelIndex}-horizontal-row-${rowNum}`}
                    x1={xOffset}
                    y1={y}
                    x2={xOffset + panelWidth}
                    y2={y}
                    {...styles.grid}
                  />
                );
              })}
            </g>
          );
        })}

        {/* Slider Panel Arrows and Fixed Labels - Distributed across panels */}
        {productType?.toLowerCase().includes('slider') && (
          <>
            {Array.from({ length: validPanelCount }).map((_, panelIndex) => {
              const xOffset = padding + (panelIndex * panelWidth);
              
              return (
                <g key={`panel-${panelIndex}-slider`}>
                  {/* For each column within the panel */}
                  {Array.from({ length: gridCols }).map((_, colIdx) => {
                    const colWidth = panelWidth / gridCols;
                    const panelCenterX = xOffset + (colIdx + 0.5) * colWidth;
                    const panelCenterY = padding + height / 2;
                    
                    const isMoving = colIdx === 0;
                    const uniqueKey = `panel-${panelIndex}-col-${colIdx}-${isMoving ? 'slider' : 'fixed'}`;
                    
                    return isMoving ? (
                      <SlideArrow
                        key={uniqueKey}
                        x={panelCenterX}
                        y={panelCenterY}
                        width={80}
                      />
                    ) : (
                      <text
                        key={uniqueKey}
                        x={panelCenterX}
                        y={panelCenterY}
                        {...styles.handleText}
                        dy="0.3em"
                      >
                        F
                      </text>
                    );
                  })}
                </g>
              );
            })}
          </>
        )}

        {/* Door Handles - For all door types based on swing direction */}
        {isDoorType && !productType?.toLowerCase().includes('slider') && (
          <>
            {Array.from({ length: validPanelCount }).map((_, panelIndex) => {
              const xOffset = padding + (panelIndex * panelWidth);
              
              // Determine handle position
              // Priority: 1) User-selected handleSide, 2) Swing direction from configuration
              const effectiveHandleSide = handleSide || swingDirection;
              const handleX = effectiveHandleSide === 'Left' ? xOffset + 60 : xOffset + panelWidth - 60;
              
              return (
                <g key={`panel-${panelIndex}-handle-group`}>
                  {/* Door Handle */}
                  <DoorHandle
                    key={`panel-${panelIndex}-handle`}
                    x={handleX}
                    y={padding + height / 2}
                    width={10}
                    height={70}
                  />
                  
                  {/* Swing Direction Indicator (Arc) */}
                  {(isInswing || isOutswing) && (
                    <path
                      d={swingDirection === 'Left' 
                        ? `M ${xOffset + 40} ${padding + height - thresholdWeight - 20} Q ${xOffset + 40} ${padding + height - thresholdWeight - 120}, ${xOffset + 140} ${padding + height - thresholdWeight - 120}`
                        : `M ${xOffset + panelWidth - 40} ${padding + height - thresholdWeight - 20} Q ${xOffset + panelWidth - 40} ${padding + height - thresholdWeight - 120}, ${xOffset + panelWidth - 140} ${padding + height - thresholdWeight - 120}`
                      }
                      stroke="black"
                      strokeWidth="3"
                      fill="none"
                      strokeDasharray="8,4"
                    />
                  )}
                </g>
              );
            })}
          </>
        )}

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
  parameters: PropTypes.shape({
    series: PropTypes.string,
    width: PropTypes.number,
    height: PropTypes.number,
    productType: PropTypes.string,
    glassType: PropTypes.string,
    frameColor: PropTypes.string,
    configuration: PropTypes.string,
    itemNumber: PropTypes.string,
    panelCount: PropTypes.number,
  }),
  selectedFrameView: PropTypes.oneOf(['head', 'sill', 'jamb']),
};

WindowElevationView.defaultProps = {
  parameters: {},
  selectedFrameView: 'head',
};

export default WindowElevationView;
