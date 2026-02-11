@echo off
setlocal

:: === Config ===
set SOURCE_DIR=out\source
set DEST_DIR=out\bin

:: === Ensure target exists ===
if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

:: === Copy files ===
echo [I] Copying sources from %SOURCE_DIR% to %DEST_DIR%...
copy /Y "%SOURCE_DIR%\payload.tar" "%DEST_DIR%\payload.tar" >nul
copy /Y "%SOURCE_DIR%\payload.sig" "%DEST_DIR%\payload.sig" >nul

if errorlevel 1 (
    echo [E] Copy failed.
    pause
    exit /b 1
)

echo [I] Sources copied successfully.
exit /b 0
