## Simple Ollama Chat (CLI)

Interactive streaming chat in your terminal using a local Ollama model via LangChain.

### Prerequisites

- **Python**: 3.10+
- **Ollama**: Install and run [Ollama](https://ollama.com) locally
- **Model**: Pull the model used by the script

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

### Run

```bash
python 01.LangChain-Howto/simple-ollama-chat-cli.py --temperature 0.2
```

- **temperature** controls randomness (0.0 = deterministic, 1.0 = creative). Default is 0.2.
- Exit with `Ctrl-C`, or type `exit` / `quit`.

### What this script does

- Streams the model’s response chunk-by-chunk with a live-updating panel.
- Persists conversation to `chat_history.json` at the repo root to keep context across runs.

To clear history, delete the file:

```bash
rm -f chat_history.json
```

To change the model, edit `MODEL_NAME` in `01.LangChain-Howto/simple-ollama-chat-cli.py`.

### Troubleshooting

- **Connection refused/failed**: Ensure the Ollama server is running: `ollama serve`.
- **Model not found**: Pull it first: `ollama pull llama3.1:8b-instruct-q8_0`.
- **Slow/laggy output**: Lower `--temperature` or try a smaller/faster model.

### Deploy/Distribute

- **Another machine (local network or remote)**:
  - Install Python and [Ollama](https://ollama.com)
  - `git clone` the repo (or copy the folder)
  - Create a venv and `pip install -r requirements.txt`
  - Pull the model and start `ollama serve`
  - Run the script as above

- **Background process** (optional):
  - Use a terminal multiplexer like `tmux` or `screen`, or:
  ```bash
  nohup python 01.LangChain-Howto/simple-ollama-chat-cli.py --temperature 0.2 >/tmp/cli-chat.log 2>&1 &
  ```


