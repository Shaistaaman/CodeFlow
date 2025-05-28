#!/bin/bash

# Check if Python is installed
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    echo "Error: Python is not installed. Please install Python 3.x to run this game."
    exit 1
fi

# Check if Pygame is installed
$PYTHON -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Pygame is not installed. Attempting to install..."
    $PYTHON -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install Pygame. Please install it manually with 'pip install pygame'."
        exit 1
    fi
fi

# Run the game
$PYTHON main.py
