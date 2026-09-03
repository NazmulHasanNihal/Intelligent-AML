@echo off
title Intelligent-AML Master Research Benchmark & Empirical Testing Suite
cd /d "%~dp0\.."

echo ===============================================================================
echo   INTELLIGENT-AML: MASTER PHYSICAL BENCHMARK & EXPERIMENTAL SUITE
echo ===============================================================================
echo   - Mode: Low-RAM Eco-Background Active (Leaves 4 CPU Cores & RAM Free)
echo   - Priority: LOW (Absolute priority to Windows UI, Mouse, and Apps)
echo   - Fault-Tolerance: Atomic Checkpointing after EVERY Model and Test
echo   - Safe Against Power Loss / Crashes: Resumes from exact pending test
echo ===============================================================================
echo.

start /low /wait .\venv\Scripts\python.exe scripts\master_physical_benchmark_runner.py

echo.
echo ===============================================================================
echo   BENCHMARK & EMPIRICAL TEST SUITE COMPLETED OR PAUSED.
echo ===============================================================================
pause
