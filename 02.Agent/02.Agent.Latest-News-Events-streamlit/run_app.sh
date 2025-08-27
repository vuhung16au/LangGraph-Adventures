#!/bin/bash

# News Dashboard Streamlit App Launcher
echo "🚀 Starting Personalized News Dashboard..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project directory."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Error: Virtual environment not found. Please ensure you have the .venv directory."
    exit 1
fi

# Activate virtual environment and run the app
echo "📦 Activating virtual environment..."
source ../.venv/bin/activate

echo "🔧 Installing dependencies..."
pip install -r requirements.txt

echo "🌐 Starting Streamlit app..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo "🛑 Press Ctrl+C to stop the app"

streamlit run app.py
