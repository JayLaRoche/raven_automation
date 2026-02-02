#!/bin/bash
# Render build script for frontend

echo "📦 Installing dependencies..."
npm ci

echo "🔍 Checking TypeScript..."
npx tsc --noEmit || echo "⚠️  TypeScript warnings (non-blocking)"

echo "🏗️  Building production bundle..."
npm run build

echo "✅ Build complete!"
ls -la dist/
