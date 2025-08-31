# Setup and Run Guide

This project runs in a Python virtual environment and loads all API keys from an external `.env.local` file. No keys are hardcoded in notebooks.

## Prerequisites

- macOS with zsh (default)
- Python 3.13 (project venv already present)
- A Google Gemini API key in your credentials file

Credentials file location (do not move or commit):

- `$HOME/Documents/LangGraph-Credentials/.env.local`

Expected keys inside that file (examples only, values omitted):

- `GEMINI_API_KEY=...`
- `GOOGLE_API_KEY=...` (optional; mirrored from GEMINI_API_KEY by notebooks)
- `LANGCHAIN_API_KEY=...` (optional, for LangSmith)
- `LANGSMITH_TRACING=true` (optional)
- `TAVILY_API_KEY=...` (optional)

## Environment

- Project venv: `$HOME/Desktop/LangGraph-Adventures/02.Agent/03.RAG-from-scratch/.venv`
- Python executable: `$HOME/Desktop/LangGraph-Adventures/02.Agent/03.RAG-from-scratch/.venv/bin/python`

In VS Code, select this interpreter for the workspace.

## Install dependencies

The notebooks include a cell that runs `! pip install -r requirements.txt`. You can also install once from the venv:

- Using the project interpreter above, install from `requirements.txt`.

If you run into missing packages, re-run the install cell at the top of any notebook.

## Model configuration

- Default chat model: `gemini-2.5-flash` (set via `GEMINI_MODEL`)
- Default embedding model: `models/embedding-001` (Google Generative AI)

You can override the chat model by setting `GEMINI_MODEL` in your shell before starting Jupyter or directly in the first env cell of each notebook.

## How the notebooks load credentials

Each notebook's first code cell:

- Reads `$HOME/Documents/LangGraph-Credentials/.env.local` via `python-dotenv`
- Sets `GEMINI_API_KEY` and mirrors it to `GOOGLE_API_KEY`
- Optionally enables LangSmith via `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2`, `LANGCHAIN_ENDPOINT`
- Leaves logic unchanged; only provider and keys are swapped to Gemini

## Project Structure

The project consists of 5 progressive notebooks:

1. **`01-rag-basics.ipynb`** - Core RAG concepts and basic pipeline
2. **`02-query-enhancement.ipynb`** - Query optimization and enhancement
3. **`03-intelligent-routing.ipynb`** - Smart routing and classification
4. **`04-advanced-indexing.ipynb`** - Advanced indexing techniques
5. **`05-retrieval-optimization.ipynb`** - Performance optimization

## Tech Stack

- **[LangChain](https://python.langchain.com/)**: Core RAG framework and orchestration
- **[Google Gemini](https://ai.google.dev/)**: LLM for generation and embeddings
- **[ChromaDB](https://www.trychroma.com/)**: Vector database for similarity search
- **[LangSmith](https://smith.langchain.com/)**: Observability and debugging platform

For detailed technical specifications, see **[Tech Stack Documentation](techstack.md)**.

## Running the notebooks

1) Open the folder in VS Code and select the venv interpreter.
2) Open any notebook (e.g., `01-rag-basics.ipynb`).
3) Run the top "Install" cell if needed, then run cells in order.
4) Follow the notebooks sequentially for the complete learning experience.

## Learning Path

```
01-rag-basics.ipynb     → Understand core RAG concepts
         ↓
02-query-enhancement.ipynb → Optimize query processing
         ↓
03-intelligent-routing.ipynb → Add smart routing
         ↓
04-advanced-indexing.ipynb → Implement advanced indexing
         ↓
05-retrieval-optimization.ipynb → Optimize for production
```

## Notes

- Do not create or commit `.env.local` in this repo. The notebooks read the file from `$HOME/Documents/LangGraph-Credentials/.env.local`.
- `.gitignore` already excludes secrets, venv, cache, and vector DB artifacts.
- The original RAG logic is unchanged; only the provider is switched to Gemini.
- All notebooks use Google Generative AI for both chat completions and embeddings.
- Vector database uses ChromaDB for efficient similarity search and document storage.
