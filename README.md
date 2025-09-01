# LangGraph-Adventures 🚀

A comprehensive learning journey through LangChain, LangGraph, and modern AI application development. This project serves as a hands-on exploration of building intelligent AI systems using cutting-edge technologies.

## 📚 Project Overview

LangGraph-Adventures is a structured learning repository that guides you through building various AI applications using LangChain and LangGraph. From basic concepts to advanced implementations, this project covers everything from simple chatbots to complex RAG (Retrieval-Augmented Generation) systems and intelligent agents.

## 🎯 What You'll Learn

- **LangChain Fundamentals**: Understanding the core concepts and architecture
- **RAG Systems**: Building retrieval-augmented generation applications from scratch
- **AI Agents**: Creating intelligent agents with tool calling and reasoning capabilities
- **Streamlit Applications**: Building user-friendly interfaces for AI systems
- **Local Model Integration**: Working with Ollama and local LLMs
- **Production-Ready Systems**: Best practices for deploying AI applications

## 🏗️ Project Structure

### 📖 00.Intro-LangChain/
Introduction to LangChain ecosystem and setup guides:
- LangChain architecture and key concepts
- Installation and environment setup
- Ollama model configuration
- Comparison studies between different models

### 🔧 01.LangChain-Howto/
Practical tutorials and implementations:
- **Structured Responses**: Working with Pydantic models and structured outputs
- **RAG System**: Complete RAG implementation with URL fetching and vector storage
- **Chat Models & Tools**: Building agents that can call external tools
- **Streaming**: Real-time response streaming with Streamlit

### 🤖 02.Agent/
Advanced agent development and applications:
- **Hello World Agents**: Basic agent implementations
- **News Dashboard**: AI-powered news aggregation with Streamlit
- **RAG from Scratch**: Comprehensive 5-part tutorial series on building production RAG systems

## 🚀 Key Features

### 🔍 RAG Systems
- URL content fetching and processing
- Vector storage with ChromaDB
- Intelligent document retrieval
- Multi-query enhancement techniques
- Advanced indexing strategies
- Performance optimization

### 📰 News Dashboard
- Real-time news aggregation
- AI-powered content categorization
- Beautiful Streamlit interface
- Multiple news categories (AI, Politics, Sports, etc.)
- Source attribution and links

### 🛠️ Agent Capabilities
- Tool calling and function execution
- Multi-step reasoning workflows
- Human-in-the-loop interactions
- Stateful conversation management
- Error handling and recovery

## 🛠️ Technology Stack

- **LangChain & LangGraph**: Core AI framework and orchestration
- **Google Gemini**: Advanced LLM for generation and embeddings
- **Ollama**: Local model inference and management
- **ChromaDB**: Vector database for similarity search
- **Streamlit**: Web application framework
- **Tavily**: Web search and content retrieval
- **Pydantic**: Data validation and structured outputs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- Google API key (for Gemini)
- Tavily API key (for web search)

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd LangGraph-Adventures

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env
# Edit .env with your API keys
```

### Running Examples

#### RAG System
```bash
cd 01.LangChain-Howto/02.Build-a-RAG
python rag_cli.py build -u "https://example.com" -m "llama3.1:8b-instruct-q8_0"
python rag_cli.py query -q "Your question here"
```

#### News Dashboard
```bash
cd 02.Agent/02.Agent.Latest-News-Events-streamlit
streamlit run app.py
```

## 📖 Learning Path

1. **Start with Basics**: Read through `00.Intro-LangChain/` for foundational concepts
2. **Build Simple Systems**: Work through `01.LangChain-Howto/` tutorials
3. **Create Advanced Agents**: Explore `02.Agent/` for complex applications
4. **Deploy Applications**: Use the provided Streamlit apps as templates

## 🔧 Configuration

The project uses environment variables for configuration. See `env.example` for all available options:

- **Ollama Configuration**: Model selection and server settings
- **Vector Store**: Database type and embedding model settings
- **API Keys**: Google Gemini, Tavily, and other service credentials
- **Performance**: Token limits, temperature, and chunking parameters



## 📄 License

This project is open source and available under the [LICENSE](LICENSE) file.

## 🎓 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)

---

**Happy Learning! 🎉**

Build amazing AI applications with LangChain and LangGraph!