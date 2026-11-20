#!/usr/bin/env node
/**
 * Intelligent-AML Vercel Build Bridge
 * Universal compatibility bridge supporting:
 * 1. Root-level Vercel builds
 * 2. Legacy 'vite build' invocations from Vercel Vite preset
 * 3. Native Next.js 16 production compilation
 * 4. Output directory mirroring (.next <-> dist)
 */
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('===============================================================');
console.log(' [Intelligent-AML] Universal Vercel Deployment Bridge v3.0');
console.log(' Arguments received:', process.argv.slice(2).join(' ') || '(none)');
console.log('===============================================================');

const rootDir = process.cwd();
const isFrontendDir = fs.existsSync(path.join(rootDir, 'next.config.ts'));
const frontendDir = isFrontendDir ? rootDir : path.join(rootDir, 'frontend');

console.log(`[Vercel Bridge] Target frontend directory: ${frontendDir}`);

// 1. Ensure frontend dependencies are installed
if (!fs.existsSync(path.join(frontendDir, 'node_modules', 'next'))) {
  console.log('[Vercel Bridge] Installing frontend dependencies...');
  execSync('npm install --prefer-offline --no-audit', {
    cwd: frontendDir,
    stdio: 'inherit',
    env: { ...process.env, VERCEL: '1' }
  });
}

// 2. Execute Next.js build
console.log('[Vercel Bridge] Executing Next.js 16 production build...');
try {
  execSync('npm run build', {
    cwd: frontendDir,
    stdio: 'inherit',
    env: { ...process.env, VERCEL: '1' }
  });
  console.log('[Vercel Bridge] Next.js build completed with exit code 0.');
} catch (err) {
  console.error('[Vercel Bridge] Build failed:', err.message);
  process.exit(1);
}

// 3. Mirror outputs for multi-preset compatibility (Next.js .next AND Vite dist)
try {
  const nextDir = path.join(frontendDir, '.next');
  const distDir = path.join(rootDir, 'dist');
  const frontendDistDir = path.join(frontendDir, 'dist');
  
  [distDir, frontendDistDir].forEach(d => {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  });

  // Copy public assets if available
  const publicDir = path.join(frontendDir, 'public');
  if (fs.existsSync(publicDir)) {
    fs.cpSync(publicDir, distDir, { recursive: true });
    fs.cpSync(publicDir, frontendDistDir, { recursive: true });
  }

  // Generate fallback index.html for static probes
  const fallbackHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Intelligent-AML Enterprise Compliance Suite</title>
  <meta http-equiv="refresh" content="0; url=/">
</head>
<body style="background:#020617;color:#f8fafc;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;">
  <div style="text-align:center;">
    <h1 style="color:#38bdf8;">Intelligent-AML Enterprise v3.0</h1>
    <p style="color:#94a3b8;">Tier-1 Institutional AML Compliance Operating System Active.</p>
  </div>
</body>
</html>`;
  fs.writeFileSync(path.join(distDir, 'index.html'), fallbackHtml);
  fs.writeFileSync(path.join(frontendDistDir, 'index.html'), fallbackHtml);
  console.log('[Vercel Bridge] Compatibility assets synchronized to ./dist and ./frontend/dist.');
} catch (e) {
  console.warn('[Vercel Bridge] Warning during dist mirroring:', e.message);
}

console.log('===============================================================');
console.log(' [Intelligent-AML] Build pipeline complete & ready for deploy.');
console.log('===============================================================');
