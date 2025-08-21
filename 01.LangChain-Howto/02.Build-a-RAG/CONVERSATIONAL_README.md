# Conversational RAG System

A powerful conversational RAG (Retrieval-Augmented Generation) system that maintains conversation history and allows for natural follow-up questions using LangGraph and Ollama.

## 🚀 Features

### Core Features
- **Conversation History**: Maintains context across multiple interactions
- **Session Management**: Multiple independent conversation sessions
- **Follow-up Questions**: Natural conversation flow with context retention
- **Document Retrieval**: Intelligent document search and retrieval
- **Rich CLI Interface**: Beautiful command-line interface with progress indicators

### Advanced Features
- **Session Persistence**: Save and load conversation sessions
- **Multiple Models**: Support for different Ollama models
- **Performance Metrics**: Query time tracking and source document analysis
- **Error Handling**: Robust error handling for network and model failures
- **URL Validation**: Automatic URL fixing and validation

## 📋 Prerequisites

### Required Software
- Python 3.8+
- Ollama (for local LLM inference)
- Git

### Python Dependencies
```bash
pip install -r requirements.txt
```

### Ollama Setup
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull a model
ollama pull llama3.1:8b-instruct-q8_0
```

## 🛠️ Installation

1. **Clone the repository** (if not already done):
   ```bash
   cd 01.LangChain-Howto/02.Build-a-RAG
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_conversational_rag.py
   ```

## 🚀 Quick Start

### 1. Build a Conversational RAG System

```bash
# Build from multiple URLs
python conversational_cli.py build \
  -u "https://python.langchain.com/docs/tutorials/rag/" \
  -u "https://lilianweng.github.io/posts/2023-06-23-agent/" \
  -m "llama3.1:8b-instruct-q8_0" \
  -o "my_conversational_rag.json"
```

### 2. Start an Interactive Chat Session

```bash
# Start a new chat session
python conversational_cli.py chat

# Continue a specific session
python conversational_cli.py chat -s "session_123"

# Show conversation history at start
python conversational_cli.py chat --show-history
```

### 3. Ask Single Questions

```bash
# Ask a single question
python conversational_cli.py query -q "What is RAG?"

# Use a specific session
python conversational_cli.py query -q "How does it work?" -s "my_session"
```

## 📖 Usage Examples

### Interactive Chat Mode

```bash
python conversational_cli.py chat
```

This starts an interactive session where you can:

```
Interactive chat mode started. Type 'quit' to exit.

Question: What is RAG?
Answer: RAG (Retrieval-Augmented Generation) is a technique that combines...

Question: How does it work?
Answer: RAG works by first retrieving relevant documents from a knowledge base...

Question: Can you give me an example?
Answer: Here's an example of how RAG works in practice...

Question: history
👤 14:30:15 (USER) What is RAG?
🤖 14:30:18 (ASSISTANT) RAG (Retrieval-Augmented Generation) is a technique...
👤 14:30:25 (USER) How does it work?
🤖 14:30:28 (ASSISTANT) RAG works by first retrieving relevant documents...
👤 14:30:35 (USER) Can you give me an example?
🤖 14:30:38 (ASSISTANT) Here's an example of how RAG works in practice...

Question: quit
Goodbye!
```

### Session Management

```bash
# List all sessions
python conversational_cli.py sessions

# Delete a session
python conversational_cli.py delete-session -s "session_123"

# Check system status
python conversational_cli.py status
```

### Advanced Usage

```bash
# Build with custom parameters
python conversational_cli.py build \
  -u "https://example.com" \
  --chunk-size 500 \
  --chunk-overlap 100 \
  --model "qwen2.5:7b-instruct"

# Test the system
python conversational_cli.py test

# List available models
python conversational_cli.py list-models
```

## 🔧 Configuration

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
LOG_FILE=conversational_rag.log

# Performance Configuration
MAX_TOKENS=4096
TEMPERATURE=0.1
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
K_RETRIEVE=4
```

### Command Line Options

#### Build Command
```bash
python conversational_cli.py build [OPTIONS]

Options:
  -u, --urls TEXT        URLs to fetch content from (multiple)
  -f, --file TEXT        File containing URLs (one per line)
  -m, --model TEXT       Ollama model to use
  -o, --output TEXT      Output file for system info
  --chunk-size INTEGER   Document chunk size
  --chunk-overlap INTEGER Document chunk overlap
```

#### Chat Command
```bash
python conversational_cli.py chat [OPTIONS]

Options:
  -s, --session TEXT     Session ID to use
  --system-info TEXT     System info file
  --sessions-file TEXT   Sessions file
  --show-history         Show conversation history at start
```

#### Query Command
```bash
python conversational_cli.py query [OPTIONS]

Options:
  -s, --session TEXT     Session ID to query
  -q, --question TEXT    Question to ask
  --system-info TEXT     System info file
  --sessions-file TEXT   Sessions file
```

## 🏗️ System Architecture

### Components

1. **ConversationalRAGSystem**: Core system class
   - Manages conversation sessions
   - Handles document processing
   - Coordinates retrieval and generation

2. **ConversationSession**: Session management
   - Stores conversation history
   - Maintains session metadata
   - Handles session persistence

3. **ConversationMessage**: Message representation
   - User and assistant messages
   - Timestamps and metadata
   - Role-based formatting

4. **CLI Interface**: Command-line interface
   - Rich terminal output
   - Interactive chat mode
   - Session management commands

### Data Flow

```
User Question → Session Context → Document Retrieval → LLM Generation → Response + History Update
```

### Memory Management

- **ConversationBufferMemory**: Maintains conversation history
- **Session Persistence**: Save/load sessions to/from JSON files
- **Context Window**: Configurable context retention

## 📊 Performance

### Metrics Tracked
- **Query Time**: Time to process each question
- **Source Documents**: Number of documents retrieved
- **Session Statistics**: Messages per session, session duration
- **System Health**: Model availability, vector store status

### Optimization Tips
- Use smaller chunk sizes for faster retrieval
- Adjust temperature for response creativity
- Increase k_retrieve for more comprehensive answers
- Use appropriate models for your use case

## 🧪 Testing

### Run Tests
```bash
# Test the conversational RAG system
python test_conversational_rag.py

# Test with sample data
python conversational_cli.py test
```

### Test Coverage
- ✅ System initialization
- ✅ Document processing
- ✅ Vector store creation
- ✅ Conversation management
- ✅ Session persistence
- ✅ CLI functionality
- ✅ Error handling

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not running**
   ```bash
   # Start Ollama
   ollama serve
   
   # Check status
   ollama list
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

4. **Session not found**
   ```bash
   # List sessions
   python conversational_cli.py sessions
   
   # Create new session
   python conversational_cli.py chat
   ```

### Debug Mode

Enable debug logging:
```bash
export LOG_LEVEL=DEBUG
python conversational_cli.py chat
```

### Getting Help

```bash
# General help
python conversational_cli.py --help

# Command-specific help
python conversational_cli.py build --help
python conversational_cli.py chat --help
python conversational_cli.py query --help
```

## 📚 Development

### Jupyter Notebook

Use the development notebook for experimentation:
```bash
jupyter notebook 02-Conversational-RAG-Development.ipynb
```

### Adding Features

1. **Extend ConversationalRAGSystem**:
   ```python
   class ConversationalRAGSystem:
       def new_feature(self):
           # Your implementation
           pass
   ```

2. **Add CLI Commands**:
   ```python
   @cli.command()
   def new_command():
       # Your command implementation
       pass
   ```

3. **Update Tests**:
   ```python
   def test_new_feature():
       # Your test implementation
       pass
   ```

### Code Structure

```
conversational_rag.py          # Core system implementation
conversational_cli.py          # CLI interface
test_conversational_rag.py     # Test suite
02-Conversational-RAG-Development.ipynb  # Development notebook
CONVERSATIONAL_README.md       # This documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) for the RAG framework
- [LangGraph](https://python.langgraph.com/) for workflow orchestration
- [Ollama](https://ollama.ai/) for local model inference
- [Chroma](https://www.trychroma.com/) for vector storage
- [HuggingFace](https://huggingface.co/) for embedding models

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test output
3. Check the logs for detailed error messages
4. Open an issue with detailed information

---

**Happy Conversing! 🗣️🤖**
