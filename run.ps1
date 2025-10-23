# Function Graph Plotter - Launch Script
# Run this script to start the application

# Activate virtual environment and run the application
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"
$env:PYTHONPATH = $PSScriptRoot
python -m src.main
