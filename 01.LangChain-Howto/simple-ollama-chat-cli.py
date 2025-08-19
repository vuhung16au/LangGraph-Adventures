import json
from pathlib import Path
from typing import List, Dict

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


# ---------- Constants ----------
MODEL_NAME = "llama3.1:8b-instruct-q8_0"


def find_project_root() -> Path:
    """
    Resolve the project root directory.

    Assumes this script lives under the project folder and returns the parent
    directory of this file's folder (repo root in this project layout).
    """
    this_file = Path(__file__).resolve()
    return this_file.parents[1]


def history_file_path() -> Path:
    return find_project_root() / "chat_history.json"


def load_chat_history() -> List[Dict[str, str]]:
    file_path = history_file_path()
    if not file_path.exists():
        return []
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            valid_messages = []
            for item in data:
                if isinstance(item, dict) and "role" in item and "content" in item:
                    if item["role"] in {"user", "assistant"} and isinstance(item["content"], str):
                        valid_messages.append({"role": item["role"], "content": item["content"]})
            return valid_messages
        return []
    except Exception:
        return []


def save_chat_history(history: List[Dict[str, str]]) -> None:
    file_path = history_file_path()
    try:
        file_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        # Silently ignore write errors to avoid interrupting chat
        pass


def format_history_for_system(history: List[Dict[str, str]]) -> str:
    if not history:
        return (
            "You are a helpful AI assistant. Maintain a friendly tone and answer clearly."
        )
    lines = [
        "You are a helpful AI assistant. Below is the previous conversation history to maintain context. "
        "Use it to understand ongoing topics, preferences, and references."
    ]
    for message in history:
        role = "User" if message["role"] == "user" else "Assistant"
        content = message["content"].strip()
        lines.append(f"{role}: {content}")
    lines.append("Continue the conversation, referring to the relevant parts of the history when helpful.")
    return "\n".join(lines)


def stream_response(model: ChatOllama, system_text: str, user_input: str, console: Console) -> str:
    messages = [
        SystemMessage(system_text),
        HumanMessage(user_input),
    ]

    response_accumulator: str = ""
    assistant_title = Text("Assistant", style="bold green")

    # Live rendering area updated as chunks stream in
    with Live(
        Panel(Text("", style="bold green"), title=assistant_title, border_style="green"),
        refresh_per_second=24,
        console=console,
    ) as live:
        try:
            for chunk in model.stream(messages):
                # chunk is an AIMessageChunk; accumulate text
                text_piece = getattr(chunk, "content", "")
                if not isinstance(text_piece, str):
                    continue
                response_accumulator += text_piece
                live.update(Panel(Text(response_accumulator, style="bold green"), title=assistant_title, border_style="green"))
        except Exception as e:
            # Provide user-friendly diagnostics
            error_message = str(e).lower()
            if "connection" in error_message and ("refused" in error_message or "failed" in error_message):
                raise click.ClickException(
                    "Cannot reach Ollama server. Make sure it is running (try: 'ollama serve')."
                )
            if "no such model" in error_message or "not found" in error_message:
                raise click.ClickException(
                    f"Model not found: {MODEL_NAME}. Install it with: 'ollama pull {MODEL_NAME}'."
                )
            raise click.ClickException(f"Unexpected error while streaming response: {e}")

    console.print()  # newline after live panel
    return response_accumulator


@click.command()
@click.option("--temperature", default=0.2, show_default=True, help="Sampling temperature for the model.")
def chat(temperature: float) -> None:
    """
    Real-time streaming chat CLI with a local Ollama model using LangChain.
    """
    console = Console()

    # Header
    console.print(
        Panel(
            Text(
                f"LangChain × Ollama Streaming Chat\nModel: {MODEL_NAME}",
                style="bold white",
                justify="center",
            ),
            border_style="cyan",
        )
    )

    # Load persisted history
    history: List[Dict[str, str]] = load_chat_history()
    if history:
        console.print(Panel(Text("Loaded previous chat history. Context will be applied.", style="yellow"), border_style="yellow"))
    else:
        console.print(Panel(Text("Starting a new conversation.", style="cyan"), border_style="cyan"))

    # Initialize model
    try:
        model = ChatOllama(model=MODEL_NAME, temperature=temperature)
    except Exception as e:
        raise click.ClickException(f"Failed to initialize Ollama model: {e}")

    console.print(Text("Type 'exit', 'quit', or press Ctrl-C to leave.\n", style="dim"))

    # Chat loop
    while True:
        try:
            user_input = click.prompt("You", type=str, default="", show_default=False)
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        normalized = user_input.strip()
        if normalized.lower() in {"exit", "quit", ":q"}:
            break
        if not normalized:
            continue

        # Show user message
        console.print(Panel(Text(normalized, style="bold cyan"), title=Text("You", style="bold cyan"), border_style="cyan"))

        # Compose system prompt with prior context
        system_text = format_history_for_system(history)

        # Stream assistant response
        assistant_response = stream_response(model, system_text, normalized, console)

        # Persist to history
        history.append({"role": "user", "content": normalized})
        history.append({"role": "assistant", "content": assistant_response})
        save_chat_history(history)

    console.print(Panel(Text("Goodbye!", style="bold magenta"), border_style="magenta"))


if __name__ == "__main__":
    chat()


