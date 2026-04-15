@echo off
echo.
echo ========================================
echo  Deep Research Agent - Streamlit App
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv-research\Scripts\activate.bat" (
    echo Error: Virtual environment not found!
    echo Please ensure venv-research is set up in the parent directory.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call ..\venv-research\Scripts\activate.bat

REM Check if streamlit is installed
python -m pip show streamlit > nul 2>&1
if errorlevel 1 (
    echo Streamlit not found. Installing dependencies...
    pip install -r ..\streamlit_requirements.txt
)

REM Run Streamlit app
echo.
echo Starting Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server.
echo.

python -m streamlit run streamlit_app.py

pause
