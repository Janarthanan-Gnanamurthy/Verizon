#!/bin/bash

# Function to check if Python is installed
check_python() {
  if command -v python3 &>/dev/null; then
    echo "Python is installed."
  else
    echo "Python is not installed. Please install Python 3.8 or newer."
    exit 1
  fi
}

# Function to check if Node.js is installed
check_node() {
  if command -v node &>/dev/null; then
    echo "Node.js is installed."
  else
    echo "Node.js is not installed. Please install Node.js 14 or newer."
    exit 1
  fi
}

# Function to setup and run backend
setup_backend() {
  echo "Setting up backend..."
  cd backend || exit
  
  # Create virtual environment if it doesn't exist
  if [ ! -d "venv" ]; then
    python3 -m venv venv
  fi
  
  # Activate virtual environment
  source venv/bin/activate
  
  # Install dependencies
  pip install -r requirements.txt
  
  # Check if .env file exists, create from example if not
  if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
      cp .env.example .env
      echo "Created .env file from .env.example. Please edit the file to add your Groq API key."
    else
      echo "ERROR: .env.example not found. Please create a .env file manually."
    fi
  fi
  
  # Start backend server in background
  echo "Starting backend server..."
  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
  BACKEND_PID=$!
  
  cd ..
}

# Function to setup and run frontend
setup_frontend() {
  echo "Setting up frontend..."
  cd frontend || exit
  
  # Install dependencies
  npm install
  
  # Start frontend server
  echo "Starting frontend server..."
  npm run dev
  
  cd ..
}

# Main execution
check_python
check_node

# Setup and run backend
setup_backend

# Setup and run frontend
setup_frontend

# Cleanup on exit
trap 'kill $BACKEND_PID; echo "Shutting down servers..."; exit' INT TERM 