@echo off
setlocal

REM Go to the folder where this bat lives (root_folder)
cd /d "%~dp0"

REM Create venv into .env if not exists
if not exist ".env\Scripts\python.exe" (
    echo *************************************************************
    echo Creating virtual environment in .env
    echo *************************************************************
    py -3 -m venv ".env"
)

echo *************************************************************
echo Upgrading pip + installing requirements.txt
echo *************************************************************
".env\Scripts\python.exe" -m pip install --upgrade pip
".env\Scripts\python.exe" -m pip install -r "requirements.txt"

echo *************************************************************
echo Done.
echo *************************************************************
endlocal
