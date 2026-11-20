#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('[Vercel Build Bridge] Intercepting legacy "vite build" invocation...');
console.log('[Vercel Build Bridge] Executing native Next.js 16 production build...');

const isFrontend = fs.existsSync(path.join(process.cwd(), 'next.config.ts'));
const targetDir = isFrontend ? process.cwd() : path.join(process.cwd(), 'frontend');

try {
  execSync('npm run build', {
    cwd: targetDir,
    stdio: 'inherit',
    env: { ...process.env, VERCEL: '1' }
  });
  console.log('[Vercel Build Bridge] Next.js build completed successfully.');
} catch (err) {
  console.error('[Vercel Build Bridge] Build failed:', err.message);
  process.exit(1);
}
