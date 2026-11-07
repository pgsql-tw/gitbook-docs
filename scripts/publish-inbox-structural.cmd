@echo off
rem Offline preflight ONLY. Does not publish or mark complete. Semantic review is mandatory.
rem Double-click to run, or schedule it with Windows Task Scheduler. Protocol: outputs\pg-translation\agents\PROTOCOL.md
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY if exist "C:\Python314\python.exe" set "PY=C:\Python314\python.exe"
if not defined PY (
  echo ERROR: python not found
  exit /b 9
)
set "PG_OUTPUT="
for /f "delims=" %%D in ('%PY% scripts\pg_project.py --relative') do set "PG_OUTPUT=%%D"
if not defined PG_OUTPUT exit /b 10
set "PG_OUTPUT=%PG_OUTPUT:/=\%"
set "LOG=%PG_OUTPUT%\agents\inbox\publish-log.txt"
if not exist "%PG_OUTPUT%\agents\inbox" mkdir "%PG_OUTPUT%\agents\inbox"
>>"%LOG%" echo ==== %DATE% %TIME% ====
>>"%LOG%" echo python: %PY%
>>"%LOG%" git rev-parse --abbrev-ref HEAD 2>&1
%PY% scripts\publish_inbox_structural.py %1 >>"%LOG%" 2>&1
set RC=%ERRORLEVEL%
>>"%LOG%" echo exit=%RC%
>>"%LOG%" git log --format="%%h %%an %%s" -6 2>&1
>>"%LOG%" git status --short 2>&1
exit /b %RC%
