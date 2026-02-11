@echo off
setlocal

:: === Cleanup previous output ===
if exist out (
    echo [I] Removing previous output folder: out
    rmdir /s /q out
)

call create_tar.bat
if errorlevel 1 (
    echo [E] Failed during TAR + signature creation.
    goto ERROR
)

call create_package.bat
if errorlevel 1 (
    echo [E] Failed during NSIS package creation.
    goto ERROR
)


call copy_sources.bat
if errorlevel 1 (
    echo [E] Failed to copy sources to bin
    goto ERROR
)

echo [I] All done successfully.
goto END

:ERROR
echo [E] ENDED WITH ERROR
pause
exit /b 1

:END
pause
exit /b 0
