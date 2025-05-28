#!/bin/bash

echo "Setting up CodeFlow: The Debugging Odyssey"
echo "----------------------------------------"

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Error: Python is not installed. Please install Python 3.x to run this game."
    exit 1
fi

echo "Using Python: $($PYTHON --version)"

# Check if pip is installed
if ! $PYTHON -m pip --version &>/dev/null; then
    echo "Error: pip is not installed. Please install pip to continue."
    exit 1
fi

echo "Using pip: $($PYTHON -m pip --version)"

# Check if venv module is available
if ! $PYTHON -c "import venv" &>/dev/null; then
    echo "Error: venv module is not available. Please install it to continue."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Error: Could not find activation script for virtual environment."
    exit 1
fi

# Install requirements
echo "Installing required packages..."
pip install pygame

# Run the simple version of the game first
echo "Running simple version of the game to test pygame..."
python simple_game.py

# If that works, try the full game
echo "Running the full game..."
python main.py

# Deactivate virtual environment
deactivate
