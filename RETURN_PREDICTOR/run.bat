@echo off
title RETURNAI - E-Commerce Return Predictor
echo ========================================================
echo        ⚡ RETURNAI // RETURN PREDICTOR LAUNCHER ⚡
echo ========================================================
echo.

cd /d "%~dp0"

echo [1/4] Checking Python environment...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not found in your PATH!
    echo Please install Python 3.9+ from https://www.python.org or the Microsoft Store.
    echo In the meantime, you can run the standalone browser app immediately by opening index.html!
    echo.
    pause
    exit /b 1
)

echo [2/4] Setting up virtual environment (venv)...
if not exist "venv" (
    echo Creating new virtual environment...
    python -m venv venv
)

call "venv\Scripts\activate.bat"

echo [3/4] Installing / verifying dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install -r requirements.txt

echo [4/4] Checking model weights and synthetic dataset...
if not exist "return_model.joblib" (
    echo Training Random Forest Machine Learning Model...
    python train_model.py
)

echo.
echo ========================================================
echo  🚀 Starting Streamlit Server at http://localhost:8501
echo ========================================================
streamlit run app.py

pause

