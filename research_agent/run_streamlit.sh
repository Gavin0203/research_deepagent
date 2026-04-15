#!/bin/bash

echo ""
echo "========================================"
echo "  Deep Research Agent - Streamlit App"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f "./venv-research/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please ensure venv-research is set up in the parent directory."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Activate virtual environment
source ./venv-research/bin/activate

# Check if streamlit is installed
python -m pip show streamlit > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Streamlit not found. Installing dependencies..."
    pip install -r ./streamlit_requirements.txt
fi

# Run Streamlit app
echo ""
echo "Starting Streamlit application..."
echo "The app will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

python -m streamlit run streamlit_app.py
