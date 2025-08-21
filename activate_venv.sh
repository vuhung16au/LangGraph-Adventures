#!/bin/bash

# Simple script to activate the virtual environment
# Usage: source activate_venv.sh

if [ -d ".venv" ]; then
    echo "🔧 Activating virtual environment..."
    source .venv/bin/activate
    echo "✅ Virtual environment activated!"
    echo "You can now run:"
    echo "  cd 01.LangChain-Howto/02.Build-a-RAG"
    echo "  python test_rag.py"
else
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup_venv.sh first to create the virtual environment."
fi
