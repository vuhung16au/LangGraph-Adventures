## Simple Ollama Chat (Streamlit UI)

A minimal web UI for chatting with a local Ollama model using LangChain and Streamlit.

### Prerequisites

- **Python**: 3.10+
- **Ollama**: Install and run [Ollama](https://ollama.com)
- **Model**: Pull the model used by the app

```bash
ollama pull llama3.1:8b-instruct-q8_0
ollama serve
```

### Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Run (local)

```bash
streamlit run 01.LangChain-Howto/simple-ollama-chat-streamlit.py
```

Then open the URL printed in the terminal (default `http://localhost:8501`).

### Features

- Streaming responses rendered live in the chat panel
- Temperature slider in the sidebar
- “Clear chat history” button (persists history to `chat_history.json` at the repo root)

To reset history manually:

```bash
rm -f chat_history.json
```

To change the model, edit `MODEL_NAME` in `01.LangChain-Howto/simple-ollama-chat-streamlit.py`.

### Troubleshooting

- **Connection refused/failed**: Start the Ollama server with `ollama serve`.
- **Model not found**: Pull it with `ollama pull llama3.1:8b-instruct-q8_0`.
- **Watchdog warning**: Optional but recommended for faster reloads:
  ```bash
  xcode-select --install
  pip install watchdog
  ```

### Deploy

This app expects a local Ollama server on the same host. Deploy options:

- **Self-hosted VM/server** (same steps as local):
  - Install Python and [Ollama](https://ollama.com)
  - Pull the model and run `ollama serve`
  - Create a venv and `pip install -r requirements.txt`
  - Launch the app:
    ```bash
    streamlit run 01.LangChain-Howto/simple-ollama-chat-streamlit.py --server.port 8501 --server.address 0.0.0.0
    ```
  - Reverse proxy (optional) with Nginx/Caddy for TLS and a nicer domain.

- **Container (optional)**: If you containerize, you must also provide Ollama in the host or container. Typical pattern is running Ollama on the host and connecting from the container to `host.docker.internal` (macOS) or the host IP.

> Note: Cloud PaaS (Streamlit Community Cloud, etc.) won’t work unless they can access an Ollama server; these services usually block local network access, so prefer a VM where you control both Streamlit and Ollama.


