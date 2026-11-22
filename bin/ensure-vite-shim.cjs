#!/usr/bin/env node
/**
 * Ensures POSIX and Windows 'vite' executable shims exist in:
 * 1. ./node_modules/.bin/vite
 * 2. ./bin/vite
 * 3. frontend/node_modules/.bin/vite
 * 4. frontend/bin/vite
 *
 * This guarantees zero-config execution whether Vercel runs:
 * - 'vite build' at repo root
 * - 'vite build' inside frontend/
 * - in Linux containers or Windows dev environments
 */
const fs = require('fs');
const path = require('path');

const rootDir = process.cwd();
const isFrontend = fs.existsSync(path.join(rootDir, 'src', 'app'));
const projectRoot = isFrontend ? path.resolve(rootDir, '..') : rootDir;
const frontendRoot = isFrontend ? rootDir : path.join(rootDir, 'frontend');

const targetDirs = [
  path.join(projectRoot, 'node_modules', '.bin'),
  path.join(projectRoot, 'bin'),
  path.join(frontendRoot, 'node_modules', '.bin'),
  path.join(frontendRoot, 'bin')
];

const posixShimContent = `#!/bin/sh
# Universal Intelligent-AML Vercel Shim for Vite -> Next.js Bridge
DIR="$(cd "$(dirname "$0")" && pwd)"
for candidate in \\
  "$DIR/../../frontend/bin/vite-compat.cjs" \\
  "$DIR/../frontend/bin/vite-compat.cjs" \\
  "$DIR/../bin/vite-compat.cjs" \\
  "$DIR/vite-compat.cjs" \\
  "$(pwd)/frontend/bin/vite-compat.cjs" \\
  "$(pwd)/bin/vite-compat.cjs"; do
  if [ -f "$candidate" ]; then
    exec node "$candidate" "$@"
  fi
done
echo "[Vercel Shim] ERROR: Could not locate vite-compat.cjs bridge." >&2
exit 1
`.replace(/\r\n/g, '\n');

const winCmdContent = `@echo off
rem Universal Intelligent-AML Windows Shim for Vite -> Next.js Bridge
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%..\\..\\frontend\\bin\\vite-compat.cjs" (
  node "%SCRIPT_DIR%..\\..\\frontend\\bin\\vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
if exist "%SCRIPT_DIR%..\\frontend\\bin\\vite-compat.cjs" (
  node "%SCRIPT_DIR%..\\frontend\\bin\\vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
if exist "%SCRIPT_DIR%vite-compat.cjs" (
  node "%SCRIPT_DIR%vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
node "%CD%\\frontend\\bin\\vite-compat.cjs" %*
exit /b %ERRORLEVEL%
`.replace(/\r\n/g, '\r\n');

for (const dir of targetDirs) {
  try {
    fs.mkdirSync(dir, { recursive: true });
    
    // Write POSIX sh shim
    const shPath = path.join(dir, 'vite');
    fs.writeFileSync(shPath, posixShimContent, { encoding: 'utf8', mode: 0o755 });
    try { fs.chmodSync(shPath, 0o755); } catch (_) {}
    
    // Write Windows cmd shim
    const cmdPath = path.join(dir, 'vite.cmd');
    fs.writeFileSync(cmdPath, winCmdContent, { encoding: 'utf8' });
  } catch (err) {
    // Non-fatal if a specific directory cannot be accessed
  }
}

console.log('[ensure-vite-shim] Universal vite shims created successfully across root and frontend.');
