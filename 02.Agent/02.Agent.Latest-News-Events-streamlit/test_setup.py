#!/usr/bin/env python3
"""
Test script to verify the Streamlit news app setup
"""

import sys
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ langchain-google-genai imported successfully")
    except ImportError as e:
        print(f"❌ langchain-google-genai import failed: {e}")
        return False
    
    try:
        from langchain_community.tools.tavily_search import TavilySearchResults
        print("✅ TavilySearchResults imported successfully")
    except ImportError as e:
        print(f"❌ TavilySearchResults import failed: {e}")
        return False
    
    try:
        from langgraph.prebuilt import create_react_agent
        print("✅ create_react_agent imported successfully")
    except ImportError as e:
        print(f"❌ create_react_agent import failed: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration file can be loaded"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import NEWS_CATEGORIES, APP_CONFIG, AGENT_CONFIG
        print("✅ Configuration imported successfully")
        print(f"   - Found {len(NEWS_CATEGORIES)} news categories")
        print(f"   - App title: {APP_CONFIG['page_title']}")
        print(f"   - Agent model: {AGENT_CONFIG['model']}")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_env_file():
    """Test if environment file exists"""
    print("\n🔍 Testing environment file...")
    
    env_path = Path("/Users/vuhung/Desktop/LangGraph-Adventures/02.Agent/.env.local")
    if env_path.exists():
        print("✅ Environment file found")
        return True
    else:
        print("❌ Environment file not found")
        print("   Please ensure .env.local exists with your API keys")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Streamlit News App Setup")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_env_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To run the app:")
        print("   cd /Users/vuhung/Desktop/LangGraph-Adventures/02.Agent/02.Agent.Latest-News-Events-streamlit")
        print("   ./run_app.sh")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Install missing dependencies: pip install -r requirements.txt")
        print("   - Check your .env.local file has the required API keys")
        print("   - Ensure you're using the correct Python environment")

if __name__ == "__main__":
    main()
