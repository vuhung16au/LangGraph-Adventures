# Research Collective

A sophisticated multi-agent research system built with LangGraph that automates the research process through parallel AI analyst interviews and expert knowledge synthesis.

## Overview

The Research Collective creates a team of AI analysts who conduct parallel interviews with expert AIs to research any given topic, then synthesizes their findings into comprehensive reports. This system demonstrates advanced LangGraph concepts including:

- **Multi-agent orchestration** with parallel processing
- **Human-in-the-loop** feedback mechanisms
- **Memory management** and state persistence
- **Map-reduce patterns** for scalable research
- **Structured output generation** with proper citations

## Features

- 🤖 **Multi-Agent Architecture**: Creates specialized AI analysts with different perspectives
- 🔄 **Parallel Processing**: Conducts multiple interviews simultaneously using LangGraph's Send API
- 👥 **Human-in-the-Loop**: Allows human feedback to refine analyst teams before research begins
- 🔍 **Multi-Source Research**: Gathers information from web search (Tavily) and Wikipedia
- 📊 **Structured Reports**: Generates comprehensive reports with proper citations and formatting
- 🧠 **Memory Management**: Maintains conversation state and checkpoints
- 📈 **Observability**: Integrated with LangSmith for tracing and monitoring

## Documentation

For detailed information about the system, please refer to the comprehensive documentation:

- 📚 **[Tech Stack](docs/techstack.md)**: Complete list of technologies, frameworks, and tools used in the project
- 🔤 **[Key Terms](docs/key-terms.md)**: Glossary of key terms, concepts, and terminology used throughout the system
- 🏗️ **[Architecture](docs/architecture.md)**: High-level system architecture, components, and design patterns with diagrams
- 🔄 **[Flow](docs/flow.md)**: Detailed process flows, execution patterns, and workflow diagrams

## Prerequisites

- Python 3.13 or higher
- Gemini API key (Google AI Studio)
- Tavily API key (for web search)
- LangSmith API key (optional, for tracing)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd 04.Research-Agent
```

### 2. Create Python Virtual Environment

Create a virtual environment to isolate project dependencies:

```bash
python3.13 -m venv .venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**

```bash
source .venv/bin/activate
```

**On Windows:**

```bash
.venv\Scripts\activate
```

You should see `(.venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -U langgraph langchain_openai langchain_community langchain_core tavily-python wikipedia python-dotenv langchain_google_genai
```

### 5. Set Up Environment Variables

The notebook expects environment variables to be loaded from a `.env.local` file. You can either:

**Option A: Create a `.env.local` file in the project root:**

```bash
# Create .env.local file
cat > .env.local << EOF
GEMINI_API_KEY=your-gemini-api-key
TAVILY_API_KEY=your-tavily-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
EOF
```

**Option B: Set environment variables directly:**

```bash
# Required
export GEMINI_API_KEY="your-gemini-api-key"
export TAVILY_API_KEY="your-tavily-api-key"

# Optional (for tracing)
export LANGSMITH_API_KEY="your-langsmith-api-key"
export LANGSMITH_TRACING="true"
export LANGSMITH_PROJECT="research-collective"
```

## Usage

### Running the Jupyter Notebook

1. Start Jupyter Lab or Jupyter Notebook:

```bash
jupyter lab
# or
jupyter notebook
```

2. Open `Research-Collective.ipynb`

3. Run the cells sequentially to:
   - Set up the environment and API keys
   - Initialize the Gemini LLM model
   - Create analyst personas with human feedback
   - Conduct parallel interviews
   - Generate comprehensive research reports

### Example Usage

```python
# Input parameters
max_analysts = 3
topic = "The benefits of adopting LangGraph as an agent framework"
thread = {"configurable": {"thread_id": "1"}}

# Run the research process
for event in graph.stream({"topic": topic, "max_analysts": max_analysts}, thread, stream_mode="values"):
    # Process results...
```

## Project Structure

```text
04.Research-Agent/
├── Research-Collective.ipynb    # Main notebook with the research system
├── Prompt.md                    # Project prompts and instructions
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE.md                   # Project license
├── docs/                        # Documentation directory
│   ├── techstack.md            # Technology stack and dependencies
│   ├── key-terms.md            # Glossary of key terms and concepts
│   ├── architecture.md         # System architecture and design patterns
│   └── flow.md                 # Process flows and workflow diagrams
└── .venv/                       # Python virtual environment (created during setup)
```

## Key Components

### 1. LLM Setup

- Uses Google's Gemini 2.0 Flash Experimental model
- Simple, clean initialization without complex retry logic
- Integrated with LangChain for structured output generation

### 2. Analyst Generation

- Creates multiple AI analyst personas with different perspectives
- Supports human feedback to refine the analyst team
- Uses structured output for consistent analyst profiles

### 3. Interview System

- Multi-turn conversations between analysts and expert AIs
- Parallel execution using LangGraph's Send API
- Information gathering from multiple sources (Tavily web search and Wikipedia)

### 4. Report Generation

- Synthesizes interview findings into structured memos
- Combines all insights into comprehensive reports
- Maintains proper citations and source attribution

## API Keys Setup

### Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create an account and generate an API key
3. Set the `GEMINI_API_KEY` environment variable

### Tavily API Key

1. Visit [Tavily](https://tavily.com/)
2. Sign up and get your API key
3. Set the `TAVILY_API_KEY` environment variable

### LangSmith API Key (Optional)

1. Visit [LangSmith](https://smith.langchain.com/)
2. Create an account and get your API key
3. Set the `LANGSMITH_API_KEY` environment variable for tracing
