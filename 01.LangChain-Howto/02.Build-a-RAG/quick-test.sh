#!/bin/bash

# Quick Test Script for RAG System
# This script performs basic functionality testing

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 RAG System Quick Test${NC}"
echo "========================"
echo ""

# Check if we're in the right directory
if [ ! -f "rag_system.py" ]; then
    echo -e "${RED}❌ This script must be run from the 02.Build-a-RAG directory${NC}"
    exit 1
fi

# Test 1: Basic Python test
echo -e "${BLUE}Test 1: Running test_rag.py...${NC}"
if python3 test_rag.py; then
    echo -e "${GREEN}✅ test_rag.py passed${NC}"
else
    echo -e "${RED}❌ test_rag.py failed${NC}"
    exit 1
fi

# Test 2: Check Ollama
echo -e "${BLUE}Test 2: Checking Ollama...${NC}"
if command -v ollama >/dev/null 2>&1 && ollama list >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is running${NC}"
else
    echo -e "${RED}❌ Ollama is not running${NC}"
    echo "Please start Ollama: ollama serve"
    exit 1
fi

# Test 3: Build RAG system
echo -e "${BLUE}Test 3: Building RAG system...${NC}"
if python3 rag_cli.py build -u "https://python.langchain.com/docs/tutorials/rag/" -o "quick_test.json"; then
    echo -e "${GREEN}✅ RAG system built successfully${NC}"
else
    echo -e "${RED}❌ RAG system build failed${NC}"
    exit 1
fi

# Test 4: Query RAG system
echo -e "${BLUE}Test 4: Testing query...${NC}"
if python3 rag_cli.py query -q "What is RAG?" >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Query test passed${NC}"
else
    echo -e "${RED}❌ Query test failed${NC}"
    exit 1
fi

# Cleanup
rm -f quick_test.json

echo ""
echo -e "${GREEN}🎉 Quick test completed successfully!${NC}"
echo ""
echo "Your RAG system is working correctly."
echo "Run './end-to-end-test.sh' for comprehensive testing."
