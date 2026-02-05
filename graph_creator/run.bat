@echo off
setlocal

cd /d "%~dp0"

if "%~1"=="" (
    echo Usage: run.bat ^<filename.csv^>
    echo Example: run.bat filename01.csv
    exit /b 2
)

set "DATASET=%~1"
set "DATASET_PATH=%CD%\datasets\%DATASET%"

if not exist ".env\Scripts\python.exe" (
    echo *************************************************************
    echo ERROR: venv not found. Run createenv.bat first.
    echo *************************************************************
    exit /b 3
)

if not exist "%DATASET_PATH%" (
    echo *************************************************************
    echo ERROR: Dataset not found:
    echo %DATASET_PATH%
    echo *************************************************************
    exit /b 4
)

echo *************************************************************
echo Running: %DATASET_PATH%
echo *************************************************************

echo Script dir: %~dp0
echo Current dir: %CD%
echo Dataset path: %DATASET_PATH%
pause

.env\Scripts\python.exe cg.py %DATASET_PATH% --labels

endlocal