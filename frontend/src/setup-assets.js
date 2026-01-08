#!/usr/bin/env node

/**
 * Asset Setup Helper
 *
 * This script helps set up the directory structure and generate placeholder SVGs
 * for component registry assets.
 *
 * Usage: node setup-assets.js
 */

const fs = require('fs')
const path = require('path')

const ASSET_DIR = path.join(__dirname, '..', '..', 'public', 'assets', 'profiles')

// Create directory if it doesn't exist
if (!fs.existsSync(ASSET_DIR)) {
  fs.mkdirSync(ASSET_DIR, { recursive: true })
  console.log(`✓ Created assets directory: ${ASSET_DIR}`)
} else {
  console.log(`✓ Assets directory exists: ${ASSET_DIR}`)
}

/**
 * Generate a placeholder profile SVG
 */
function generateProfileSVG(title, series, type) {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300">
  <defs>
    <style>
      .frame { stroke: #000; stroke-width: 2; fill: none; }
      .profile { stroke: #333; stroke-width: 1.5; fill: #e3f2fd; }
      .label { font-family: Arial, sans-serif; font-size: 14px; fill: #333; }
      .title { font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; fill: #000; }
    </style>
  </defs>

  <!-- Background -->
  <rect width="400" height="300" fill="#fafafa"/>

  <!-- Frame -->
  <rect class="frame" x="20" y="20" width="360" height="260"/>

  <!-- Profile Section -->
  <rect class="profile" x="50" y="60" width="300" height="160"/>

  <!-- Grid lines to show profile depth -->
  <line x1="80" y1="60" x2="80" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="110" y1="60" x2="110" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="140" y1="60" x2="140" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="170" y1="60" x2="170" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="200" y1="60" x2="200" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="230" y1="60" x2="230" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="260" y1="60" x2="260" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="290" y1="60" x2="290" y2="220" stroke="#ccc" stroke-width="0.5"/>
  <line x1="320" y1="60" x2="320" y2="220" stroke="#ccc" stroke-width="0.5"/>

  <!-- Horizontal lines -->
  <line x1="50" y1="80" x2="350" y2="80" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="100" x2="350" y2="100" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="120" x2="350" y2="120" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="140" x2="350" y2="140" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="160" x2="350" y2="160" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="180" x2="350" y2="180" stroke="#ccc" stroke-width="0.5"/>
  <line x1="50" y1="200" x2="350" y2="200" stroke="#ccc" stroke-width="0.5"/>

  <!-- Dimension arrow -->
  <g>
    <line x1="40" y1="240" x2="360" y2="240" stroke="#000" stroke-width="1"/>
    <polygon points="40,240 45,235 45,245" fill="#000"/>
    <polygon points="360,240 355,235 355,245" fill="#000"/>
    <text class="label" x="200" y="260" text-anchor="middle">Width →</text>
  </g>

  <!-- Title and info -->
  <text class="title" x="200" y="40" text-anchor="middle">${title}</text>
  <text class="label" x="200" y="280" text-anchor="middle" font-size="12">Series ${series} - ${type} (Placeholder)</text>
</svg>
`
}

/**
 * Frame series to generate
 */
const frameSeries = ['65', '86', '135', '4518']
const profileTypes = ['head', 'sill', 'jamb']

let fileCount = 0

frameSeries.forEach(series => {
  profileTypes.forEach(type => {
    const filename = `series${series}-${type}.svg`
    const filepath = path.join(ASSET_DIR, filename)

    // Only create if doesn't exist
    if (!fs.existsSync(filepath)) {
      const svg = generateProfileSVG(
        `${type.toUpperCase()} Profile`,
        series,
        type.toUpperCase()
      )
      fs.writeFileSync(filepath, svg)
      console.log(`✓ Created: ${filename}`)
      fileCount++
    } else {
      console.log(`⊘ Already exists: ${filename}`)
    }
  })
})

console.log(`\n✓ Setup complete! Created ${fileCount} placeholder SVGs.`)
console.log(`\nAssets are located in: ${ASSET_DIR}`)
console.log(`\nNext steps:`)
console.log('1. Replace placeholder SVGs with actual CAD drawings')
console.log('2. Update ComponentRegistry.js with correct file paths if needed')
console.log('3. Verify profile display components render correctly')
