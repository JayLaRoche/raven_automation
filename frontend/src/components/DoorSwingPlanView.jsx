import React from 'react';
import PropTypes from 'prop-types';

/**
 * Human Figure component for plan view (Always on Exterior Side / Top)
 */
const Human = ({ cx, cy, humanStyle }) => (
  <g transform={`translate(${cx}, ${cy})`}>
    <circle cx="0" cy="-12" r="7" {...humanStyle} />
    <line x1="0" y1="-5" x2="0" y2="15" {...humanStyle} />
    <line x1="-10" y1="2" x2="10" y2="2" {...humanStyle} />
    <line x1="0" y1="15" x2="-8" y2="28" {...humanStyle} />
    <line x1="0" y1="15" x2="8" y2="28" {...humanStyle} />
  </g>
);

Human.propTypes = {
  cx: PropTypes.number.isRequired,
  cy: PropTypes.number.isRequired,
  humanStyle: PropTypes.object.isRequired
};

/**
 * Architectural Plan View of a Door.
 * Renders a 45-degree open door with swing arc and handing annotation.
 *
 * @param {string} handing - 'left' | 'right' (Default: 'right')
 * @param {boolean} isOutswing - true | false (Default: true)
 * @param {string} label - Optional text (e.g., 'Entry')
 */
const DoorSwingPlanView = ({ handing = 'right', isOutswing = true, label }) => {
  // SVG Config
  const size = 300; // Increased viewbox for breathing room
  const center = size / 2;
  const wallY = center + 40;
  const doorLength = 100;

  // 45-Degree Math
  const angleRad = (45 * Math.PI) / 180;
  const dx = doorLength * Math.cos(angleRad); // Horizontal offset
  const dy = doorLength * Math.sin(angleRad); // Vertical offset

  // Styles
  const styles = {
    wall: { stroke: 'black', strokeWidth: 4, strokeLinecap: 'square' },
    door: { stroke: 'black', strokeWidth: 4, fill: 'none' },
    arc: { stroke: 'black', strokeWidth: 1.5, fill: 'none', strokeDasharray: '6,4' },
    human: { stroke: 'black', strokeWidth: 2, fill: 'none' },
    text: { font: 'bold 24px Arial, sans-serif', textAnchor: 'middle', fill: 'black' }
  };

  // 1. Calculate Coordinates based on Handing/Swing
  const hingeX = handing === 'right' ? center + 40 : center - 40;

  // Door Tip Coordinates (45 degrees)
  // Right Hand: Subtract dx (move left). Left Hand: Add dx (move right).
  // Outswing: Subtract dy (move up). Inswing: Add dy (move down).
  const tipX = handing === 'right' ? hingeX - dx : hingeX + dx;
  const tipY = isOutswing ? wallY - dy : wallY + dy;

  // Arc Start Point (Door Closed Position)
  const arcStartX = handing === 'right' ? hingeX - doorLength : hingeX + doorLength;

  // Arc Sweep Flag (0 or 1)
  // Logic: RH+Out(0), LH+In(0) | RH+In(1), LH+Out(1)
  const sweepFlag =
    (handing === 'right' && isOutswing) || (handing === 'left' && !isOutswing) ? 0 : 1;

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center'
      }}
    >
      <svg width="100%" height="100%" viewBox={`0 0 ${size} ${size}`} preserveAspectRatio="xMidYMid meet">
        {/* Wall */}
        <line x1={20} y1={wallY} x2={size - 20} y2={wallY} {...styles.wall} />

        {/* Exterior Indicator */}
        <Human cx={center} cy={wallY - 80} humanStyle={styles.human} />

        {/* Door Panel */}
        <line x1={hingeX} y1={wallY} x2={tipX} y2={tipY} {...styles.door} />

        {/* Hinge Point */}
        <circle cx={hingeX} cy={wallY} r="4" fill="black" />

        {/* Swing Arc */}
        <path
          d={`M ${arcStartX} ${wallY} A ${doorLength} ${doorLength} 0 0 ${sweepFlag} ${tipX} ${tipY}`}
          {...styles.arc}
        />

        {/* Annotation (RH/LH) - Placed opposite to the swing */}
        <text x={center} y={isOutswing ? wallY + 40 : wallY - 60} {...styles.text}>
          {label || (handing === 'right' ? 'RH' : 'LH')}
        </text>
      </svg>
    </div>
  );
};
Human.propTypes = {
  cx: PropTypes.number.isRequired,
  cy: PropTypes.number.isRequired,
  humanStyle: PropTypes.object.isRequired
};

DoorSwingPlanView.propTypes = {
  handing: PropTypes.oneOf(['left', 'right']),
  isOutswing: PropTypes.bool,
  label: PropTypes.string
};

DoorSwingPlanView.defaultProps = {
  handing: 'right',
  isOutswing: true,
  label: null
};

export default DoorSwingPlanView;
