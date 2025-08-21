# RAG System Usage Guide

This guide shows you how to use the RAG system CLI effectively.

## 🚀 Quick Start

### 1. Build a RAG System

```bash
# Build from a single URL
python rag_cli.py build -u "https://lilianweng.github.io/posts/2023-06-23-agent/"

# Build from multiple URLs
python rag_cli.py build -u "https://python.langchain.com/docs/tutorials/rag/" -u "https://lilianweng.github.io/posts/2023-06-23-agent/"

# Build from a file containing URLs
python rag_cli.py build -f example_urls.txt

# Use a specific model
python rag_cli.py build -u "https://example.com" -m "qwen2.5:7b-instruct"
```

### 2. Query the RAG System

#### Single Question Mode
```bash
# Ask a single question
python rag_cli.py query -q "What is RAG?"

# Use quotes for questions with spaces
python rag_cli.py query -q "What are the main components of an AI agent system?"
```

#### Interactive Mode
```bash
# Start interactive chat mode
python rag_cli.py query -i

# Then type your questions interactively:
# Question: What is RAG?
# Question: How do agents work?
# Question: quit
```

## ❌ Common Mistakes

### Don't do this:
```bash
# ❌ Wrong: Passing question to interactive mode
python rag_cli.py query -i "What is RAG?"

# ❌ Wrong: No question provided
python rag_cli.py query

# ❌ Wrong: Missing quotes around question with spaces
python rag_cli.py query -q What is RAG?
```

### Do this instead:
```bash
# ✅ Correct: Single question mode
python rag_cli.py query -q "What is RAG?"

# ✅ Correct: Interactive mode
python rag_cli.py query -i

# ✅ Correct: Quoted question with spaces
python rag_cli.py query -q "What is RAG and how does it work?"
```

## 🔧 Other Commands

### Check System Status
```bash
python rag_cli.py status
```

### List Available Models
```bash
python rag_cli.py list-models
```

### Run Tests
```bash
python rag_cli.py test
```

### Get Help
```bash
# General help
python rag_cli.py --help

# Command-specific help
python rag_cli.py build --help
python rag_cli.py query --help
```

## 📝 Examples

### Complete Workflow

```bash
# 1. Build the RAG system
python rag_cli.py build -u "https://python.langchain.com/docs/tutorials/rag/" -u "https://lilianweng.github.io/posts/2023-06-23-agent/"

# 2. Check status
python rag_cli.py status

# 3. Ask questions
python rag_cli.py query -q "What is RAG?"
python rag_cli.py query -q "How do AI agents work?"

# 4. Or use interactive mode
python rag_cli.py query -i
```

### URL Validation

```bash
# Check and fix common URL issues
python url_helper.py

# The system automatically fixes common typos like:
# github.ioposts → github.io/posts
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No question provided" error**
   - Use `-q` flag for single questions: `python rag_cli.py query -q "Your question"`
   - Use `-i` flag for interactive mode: `python rag_cli.py query -i`

2. **URL not found errors**
   - Check the URL spelling
   - Use `python url_helper.py` to validate URLs
   - Make sure the URL is accessible

3. **Model not found errors**
   - Run `python rag_cli.py list-models` to see available models
   - Make sure Ollama is running: `ollama serve`
   - Pull the model: `ollama pull llama3.1:8b-instruct-q8_0`

### Getting Help

```bash
# Check if everything is working
python test_rag.py

# Check requirements
python check_requirements.py

# Get detailed help
python rag_cli.py --help
```

## 💡 Tips

- **Use quotes** around questions with spaces
- **Interactive mode** is great for multiple questions
- **Single question mode** is faster for one-off queries
- **Check URLs** before building the system
- **Use the test command** to verify everything works
