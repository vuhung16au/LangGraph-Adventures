# Tech Stack

This document outlines the technologies, frameworks, and tools used in the Research Collective project.

## Core Framework

### LangGraph
- **Purpose**: Multi-agent orchestration and workflow management
- **Version**: Latest stable
- **Usage**: 
  - State management and graph-based execution
  - Human-in-the-loop interactions
  - Parallel processing with Send API
  - Memory management and checkpoints

### LangChain
- **Purpose**: LLM integration and chain orchestration
- **Components Used**:
  - `langchain_core`: Core abstractions and base classes
  - `langchain_community`: Community integrations and tools
  - `langchain_openai`: OpenAI model integrations (for compatibility)
  - `langchain_google_genai`: Google Gemini model integration

## Language Models

### Google Gemini
- **Model**: `gemini-2.0-flash`
- **Provider**: Google AI Studio
- **Usage**: Primary LLM for all text generation tasks
- **Configuration**: Temperature set to 0 for consistent outputs

## Data Sources & APIs

### Tavily Search
- **Purpose**: Web search and information retrieval
- **Integration**: `tavily-python` package
- **Usage**: Real-time web search for research data
- **Configuration**: Max 3 results per query

### Wikipedia
- **Purpose**: Encyclopedic knowledge base
- **Integration**: `langchain_community.document_loaders.WikipediaLoader`
- **Usage**: Structured information retrieval
- **Configuration**: Max 2 documents per query

## Development Environment

### Python
- **Version**: 3.13+
- **Virtual Environment**: `.venv` directory
- **Package Management**: pip

### Jupyter Notebook
- **Purpose**: Interactive development and execution
- **Extensions**: IPython for enhanced functionality
- **Notebook**: `Research-Collective.ipynb`

## Environment & Configuration

### Environment Variables
- **Management**: `python-dotenv` package
- **Configuration File**: `.env.local`
- **Variables**:
  - `GEMINI_API_KEY`: Google AI Studio API key
  - `TAVILY_API_KEY`: Tavily search API key
  - `LANGSMITH_API_KEY`: LangSmith tracing API key (optional)

### Observability
- **LangSmith**: Tracing and monitoring
- **Project**: `research-collective`
- **Features**: Request tracing, performance monitoring

## Data Structures & Models

### Pydantic
- **Purpose**: Data validation and serialization
- **Usage**: 
  - Analyst model definitions
  - Search query structures
  - State management

### TypedDict
- **Purpose**: Type hints for state management
- **Usage**: Graph state definitions

## Error Handling & Resilience

### Tenacity
- **Purpose**: Retry logic and error handling
- **Usage**: API call resilience (if needed)

### Google API Core
- **Purpose**: Google API client libraries
- **Usage**: Gemini API integration

## Project Structure

### Documentation
- **Format**: Markdown files
- **Location**: `docs/` directory
- **Files**: Architecture, flow, tech stack, key terms

### Configuration Files
- **Requirements**: `requirements.txt`
- **Environment**: `.env.local`
- **Git**: `.gitignore`

## Dependencies Summary

```text
Core Framework:
├── langgraph (multi-agent orchestration)
├── langchain_core (core abstractions)
├── langchain_community (integrations)
├── langchain_google_genai (Gemini integration)

Data Sources:
├── tavily-python (web search)
├── wikipedia (knowledge base)

Development:
├── jupyter (notebooks)
├── ipython (enhanced Python)
├── python-dotenv (environment management)

Utilities:
├── tenacity (retry logic)
├── google-api-core (Google APIs)
```

## API Keys Required

1. **Gemini API Key** (Required)
   - Source: Google AI Studio
   - Usage: LLM inference

2. **Tavily API Key** (Required)
   - Source: Tavily.com
   - Usage: Web search functionality

3. **LangSmith API Key** (Optional)
   - Source: LangSmith
   - Usage: Tracing and monitoring
