# Testing Guide

This guide explains how to test the RAG system using the provided test scripts.

## 🚀 Quick Test

The quick test script performs basic functionality testing:

```bash
./quick-test.sh
```

**What it tests:**
- ✅ Python dependencies and imports
- ✅ RAG system core functionality
- ✅ Ollama service availability
- ✅ RAG system building
- ✅ Basic querying

**Duration:** ~2-3 minutes

## 🔍 Comprehensive End-to-End Test

The comprehensive test script performs full system testing:

```bash
./end-to-end-test.sh
```

**What it tests:**
- ✅ All quick test items
- ✅ Multiple URL processing
- ✅ Interactive query mode
- ✅ System status commands
- ✅ Model listing
- ✅ Error handling
- ✅ Cleanup procedures

**Duration:** ~5-10 minutes

## 🧪 Manual Testing

### Test Python Components

```bash
# Test core RAG functionality
python3 test_rag.py

# Test URL validation
python3 url_helper.py
```

### Test CLI Commands

```bash
# Check system status
python3 rag_cli.py status

# List available models
python3 rag_cli.py list-models

# Test build command
python3 rag_cli.py build -u "https://example.com" -o "test.json"

# Test query command
python3 rag_cli.py query -q "What is RAG?"

# Test interactive mode
python3 rag_cli.py query -i
```

## 🛠️ Test Scripts Details

### `quick-test.sh`

**Purpose:** Fast verification that the system works
**Use case:** After installation or when making small changes
**Output:** Simple pass/fail with colored status messages

**Features:**
- Automatic cleanup of test files
- Clear error messages
- Fast execution
- Basic functionality verification

### `end-to-end-test.sh`

**Purpose:** Comprehensive system validation
**Use case:** Before deployment or major changes
**Output:** Detailed test results with timing information

**Features:**
- Automatic Ollama startup if needed
- Model availability checking
- Multiple URL testing
- Interactive mode testing
- Complete cleanup
- Signal handling (Ctrl+C safe)
- Colored output with status indicators

## 📊 Test Results Interpretation

### Success Indicators

✅ **All tests passed** - System is ready for use
✅ **Green status messages** - Individual components working
✅ **No error messages** - Clean execution

### Common Issues

❌ **Ollama not running** - Start with `ollama serve`
❌ **Model not found** - Pull with `ollama pull llama3.1:8b-instruct-q8_0`
❌ **Python import errors** - Check virtual environment and dependencies
❌ **Network errors** - Check internet connection and URL accessibility

### Performance Metrics

**Expected timings:**
- Quick test: 2-3 minutes
- End-to-end test: 5-10 minutes
- Individual queries: 2-5 seconds
- System build: 1-3 minutes

## 🔧 Troubleshooting Tests

### Test Script Won't Run

```bash
# Make scripts executable
chmod +x quick-test.sh
chmod +x end-to-end-test.sh

# Check if in correct directory
ls rag_system.py
```

### Tests Fail

1. **Check Ollama:**
   ```bash
   ollama list
   ollama serve  # if not running
   ```

2. **Check Python environment:**
   ```bash
   python3 -c "import langchain; print('OK')"
   ```

3. **Check dependencies:**
   ```bash
   python3 check_requirements.py
   ```

4. **Check URLs:**
   ```bash
   python3 url_helper.py
   ```

### Performance Issues

- **Slow tests:** Normal for first run (model loading)
- **Memory issues:** Close other applications
- **Network timeouts:** Check internet connection

## 📝 Test Customization

### Modify Test URLs

Edit the test scripts to use different URLs:

```bash
# In quick-test.sh or end-to-end-test.sh
python3 rag_cli.py build -u "https://your-url.com" -o "test.json"
```

### Add Custom Tests

Add your own test cases to `test_rag.py`:

```python
def test_custom_functionality():
    # Your test code here
    pass
```

### Environment Variables

Set test-specific environment variables:

```bash
export LOG_LEVEL=DEBUG
export OLLAMA_MODEL=your-model
./end-to-end-test.sh
```

## 🎯 Best Practices

1. **Run quick test first** - Fast verification
2. **Run end-to-end test before deployment** - Full validation
3. **Check logs for details** - Use `LOG_LEVEL=DEBUG`
4. **Clean up after tests** - Scripts do this automatically
5. **Test with real URLs** - Use your actual data sources

## 📚 Related Documentation

- **[USAGE.md](USAGE.md)** - Usage guide
- **[README.md](README.md)** - Main documentation
- **[test_rag.py](test_rag.py)** - Python test suite
- **[url_helper.py](url_helper.py)** - URL validation utility
