@echo off
setlocal
cd /d "%~dp0.."
echo ========================================
echo Realizer V1 Backend
echo ========================================
python -m backend.run
if errorlevel 1 (
  echo.
  echo Realizer backend stopped with an error.
  echo Check Python and backend\requirements.txt.
  pause
)
