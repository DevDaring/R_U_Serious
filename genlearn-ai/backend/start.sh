#!/bin/bash
# R U Serious? Backend - Quick Start Script for Unix/Linux/macOS

echo "============================================================"
echo "R U Serious? Backend - Quick Start"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        echo "Make sure Python 3.11+ is installed"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "Warning: Some dependencies may have failed to install"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "Warning: .env file not found!"
    if [ -f ".env.example" ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo ""
        echo "Please edit .env and add your API keys before continuing"
        read -p "Press Enter to continue..."
    fi
fi

# Start server
echo ""
echo "============================================================"
echo "Starting R U Serious? Backend Server..."
echo "============================================================"
echo ""
python run.py --reload
