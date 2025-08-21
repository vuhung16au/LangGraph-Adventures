# RAG System with LangGraph and Ollama

A Retrieval-Augmented Generation (RAG) system built using LangGraph and Ollama that can fetch content from URLs, create embeddings, and answer questions based on the retrieved content.

## Features

- **URL Content Fetching**: Automatically fetch and process content from web URLs
- **Document Processing**: Split documents into chunks for better retrieval
- **Vector Storage**: Use Chroma vector database for efficient document storage and retrieval
- **Intelligent Retrieval**: Find the most relevant documents for user queries
- **Answer Generation**: Generate accurate answers using Ollama models
- **CLI Interface**: Easy-to-use command-line interface
- **Interactive Mode**: Chat-like interface for continuous questioning
- **Performance Metrics**: Track query times and system performance
- **Error Handling**: Robust error handling for network and model issues

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** installed and running locally
3. At least one Ollama model downloaded (e.g., `llama3.1:8b-instruct-q8_0`)

### Installing Ollama

```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### Installing Python Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Build a RAG System

```bash
# Build from specific URLs
python rag_cli.py build -u "https://python.langchain.com/docs/tutorials/rag/" -u "https://lilianweng.github.io/posts/2023-06-23-agent/"

# Build from a file containing URLs
echo "https://python.langchain.com/docs/tutorials/rag/" > urls.txt
echo "https://lilianweng.github.io/posts/2023-06-23-agent/" >> urls.txt
python rag_cli.py build -f urls.txt

# Use a specific Ollama model
python rag_cli.py build -u "https://example.com" -m "qwen2.5:7b-instruct"
```

### 2. Query the RAG System

```bash
# Single question
python rag_cli.py query -q "What is RAG and how does it work?"

# Interactive mode
python rag_cli.py query -i
```

### 3. Test the System

```bash
# Run comprehensive tests
python rag_cli.py test

# Test with specific model
python rag_cli.py test -m "llama3.1:8b-instruct-q8_0"
```

## Usage Examples

### Building a RAG System

```bash
# Build from multiple URLs
python rag_cli.py build \
  -u "https://python.langchain.com/docs/tutorials/rag/" \
  -u "https://lilianweng.github.io/posts/2023-06-23-agent/" \
  -u "https://example.com/article" \
  -m "llama3.1:8b-instruct-q8_0" \
  -o "my_rag_system.json"
```

### URL Validation

The RAG system includes automatic URL validation and fixes for common issues:

```bash
# Test URL fixes
python url_helper.py
```

**Common URL fixes:**
- `github.ioposts` → `github.io/posts`
- Missing `https://` protocol
- Duplicate path segments

### Interactive Querying

```bash
python rag_cli.py query -i
```

This will start an interactive session where you can ask questions:

```
Interactive mode started. Type 'quit' to exit.

Question: What is RAG?
Answer: RAG (Retrieval-Augmented Generation) is a technique that combines...

Question: How do agents work?
Answer: AI agents are systems that can perceive their environment...

Question: quit
Goodbye!
```

### Single Query

```bash
python rag_cli.py query -q "What are the key components of a RAG system?"
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b-instruct-q8_0

# Vector Store Configuration
VECTOR_STORE_TYPE=chroma
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=rag_system.log

# Performance Configuration
MAX_TOKENS=4096
TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Available Models

Check available Ollama models:

```bash
python rag_cli.py list-models
```

Or use the Ollama CLI:

```bash
ollama list
```

## Development

### Jupyter Notebook

For development and experimentation, use the Jupyter notebook:

```bash
jupyter notebook 01-RAG-System-Development.ipynb
```

The notebook includes:
- Step-by-step RAG system building
- Interactive testing
- Performance analysis
- System debugging

### Python API

You can also use the RAG system programmatically:

```python
from rag_system import RAGSystem

# Initialize RAG system
rag = RAGSystem(model_name="llama3.1:8b-instruct-q8_0")

# Build from URLs
urls = [
    "https://python.langchain.com/docs/tutorials/rag/",
    "https://lilianweng.github.io/posts/2023-06-23-agent/"
]
rag.build_rag_from_urls(urls)

# Query the system
result = rag.query("What is RAG?")
print(result['answer'])
```

## System Architecture

### Components

1. **Document Ingestion**: Fetches content from URLs using BeautifulSoup
2. **Text Processing**: Splits documents into chunks using RecursiveCharacterTextSplitter
3. **Embedding Generation**: Creates embeddings using HuggingFace models
4. **Vector Storage**: Stores embeddings in Chroma vector database
5. **Retrieval**: Finds relevant documents using similarity search
6. **Answer Generation**: Generates answers using Ollama models

### LangGraph Workflow

The system uses LangGraph for orchestration:

```
User Question → Retrieve Documents → Generate Answer → Return Result
```

### File Structure

```
02.Build-a-RAG/
├── rag_system.py              # Core RAG system implementation
├── rag_cli.py                 # Command-line interface
├── 01-RAG-System-Development.ipynb  # Development notebook
├── README.md                  # This file
├── chroma_db/                 # Vector store (created automatically)
├── rag_system.json           # System configuration (created automatically)
└── rag_system.log            # Log file (created automatically)
```

## Performance

### Typical Performance Metrics

- **Document Processing**: ~1-2 seconds per URL
- **Query Response**: ~2-5 seconds per question
- **Vector Store Creation**: ~30-60 seconds for 1000 documents
- **Memory Usage**: ~500MB-1GB depending on document size

### Optimization Tips

1. **Chunk Size**: Adjust `CHUNK_SIZE` and `CHUNK_OVERLAP` for your use case
2. **Model Selection**: Use smaller models for faster responses
3. **Retrieval Count**: Adjust the number of retrieved documents (default: 4)
4. **Temperature**: Lower temperature for more focused answers

## Troubleshooting

### Common Issues

1. **Ollama not running**
   ```bash
   # Start Ollama
   ollama serve
   ```

2. **Model not found**
   ```bash
   # Pull the model
   ollama pull llama3.1:8b-instruct-q8_0
   ```

3. **Memory issues**
   - Use smaller models
   - Reduce chunk size
   - Close other applications

4. **Network errors**
   - Check internet connection
   - Verify URL accessibility
   - Increase timeout settings

### Debug Mode

Enable debug logging:

```bash
export LOG_LEVEL=DEBUG
python rag_cli.py query -q "test question"
```

### System Status

Check system status:

```bash
python rag_cli.py status
```

## Advanced Usage

### Custom Embeddings

You can use different embedding models by setting the `EMBEDDING_MODEL` environment variable:

```bash
export EMBEDDING_MODEL="sentence-transformers/all-mpnet-base-v2"
```

### Custom Prompts

Modify the prompt template in `rag_system.py`:

```python
prompt_template = """Your custom prompt here.
Context: {context}
Question: {question}
Answer:"""
```

### Multiple Vector Stores

You can create multiple RAG systems by specifying different output directories:

```bash
python rag_cli.py build -u "https://example.com" -o "system1.json"
python rag_cli.py build -u "https://another.com" -o "system2.json"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [LangChain](https://python.langchain.com/) for the RAG framework
- [LangGraph](https://python.langgraph.com/) for workflow orchestration
- [Ollama](https://ollama.ai/) for local model inference
- [Chroma](https://www.trychroma.com/) for vector storage
- [HuggingFace](https://huggingface.co/) for embedding models

## 📖 Additional Documentation

- **[USAGE.md](USAGE.md)** - Detailed usage guide with examples and troubleshooting
- **[url_helper.py](url_helper.py)** - URL validation and fixing utility
- **[test_rag.py](test_rag.py)** - System testing and verification
