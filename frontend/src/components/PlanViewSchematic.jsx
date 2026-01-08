import React from 'react';
import PropTypes from 'prop-types';

const PlanViewSchematic = ({ width = 200, type = 'fixed' }) => {
  // Styles for the schematic lines
  const styles = {
    glass: { stroke: 'black', strokeWidth: 2, fill: 'white' },
    swing: { stroke: 'black', strokeWidth: 1, fill: 'none', strokeDasharray: '4' },
    person: { stroke: 'black', strokeWidth: 2, fill: 'none' }
  };

  // Helper function to render person icon
  const renderPersonIcon = (x, y) => (
    <g key="person" transform={`translate(${x}, ${y}) scale(0.8)`}>
      <circle cx="10" cy="10" r="8" stroke="black" strokeWidth="2" fill="none" /> {/* Head */}
      <line x1="10" y1="18" x2="10" y2="40" stroke="black" strokeWidth="2" /> {/* Body */}
      <line x1="0" y1="25" x2="20" y2="25" stroke="black" strokeWidth="2" /> {/* Arms */}
    </g>
  );

  // Logic to choose the view based on "type"
  const renderSchematic = () => {
    const windowWidth = 140;
    const windowHeight = 30;
    const startX = 40;
    const startY = 25;

    switch (type.toLowerCase()) {
      case 'swing-left':
      case 'casement-left':
        return (
          <g>
            {/* Window frame */}
            <rect x={startX} y={startY} width={windowWidth} height={windowHeight} {...styles.glass} />
            {/* Hinge on left */}
            <rect x={startX} y={startY} width="6" height={windowHeight} fill="black" />
            {/* Sash line */}
            <line x1={startX + 6} y1={startY + windowHeight / 2} x2={startX + windowWidth} y2={startY + windowHeight / 2} stroke="black" strokeWidth="1" />
            {/* Swing arc (dashed) */}
            <path d={`M ${startX + 6} ${startY + windowHeight / 2} Q ${startX + windowWidth + 20} ${startY + windowHeight / 2} ${startX + windowWidth} ${startY}`} {...styles.swing} />
            {/* Swing direction arrow */}
            <polygon points={`${startX + windowWidth + 10},${startY + 5} ${startX + windowWidth + 5},${startY + 15} ${startX + windowWidth + 15},${startY + 15}`} fill="black" />
          </g>
        );
      case 'swing-right':
      case 'casement-right':
        return (
          <g>
            {/* Window frame */}
            <rect x={startX} y={startY} width={windowWidth} height={windowHeight} {...styles.glass} />
            {/* Hinge on right */}
            <rect x={startX + windowWidth - 6} y={startY} width="6" height={windowHeight} fill="black" />
            {/* Sash line */}
            <line x1={startX} y1={startY + windowHeight / 2} x2={startX + windowWidth - 6} y2={startY + windowHeight / 2} stroke="black" strokeWidth="1" />
            {/* Swing arc (dashed) */}
            <path d={`M ${startX + windowWidth - 6} ${startY + windowHeight / 2} Q ${startX - 20} ${startY + windowHeight / 2} ${startX} ${startY}`} {...styles.swing} />
            {/* Swing direction arrow */}
            <polygon points={`${startX - 10},${startY + 5} ${startX - 5},${startY + 15} ${startX - 15},${startY + 15}`} fill="black" />
          </g>
        );
      case 'slider':
      case 'sliding':
        return (
          <g>
            {/* Left pane (stationary) */}
            <rect x={startX} y={startY} width={windowWidth / 2} height={windowHeight} {...styles.glass} />
            {/* Right pane (sliding) */}
            <rect x={startX + windowWidth / 2} y={startY} width={windowWidth / 2} height={windowHeight} {...styles.glass} />
            {/* Vertical divider */}
            <line x1={startX + windowWidth / 2} y1={startY} x2={startX + windowWidth / 2} y2={startY + windowHeight} stroke="black" strokeWidth="1" />
            {/* Sliding arrow */}
            <line x1={startX + windowWidth / 2 + 10} y1={startY - 15} x2={startX + windowWidth - 10} y2={startY - 15} stroke="black" strokeWidth="2" />
            <polygon points={`${startX + windowWidth - 10},${startY - 15} ${startX + windowWidth - 15},${startY - 10} ${startX + windowWidth - 15},${startY - 20}`} fill="black" />
          </g>
        );
      case 'double-hung':
        return (
          <g>
            {/* Window frame */}
            <rect x={startX} y={startY} width={windowWidth} height={windowHeight} {...styles.glass} />
            {/* Horizontal divider */}
            <line x1={startX} y1={startY + windowHeight / 2} x2={startX + windowWidth} y2={startY + windowHeight / 2} stroke="black" strokeWidth="1" />
            {/* Up arrow (top sash) */}
            <line x1={startX + windowWidth + 15} y1={startY + 5} x2={startX + windowWidth + 15} y2={startY - 10} stroke="black" strokeWidth="2" />
            <polygon points={`${startX + windowWidth + 15},${startY - 10} ${startX + windowWidth + 10},${startY - 5} ${startX + windowWidth + 20},${startY - 5}`} fill="black" />
            {/* Down arrow (bottom sash) */}
            <line x1={startX + windowWidth + 15} y1={startY + windowHeight - 5} x2={startX + windowWidth + 15} y2={startY + windowHeight + 10} stroke="black" strokeWidth="2" />
            <polygon points={`${startX + windowWidth + 15},${startY + windowHeight + 10} ${startX + windowWidth + 10},${startY + windowHeight + 5} ${startX + windowWidth + 20},${startY + windowHeight + 5}`} fill="black" />
          </g>
        );
      case 'fixed':
      default:
        return (
          <g>
            {/* Window frame */}
            <rect x={startX} y={startY} width={windowWidth} height={windowHeight} {...styles.glass} />
            {/* "Fixed" text */}
            <text x={startX + windowWidth / 2} y={startY + windowHeight / 2 + 5} textAnchor="middle" fontSize="12" fontWeight="bold" fill="black">
              FIXED
            </text>
          </g>
        );
    }
  };

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        padding: '10px'
      }}
    >
      <svg width="100%" height="100%" viewBox="0 0 240 120" preserveAspectRatio="xMidYMid meet">
        {/* Render the Window Logic */}
        {renderSchematic()}

        {/* Render the Person standing "Inside" - positioned to the right */}
        <text x="200" y="25" textAnchor="middle" fontSize="10" fontStyle="italic" fill="#666">
          INSIDE
        </text>
        {renderPersonIcon(185, 50)}
      </svg>
    </div>
  );
};

PlanViewSchematic.propTypes = {
  width: PropTypes.number,
  type: PropTypes.string,
};

PlanViewSchematic.defaultProps = {
  width: 200,
  type: 'fixed',
};

export default PlanViewSchematic;
