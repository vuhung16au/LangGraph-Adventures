#!/bin/bash

# Setup script for LangGraph Adventures virtual environment
# This script helps set up the Python virtual environment and install dependencies

echo "🚀 Setting up LangGraph Adventures Virtual Environment"
echo "=================================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if virtual environment already exists
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists at .venv/"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf .venv
    else
        echo "✅ Using existing virtual environment"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Setup completed successfully!"
    echo ""
    echo "🎉 Your virtual environment is ready!"
    echo ""
    echo "To activate the virtual environment:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "To deactivate:"
    echo "   deactivate"
    echo ""
    echo "To test the RAG system:"
    echo "   cd 01.LangChain-Howto/02.Build-a-RAG"
    echo "   python test_rag.py"
    echo ""
    echo "Make sure Ollama is running:"
    echo "   ollama serve"
    echo ""
else
    echo "❌ Installation failed. Please check the error messages above."
    exit 1
fi
