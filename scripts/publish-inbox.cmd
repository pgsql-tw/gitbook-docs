@echo off
rem Publish translations that other AI agents left in the inbox: validate, then one commit per page (no push).
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
rem 語意審查需要 codex CLI；雙擊執行時 PATH 可能不含它，這裡補上常見安裝位置。
set "PATH=%PATH%;%APPDATA%\npm;%LOCALAPPDATA%\Programs\codex\bin;%USERPROFILE%\.local\bin;%USERPROFILE%\AppData\Roaming\npm"
where codex >>"%LOG%" 2>&1
where codex >nul 2>nul || (
  >>"%LOG%" echo ERROR: codex CLI not found in PATH; inbox review cannot run.
  >>"%LOG%" echo HINT: open a terminal where "codex --version" works, cd to the repo and run: %PY% scripts\agent_handoff.py publish --publisher publish-inbox
  exit /b 8
)
>>"%LOG%" git rev-parse --abbrev-ref HEAD 2>&1
%PY% scripts\agent_handoff.py publish --publisher publish-inbox >>"%LOG%" 2>&1
set RC=%ERRORLEVEL%
>>"%LOG%" echo exit=%RC%
>>"%LOG%" git log --format="%%h %%an %%s" -6 2>&1
>>"%LOG%" git status --short 2>&1
exit /b %RC%
