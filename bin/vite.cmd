@echo off
rem Universal Intelligent-AML Windows Shim for Vite -> Next.js Bridge
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%..\..\frontend\bin\vite-compat.cjs" (
  node "%SCRIPT_DIR%..\..\frontend\bin\vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
if exist "%SCRIPT_DIR%..\frontend\bin\vite-compat.cjs" (
  node "%SCRIPT_DIR%..\frontend\bin\vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
if exist "%SCRIPT_DIR%vite-compat.cjs" (
  node "%SCRIPT_DIR%vite-compat.cjs" %*
  exit /b %ERRORLEVEL%
)
node "%CD%\frontend\bin\vite-compat.cjs" %*
exit /b %ERRORLEVEL%
