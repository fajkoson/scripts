@echo off
setlocal

REM --- Store path of this script's directory into %root% ---
set "root=%~dp0"

REM --- Path to your virtualenv's Python ---
set "PYEXE=%root%.env\Scripts\python.exe"

REM --- Path to your Python script in src folder ---
set "SCRIPT=%root%src\makepatch.py"

REM --- Run script, passing all forwarded args ---
"%PYEXE%" "%SCRIPT%" %*

endlocal
