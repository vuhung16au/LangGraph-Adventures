import json
from pathlib import Path
from typing import List, Dict, Iterable

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


MODEL_NAME = "llama3.1:8b-instruct-q8_0"


def find_project_root() -> Path:
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


@st.cache_resource(show_spinner=False)
def get_model(temperature: float) -> ChatOllama:
    return ChatOllama(model=MODEL_NAME, temperature=temperature)


def stream_generator(model: ChatOllama, system_text: str, user_input: str) -> Iterable[str]:
    messages = [
        SystemMessage(system_text),
        HumanMessage(user_input),
    ]
    for chunk in model.stream(messages):
        text = getattr(chunk, "content", "")
        if text:
            yield text


st.set_page_config(page_title="LangChain × Ollama (Streaming Chat)", page_icon="💬", layout="centered")
st.title("LangChain × Ollama (Streaming Chat)")
st.caption(f"Model: {MODEL_NAME}")

with st.sidebar:
    st.markdown("### Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    clear = st.button("Clear chat history", use_container_width=True)
    if clear:
        st.session_state.pop("history", None)
        try:
            history_file_path().unlink(missing_ok=True)
        except Exception:
            pass
        st.rerun()

if "history" not in st.session_state:
    st.session_state.history = load_chat_history()

for m in st.session_state.history:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

user_input = st.chat_input("Type your message")
if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        model = get_model(temperature)
    except Exception as e:
        st.error(f"Failed to initialize Ollama model: {e}")
        st.stop()

    system_text = format_history_for_system(st.session_state.history)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        collected = ""
        try:
            for piece in stream_generator(model, system_text, user_input):
                collected += piece
                placeholder.markdown(collected)
        except Exception as e:
            msg = str(e).lower()
            if "connection" in msg and ("refused" in msg or "failed" in msg):
                st.error("Cannot reach Ollama server. Make sure it is running (try: `ollama serve`).")
            elif "no such model" in msg or "not found" in msg:
                st.error(f"Model not found: {MODEL_NAME}. Install it with: `ollama pull {MODEL_NAME}`.")
            else:
                st.error(f"Unexpected error while streaming response: {e}")
            st.stop()

    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": collected})
    save_chat_history(st.session_state.history)


