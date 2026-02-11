@echo off
setlocal

:: === Config ===
set NSIS_EXE="%ProgramFiles(x86)%\NSIS\makensis.exe"
set NSIS_SCRIPT=nsis\installer.nsi

if not exist %NSIS_EXE% (
    echo [E] NSIS failed.
    pause
    exit /b 1
)

if not exist out\bin (
    mkdir out\bin
)

:: === Run NSIS ===
%NSIS_EXE% %NSIS_SCRIPT%

if errorlevel 1 (
    echo [E] NSIS failed.
    pause
    exit /b 1
)

echo [I] Package created successfully.
pause
exit /b 0
