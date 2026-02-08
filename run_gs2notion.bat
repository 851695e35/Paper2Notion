@echo off
REM GS2Notion Pipeline Runner
REM This script runs the GS2Notion automation pipeline

cd /d "D:\tools\vibe\gs2notion"

echo.
echo ========================================
echo   GS2Notion Pipeline Starting...
echo ========================================
echo.

python main.py

echo.
echo ========================================
echo   Pipeline Completed!
echo ========================================
echo.
pause
