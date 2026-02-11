@echo off
setlocal

:: === Config ===
set TAR_DIR=payload
set OUT_DIR=out\source
set TAR_NAME=payload.tar
set SIG_NAME=payload.sig

:: === Ensure output directory exists ===
if not exist "%OUT_DIR%" (
    mkdir "%OUT_DIR%"
)

:: === Validate source folder ===
if not exist "%TAR_DIR%\*" (
    echo [E] Folder '%TAR_DIR%' is missing or empty.
    exit /b 1
)

:: === Clean previous output ===
echo [I] Cleaning up...
del /f /q "%OUT_DIR%\%TAR_NAME%" "%OUT_DIR%\%SIG_NAME%" 2>nul

:: === Create TAR file ===
echo [I] Creating TAR from '%TAR_DIR%'...
tar -cf "%OUT_DIR%\%TAR_NAME%" -C "%TAR_DIR%" .
if not exist "%OUT_DIR%\%TAR_NAME%" (
    echo [E] Failed to create TAR file.
    exit /b 1
)

:: === Generate SHA256 signature (single clean line) ===
echo [I] Generating SHA256 signature...
setlocal enabledelayedexpansion
for /f "skip=1 tokens=1" %%H in ('certutil -hashfile "%OUT_DIR%\%TAR_NAME%" SHA256') do (
    set "HASH=%%H"
    goto :hash_done
)
:hash_done
(
    echo !HASH!
) > "%OUT_DIR%\%SIG_NAME%"
endlocal

:: === Final confirmation ===
if not exist "%OUT_DIR%\%SIG_NAME%" (
    echo [E] Failed to generate signature.
    exit /b 1
)

echo [I] TAR and signature successfully created.
exit /b 0
