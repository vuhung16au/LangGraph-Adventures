# Tech Stack Documentation

This document provides detailed information about the technologies, frameworks, and tools used in the RAG From Scratch project.

## 🏗️ Core Framework

### **LangChain**
- **Version**: 0.3.27+
- **Purpose**: Core RAG framework and orchestration
- **Key Features**:
  - Document loaders and processors
  - Text splitters and chunking strategies
  - Vector store integrations
  - LLM orchestration and chaining
  - Prompt management and templates
  - Output parsing and formatting
- **Documentation**: [https://python.langchain.com/](https://python.langchain.com/)

### **LangChain Community**
- **Version**: 0.3.29+
- **Purpose**: Community-maintained integrations
- **Key Features**:
  - Additional document loaders
  - Extended vector store support
  - Community-contributed tools
- **Documentation**: [https://python.langchain.com/docs/integrations/](https://python.langchain.com/docs/integrations/)

### **LangGraph**
- **Version**: 0.6.6+
- **Purpose**: Complex workflow orchestration
- **Key Features**:
  - Stateful workflows
  - Conditional routing
  - Parallel processing
  - Error handling and recovery
- **Documentation**: [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)

## 🤖 AI Models & Providers

### **Google Generative AI (Gemini)**
- **Version**: 0.8.5+
- **Purpose**: Primary LLM provider for generation and embeddings
- **Models Used**:
  - **Chat Model**: `gemini-2.5-flash` (generation)
  - **Embedding Model**: `models/embedding-001` (embeddings)
- **Key Features**:
  - High-performance text generation
  - Multimodal capabilities
  - Cost-effective pricing
  - Reliable API with good uptime
- **Documentation**: [https://ai.google.dev/](https://ai.google.dev/)

### **LangChain Google GenAI Integration**
- **Version**: 2.0.10+
- **Purpose**: Seamless integration between LangChain and Google Gemini
- **Key Features**:
  - `ChatGoogleGenerativeAI` for chat completions
  - `GoogleGenerativeAIEmbeddings` for vector embeddings
  - Automatic retry and error handling
  - Streaming support
- **Documentation**: [https://python.langchain.com/docs/integrations/llms/google_generative_ai](https://python.langchain.com/docs/integrations/llms/google_generative_ai)

## 🗄️ Vector Database

### **ChromaDB**
- **Version**: 1.0.20+
- **Purpose**: Vector database for similarity search and document storage
- **Key Features**:
  - In-memory and persistent storage options
  - Efficient similarity search
  - Metadata filtering
  - Collection management
  - Easy integration with LangChain
- **Documentation**: [https://www.trychroma.com/](https://www.trychroma.com/)

## 🔍 Search & Retrieval

### **Tavily**
- **Version**: 0.7.11+
- **Purpose**: Web search integration for real-time information retrieval
- **Key Features**:
  - Real-time web search
  - Content extraction
  - Search result filtering
  - API rate limiting and optimization
- **Documentation**: [https://tavily.com/](https://tavily.com/)

### **LangChain Tavily Integration**
- **Version**: 0.2.11+
- **Purpose**: Seamless integration between LangChain and Tavily
- **Key Features**:
  - `TavilySearchResults` for web search
  - Automatic result formatting
  - Error handling and retry logic
- **Documentation**: [https://python.langchain.com/docs/integrations/tools/tavily_search](https://python.langchain.com/docs/integrations/tools/tavily_search)

## 🛠️ Development Tools

### **LangSmith**
- **Version**: 0.1.21+
- **Purpose**: Observability, debugging, and monitoring platform
- **Key Features**:
  - Request/response tracing
  - Performance monitoring
  - Debug information
  - Chain visualization
  - A/B testing support
- **Documentation**: [https://smith.langchain.com/](https://smith.langchain.com/)

### **Jupyter Notebooks**
- **Purpose**: Interactive development and learning environment
- **Key Features**:
  - Code execution and visualization
  - Markdown documentation
  - Interactive widgets
  - Rich output display
- **Documentation**: [https://jupyter.org/](https://jupyter.org/)


## 📊 Data Processing

### **BeautifulSoup4**
- **Version**: 4.13.5+
- **Purpose**: Web scraping and HTML/XML parsing
- **Key Features**:
  - HTML/XML parsing
  - Content extraction
  - Tag filtering
  - Clean text extraction
- **Documentation**: [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)

### **NumPy**
- **Version**: 2.3.2+
- **Purpose**: Numerical computing and array operations
- **Key Features**:
  - Vector operations
  - Mathematical functions
  - Array manipulation
  - Performance optimization
- **Documentation**: [https://numpy.org/](https://numpy.org/)

## 🔧 Utilities

### **TikToken**
- **Version**: 0.11.0+
- **Purpose**: Token counting and text processing
- **Key Features**:
  - Accurate token counting
  - Multiple encoding support
  - Text chunking optimization
  - Cost estimation
- **Documentation**: [https://github.com/openai/tiktoken](https://github.com/openai/tiktoken)

### **Python-dotenv**
- **Version**: 1.1.1+
- **Purpose**: Environment variable management
- **Key Features**:
  - .env file loading
  - Environment variable parsing
  - Secure credential management
  - Development/production configuration
- **Documentation**: [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)

### **Pydantic**
- **Version**: 2.0.0+
- **Purpose**: Data validation and settings management
- **Key Features**:
  - Type validation
  - Data serialization
  - Settings management
  - Error handling
- **Documentation**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

## 🔒 Security & Configuration

### **Environment Management**
- **External Credentials**: `$HOME/Documents/LangGraph-Credentials/.env.local`
- **Security**: No hardcoded credentials in repository
- **Git Protection**: Comprehensive `.gitignore` for sensitive files

### **API Key Management**
- **Google Gemini API**: Primary LLM and embedding provider
- **LangSmith API**: Optional tracing and monitoring
- **Tavily API**: Web search capabilities

## 📦 Installation

All dependencies are managed through `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🔄 Version Compatibility

This project is tested with:
- **Python**: 3.13+
- **LangChain**: 0.3.27+
- **Google Generative AI**: 0.8.5+
- **ChromaDB**: 1.0.20+

## 🚀 Performance Considerations

### **Optimization Strategies**
- **Batch Processing**: Efficient handling of large document sets
- **Caching**: Vector store caching for repeated queries
- **Streaming**: Real-time response generation
- **Parallel Processing**: Concurrent document processing

### **Scalability Features**
- **Modular Design**: Easy to scale individual components
- **Cloud Integration**: Ready for cloud deployment
- **Database Options**: Support for various vector databases
- **Load Balancing**: Built-in retry and error handling

## 🔧 Development Workflow

1. **Local Development**: Jupyter notebooks for experimentation
2. **Version Control**: Git for code management
3. **Testing**: Interactive testing in notebooks
4. **Monitoring**: LangSmith for production monitoring

## 📚 Additional Resources

- **LangChain Documentation**: [https://python.langchain.com/](https://python.langchain.com/)
- **Google AI Documentation**: [https://ai.google.dev/](https://ai.google.dev/)
- **ChromaDB Documentation**: [https://docs.trychroma.com/](https://docs.trychroma.com/)

---

*This tech stack is designed for production-ready RAG applications with a focus on scalability, maintainability, and ease of use.*
