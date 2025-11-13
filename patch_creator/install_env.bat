:: install python .env if not present
if not exist .env (
    @echo Python virtual environment not found. Installing...    
    py --version >NUL 2>NUL || goto VER_FAIL
    py -m venv --upgrade-deps .env || goto SETUP_FAIL
)

@echo Syncing python virtual environment...
.env\scripts\python -m pip install --disable-pip-version-check --require-virtualenv --requirement tool\requirements.txt || goto SETUP_FAIL

:: exit codes
@echo SUCCESS
pause
exit /b 0

:VER_FAIL
@echo FATAL ERROR: Python launcher is not installed or is not in your PATH!
pause
exit /b %ERRORLEVEL%

:SETUP_FAIL
@echo FATAL ERROR: Conan setup has failed!
pause
exit /b %ERRORLEVEL%