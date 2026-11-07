@echo off
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\local_screen_run.ps1
echo.
echo Done. You can close this window.
pause
