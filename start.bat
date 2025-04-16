@echo off
echo Starting Educational Platform...

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or newer.
    exit /b
)

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js is not installed. Please install Node.js 14 or newer.
    exit /b
)

REM Setup and start backend
echo Setting up backend...
cd backend

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Check if .env file exists, create from example if not
if not exist .env (
    if exist .env.example (
        copy .env.example .env
        echo Created .env file from .env.example. Please edit the file to add your Groq API key.
    ) else (
        echo ERROR: .env.example not found. Please create a .env file manually.
    )
)

REM Start backend server in a new terminal
start cmd /k "call venv\Scripts\activate && uvicorn app.main:app --reload"

REM Return to root directory
cd ..

REM Setup and start frontend
echo Setting up frontend...
cd frontend

REM Install dependencies
call npm install

REM Start frontend server
start cmd /k "npm run dev"

echo Servers started! Access the application at http://localhost:3000
echo Press any key to shut down servers...
pause >nul

REM Kill server processes
taskkill /f /im node.exe >nul 2>nul
taskkill /f /im python.exe >nul 2>nul 