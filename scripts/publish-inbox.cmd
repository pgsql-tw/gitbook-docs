@echo off
rem Publish translations that other AI agents left in the inbox: validate, then one commit per page (no push).
rem Double-click to run, or schedule it with Windows Task Scheduler. Protocol: outputs\pg18-translation\agents\PROTOCOL.md
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0.."
set "LOG=outputs\pg18-translation\agents\inbox\publish-log.txt"
if not exist "outputs\pg18-translation\agents\inbox" mkdir "outputs\pg18-translation\agents\inbox"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY where python >nul 2>nul && set "PY=python"
if not defined PY if exist "C:\Python314\python.exe" set "PY=C:\Python314\python.exe"
>>"%LOG%" echo ==== %DATE% %TIME% ====
if not defined PY (
  >>"%LOG%" echo ERROR: python not found
  exit /b 9
)
>>"%LOG%" echo python: %PY%
>>"%LOG%" git rev-parse --abbrev-ref HEAD 2>&1
%PY% scripts\agent_handoff.py publish --publisher publish-inbox >>"%LOG%" 2>&1
set RC=%ERRORLEVEL%
>>"%LOG%" echo exit=%RC%
>>"%LOG%" git log --format="%%h %%an %%s" -6 2>&1
>>"%LOG%" git status --short 2>&1
exit /b %RC%
