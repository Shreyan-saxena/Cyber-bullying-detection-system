@echo off
title Cyberbullying Detector - Runner
echo ==========================================
echo    Cyberbullying Detector Web Application
echo ==========================================
echo.

:: Check if requirements are installed (optional but recommended)
echo [1/2] Checking and installing dependencies...
pip install -r requirements.txt

echo.
echo [2/2] Starting the Flask server...
echo The app will be available at: http://127.0.0.1:5000
echo.

:: Run the application
python app.py

:: If the app crashes, keep the window open
echo.
echo Server has stopped.
pause
