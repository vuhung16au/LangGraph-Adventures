#!/usr/bin/env python3
"""
Requirements Check Script

This script checks if all required dependencies are installed
and provides helpful information about missing packages.
"""

import sys
import importlib
import subprocess

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def check_ollama():
    """Check if Ollama is available"""
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stderr if result.returncode != 0 else None
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False, "Ollama not found or not responding"

def main():
    """Main function to check all requirements"""
    print("🔍 Checking LangGraph Adventures Requirements")
    print("=" * 50)
    
    # Core dependencies
    core_packages = [
        ("langchain", "langchain"),
        ("langchain-ollama", "langchain_ollama"),
        ("langchain-community", "langchain_community"),
        ("langgraph", "langgraph"),
        ("chromadb", "chromadb"),
        ("sentence-transformers", "sentence_transformers"),
        ("beautifulsoup4", "bs4"),
        ("requests", "requests"),
        ("rich", "rich"),
        ("click", "click"),
        ("python-dotenv", "dotenv"),
        ("numpy", "numpy"),
        ("pandas", "pandas"),
    ]
    
    print("\n📦 Checking Python packages:")
    all_good = True
    
    for package, import_name in core_packages:
        installed, error = check_package(package, import_name)
        status = "✅" if installed else "❌"
        print(f"  {status} {package}")
        if not installed:
            all_good = False
            print(f"     Error: {error}")
    
    print("\n🤖 Checking Ollama:")
    ollama_ok, ollama_error = check_ollama()
    status = "✅" if ollama_ok else "❌"
    print(f"  {status} Ollama")
    if not ollama_ok:
        all_good = False
        print(f"     Error: {ollama_error}")
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 All requirements are satisfied!")
        print("\nYou can now run:")
        print("  cd 01.LangChain-Howto/02.Build-a-RAG")
        print("  python test_rag.py")
    else:
        print("⚠️  Some requirements are missing.")
        print("\nTo install missing packages:")
        print("  pip install -r requirements.txt")
        print("\nTo install Ollama:")
        print("  curl -fsSL https://ollama.ai/install.sh | sh")
        print("  ollama serve")
        print("  ollama pull llama3.1:8b-instruct-q8_0")

if __name__ == "__main__":
    main()
