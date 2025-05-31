#!/bin/bash

echo "========================================="
echo "Documentation Analyzer Setup"
echo "========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo " Found: $python_version"
else
    echo " Python 3 is required but not found"
    exit 1
fi

# Check pip
echo "Checking pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo " pip is not available"
    exit 1
fi

# Create virtual environment
read -p "Create virtual environment? (y/n): " create_venv
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    python3 -m venv venv
    source venv/bin/activate
    echo " Virtual environment activated"
fi

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt
if [[ $? -eq 0 ]]; then
    echo " Dependencies installed successfully"
else
    echo " Failed to install dependencies"
    exit 1
fi
# Check for additional tools
echo "Checking for additional tools..."
if command -v pylint &> /dev/null; then
    echo " pylint is installed"
else
    echo " pylint is not installed, please install it using 'pip install pylint'"
fi
if command -v black &> /dev/null; then
    echo " black is installed"
else
    echo " black is not installed, please install it using 'pip install black'"
fi
# Check for additional Python packages
echo "Checking for additional Python packages..."
if python3 -c "import requests" &> /dev/null; then
    echo " requests is installed"
else
    echo " requests is not installed, please install it using 'pip install requests'"
fi
if python3 -c "import beautifulsoup4" &> /dev/null; then
    echo " beautifulsoup4 is installed"
else
    echo " beautifulsoup4 is not installed, please install it using 'pip install beautifulsoup4'"
fi
# Final message
echo "========================================="
echo "Documentation Analyzer setup completed!"
echo "You can now run the analyzer using 'python3 analyzer.py'"
echo "========================================="
# Deactivate virtual environment if created
if [[ $create_venv == "y" || $create_venv == "Y" ]]; then
    deactivate
    echo "Virtual environment deactivated"
fi
# Exit script
exit 0
# End of setup script
# This script sets up the Documentation Analyzer environment by checking for Python, pip, creating a virtual environment, and installing dependencies.
# It also checks for additional tools and Python packages that may be required for the analyzer to function properly.
# Ensure the script is executable
chmod +x setup.sh
# Usage: Run this script in the terminal to set up the Documentation Analyzer environment.
# Make sure to have a requirements.txt file in the same directory with the necessary dependencies listed. 