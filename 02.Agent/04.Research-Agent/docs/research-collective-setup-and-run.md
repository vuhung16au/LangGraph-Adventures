# Research Collective - Setup and Run Guide

A comprehensive guide to setting up and running the Research Collective, a sophisticated multi-agent research system built with LangGraph and powered by Google Gemini.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [API Keys Configuration](#api-keys-configuration)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Understanding the System](#understanding-the-system)
- [Troubleshooting](#troubleshooting)
- [Rate Limiting & Best Practices](#rate-limiting--best-practices)

## 🎯 Overview

The Research Collective is an advanced AI research system that:

- **Creates AI analyst teams** with different perspectives and expertise
- **Conducts parallel interviews** using multiple AI agents
- **Gathers information** from web search and Wikipedia
- **Synthesizes findings** into comprehensive research reports
- **Supports human feedback** to refine the research process

### Key Features

- 🤖 **Multi-Agent Architecture**: Specialized AI analysts with unique perspectives
- 🔄 **Parallel Processing**: Simultaneous interviews using LangGraph's Send API
- 👥 **Human-in-the-Loop**: Interactive feedback to improve analyst teams
- 🔍 **Multi-Source Research**: Web search (Tavily) + Wikipedia integration
- 📊 **Structured Reports**: Professional reports with citations and formatting
- 🧠 **Memory Management**: Conversation state and checkpoint persistence
- 📈 **Observability**: LangSmith integration for tracing and monitoring
- ⚡ **Rate Limiting**: Built-in protection against API quota limits

## 🔧 Prerequisites

### System Requirements

- **Python**: 3.13 or higher
- **Operating System**: macOS, Linux, or Windows
- **Memory**: At least 4GB RAM recommended
- **Storage**: 2GB free space for dependencies

### Required API Keys

1. **Google Gemini API Key** (Primary LLM)
2. **Tavily API Key** (Web search)
3. **LangSmith API Key** (Optional - for tracing)

## 🌍 Environment Setup

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd 04.Research-Agent

# Or download and extract the project files
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python3.13 -m venv .venv

# On Windows, use:
# python -m venv .venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

You should see `(.venv)` in your command prompt, indicating the virtual environment is active.

## 🔑 API Keys Configuration

### Create Environment File

Create a `.env.local` file in your credentials directory:

```bash
# Create the credentials directory if it doesn't exist
mkdir -p ~/Documents/LangGraph-Credentials

# Create the environment file
touch ~/Documents/LangGraph-Credentials/.env.local
```

### Add Your API Keys

Edit `~/Documents/LangGraph-Credentials/.env.local` and add:

```bash
# Required API Keys
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
LANGSMITH_API_KEY=your_langsmith_api_key_here
```

### Getting API Keys

#### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" and create a new key
4. Copy the key to your `.env.local` file

#### Tavily API Key
1. Visit [Tavily](https://tavily.com/)
2. Sign up for a free account
3. Navigate to your dashboard and copy the API key
4. Add it to your `.env.local` file

#### LangSmith API Key (Optional)
1. Visit [LangSmith](https://smith.langchain.com/)
2. Create an account
3. Go to Settings → API Keys
4. Create a new API key and add it to your `.env.local` file

## 📦 Installation

### 1. Update pip

```bash
pip install --upgrade pip
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes:
- `langgraph` - Multi-agent orchestration framework
- `langchain_google_genai` - Google Gemini integration
- `langchain_community` - Community tools and integrations
- `langchain_core` - Core LangChain functionality
- `tavily-python` - Web search API
- `wikipedia` - Wikipedia search
- `python-dotenv` - Environment variable management
- `tenacity` - Retry logic for API calls
- `jupyter` - Jupyter notebook environment

### 3. Verify Installation

```bash
python -c "
import langgraph
import langchain_google_genai
import tavily
print('✅ All dependencies installed successfully!')
"
```

## 🚀 Running the Project

### Method 1: Jupyter Notebook (Recommended)

1. **Start Jupyter Lab:**
```bash
jupyter lab
```

2. **Open the notebook:**
   - Navigate to `Research-Collective.ipynb`
   - Click to open it

3. **Run cells sequentially:**
   - Start with the setup cells (cells 1-6)
   - Follow the notebook's natural flow
   - The system will guide you through the process

### Method 2: Jupyter Notebook (Alternative)

```bash
jupyter notebook
```

### Method 3: VS Code with Jupyter Extension

1. Open VS Code
2. Install the Jupyter extension
3. Open `Research-Collective.ipynb`
4. Select the Python interpreter from your virtual environment
5. Run cells using Shift+Enter

## 🧠 Understanding the System

### Workflow Overview

1. **Setup & Configuration**
   - Load environment variables
   - Initialize LLM with rate limiting
   - Set up LangSmith tracing

2. **Analyst Generation**
   - Create AI analyst personas
   - Human feedback loop for refinement
   - Finalize analyst team

3. **Parallel Interviews**
   - Each analyst conducts interviews
   - Web search and Wikipedia research
   - Multi-turn conversations

4. **Report Synthesis**
   - Combine interview findings
   - Generate structured reports
   - Add citations and sources

### Key Components

#### Rate Limiting System
- **Conservative limits**: 10 requests/minute (below Gemini's 15/minute free tier)
- **Automatic queuing**: Waits when approaching limits
- **Retry logic**: Exponential backoff for failed requests

#### Multi-Agent Architecture
- **Analyst personas**: Different perspectives and expertise
- **Parallel execution**: Simultaneous interviews using Send API
- **State management**: Persistent conversation memory

#### Research Sources
- **Tavily search**: Real-time web information
- **Wikipedia**: Comprehensive knowledge base
- **Structured queries**: Optimized search strategies

## 🔧 Troubleshooting

### Common Issues

#### 1. Virtual Environment Problems

**Can't activate virtual environment:**
```bash
# Check current directory
pwd
# Should show: /path/to/04.Research-Agent

# Recreate virtual environment
rm -rf .venv
python3.13 -m venv .venv
source .venv/bin/activate
```

**Packages not installing:**
```bash
# Update pip first
pip install --upgrade pip

# Install packages individually if needed
pip install langgraph
pip install langchain_google_genai
pip install python-dotenv
```

#### 2. API Key Issues

**Environment variables not loading:**
```bash
# Check if .env.local exists
ls -la ~/Documents/LangGraph-Credentials/.env.local

# Verify file contents (without exposing keys)
head -1 ~/Documents/LangGraph-Credentials/.env.local
```

**API key errors:**
- Verify keys are correctly set in `.env.local`
- Check API key validity in respective dashboards
- Ensure sufficient credits/quota

#### 3. Rate Limiting Issues

**Getting quota exceeded errors:**
- The system includes built-in rate limiting
- If you still hit limits, consider upgrading your Gemini API plan
- Check your usage in the Google AI Studio dashboard

#### 4. Import Errors

**Module not found errors:**
```bash
# Ensure virtual environment is activated
which python
# Should show: /path/to/.venv/bin/python

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

Enable debug logging by modifying the notebook:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ⚡ Rate Limiting & Best Practices

### Built-in Protection

The system includes comprehensive rate limiting:

- **Request throttling**: Maximum 10 requests/minute
- **Automatic queuing**: Waits when approaching limits
- **Retry logic**: Handles temporary failures gracefully
- **Error handling**: Clear feedback on quota issues

### Best Practices

1. **Start small**: Begin with 2-3 analysts to test the system
2. **Monitor usage**: Check your API dashboards regularly
3. **Plan ahead**: For large research projects, consider API plan upgrades
4. **Use human feedback**: Leverage the human-in-the-loop features
5. **Save progress**: The system maintains state between runs

### API Usage Optimization

- **Batch operations**: The system automatically parallelizes where possible
- **Efficient prompts**: Optimized for minimal token usage
- **Smart caching**: Reuses results when appropriate
- **Graceful degradation**: Continues working even with partial failures

## 📊 Monitoring & Observability

### LangSmith Integration

If you've set up LangSmith:

1. **Tracing**: All API calls are automatically traced
2. **Performance**: Monitor response times and success rates
3. **Debugging**: Detailed logs for troubleshooting
4. **Analytics**: Usage patterns and optimization insights

### Built-in Logging

The system provides:
- **Rate limit notifications**: When waiting for quota
- **Retry attempts**: Progress on failed requests
- **Error details**: Specific failure reasons
- **Success confirmations**: When operations complete

## 🎯 Example Usage

### Basic Research Session

```python
# 1. Set up parameters
max_analysts = 3
topic = "The benefits of adopting LangGraph as an agent framework"
thread = {"configurable": {"thread_id": "research_session_1"}}

# 2. Run the research process
for event in graph.stream(
    {"topic": topic, "max_analysts": max_analysts}, 
    thread, 
    stream_mode="values"
):
    # Process results as they come in
    if 'analysts' in event:
        print(f"Generated {len(event['analysts'])} analysts")
    
    if 'final_report' in event:
        print("Research complete!")
        print(event['final_report'])
```

### Customizing the Research

```python
# Adjust number of analysts
max_analysts = 5  # More perspectives

# Change research topic
topic = "The future of AI in healthcare"

# Use different thread ID for new session
thread = {"configurable": {"thread_id": "healthcare_ai_research"}}
```

## 🔄 Deactivating Environment

When finished:

```bash
deactivate
```



---

**Happy Researching! 🚀**

The Research Collective is designed to make AI-powered research accessible and reliable. With proper setup and understanding of the rate limiting features, you'll be able to conduct comprehensive research on any topic efficiently and effectively.
