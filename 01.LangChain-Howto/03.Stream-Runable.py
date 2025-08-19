#!/usr/bin/env python
# coding: utf-8

# ## LangChain How-to: Stream Runnables (Ollama)
# 
# This notebook shows how to stream with LangChain runnables using local `ollama` models, and how to work with streaming events. We use these models served by `ollama`:
# - `deepseek-r1:8b`
# - `llama3.1:8b-instruct-q8_0`
# - `qwen2.5:7b-instruct`
# 
# References:
# - LangChain How-to: Streaming (`python.langchain.com`) — see `Using Stream` and `Using Stream Events`.
# - Reference notebook: `streaming.ipynb` from the LangChain docs repository.
# 
# Prerequisites:
# - `ollama` is running locally and the models are pulled: `ollama pull deepseek-r1:8b`, `ollama pull llama3.1:8b-instruct-q8_0`, `ollama pull qwen2.5:7b-instruct`
# - Python packages installed: `pip install -r requirements.txt`
# 
# Tip:
# - You can switch models by changing the `MODEL` variable in the setup cell below.
# - Each section is broken into small steps with short runnable examples and plain-English explanations.
# 

# In[18]:


# Setup
# - Select an Ollama model by name
# - Import LangChain + langchain-ollama integrations
# - Quick utility to pretty-print streaming

# MODEL = "deepseek-r1:8b"  # change to: "llama3.1:8b-instruct-q8_0" or "qwen2.5:7b-instruct"
MODEL = "llama3.1:8b-instruct-q8_0" 

from typing import Iterable, Any

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableLambda


def print_stream(iterable: Iterable[Any]):
    """Print streaming chunks as they arrive, on one line."""
    for chunk in iterable:
        # Chunks from chat models are usually AIMessageChunks or strings
        print(getattr(chunk, "content", chunk), end="", flush=True)
    print()


# ### Using Stream
# 
# In this part, we stream the final outputs from runnables. We'll start with chat models (LLMs), then build simple chains, then show streamed inputs, and call out non-streaming components.
# 

# #### LLMs and Chat Models
# 
# Small steps:
# 1) Create a `ChatOllama` chat model bound to your `ollama` instance
# 2) Stream a simple prompt token-by-token
# 3) Try switching `MODEL`
# 
# Explanation:
# - `stream` yields chunks. For chat models, each chunk is an `AIMessageChunk` with `.content`.
# - Printing as chunks arrive makes UI responsive and reduces perceived latency.
# 

# In[19]:


chat = ChatOllama(model=MODEL, temperature=0.3)

print("Model:", MODEL)
print("Streaming response:\n")

print_stream(
    chat.stream([
        HumanMessage(content="Give a 1-sentence fun fact about Vietnamese coffee.")
    ])
)


# #### Chains
# 
# Small steps:
# 1) Build a simple prompt → chat chain with LCEL
# 2) Stream the chain output
# 3) Swap models and compare
# 
# Explanation:
# - LCEL composes components with `|`. Here: `prompt | chat`.
# - `chain.stream(input_dict)` yields `AIMessageChunk`s reflecting the chain's final output.
# 

# In[20]:


from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "Translate to Vietnamese: {text}")
])

chain = prompt | chat

print_stream(chain.stream({"text": "Good morning!"}))


# #### Working with Input Streams
# 
# Small steps:
# 1) Define a prompt that takes a single `input` field
# 2) Create an async generator that yields input chunks
# 3) Stream the chain output as the input arrives
# 
# Explanation:
# - `chain.astream({...})` supports async iterables as values. The chain produces output chunks as soon as it has enough input to generate.
# - This is useful for partial-input UX like live dictation.
# 

# In[21]:


import asyncio
from typing import AsyncIterable

# Reuse chat and define a prompt that consumes {input}
stream_prompt = ChatPromptTemplate.from_messages([
    ("system", "You produce concise helpful answers."),
    ("human", "Summarize as I type: {input}")
])
stream_chain = stream_prompt | chat

async def input_chunks() -> AsyncIterable[str]:
    parts = ["Today ", "we explore ", "LangChain streaming."]
    for p in parts:
        await asyncio.sleep(0.2)
        yield p

async def demo_streaming_input():
    async for chunk in stream_chain.astream({"input": input_chunks()}):
        print(getattr(chunk, "content", chunk), end="", flush=True)
    print()

# (Run inside a single orchestrated event loop at the end of the file)


# #### Non-streaming components
# 
# Small steps:
# 1) Create a synchronous `RunnableLambda` that does CPU-bound work (non-streaming)
# 2) Compose it before the chat model
# 3) Observe: the overall chain can't emit until the non-streaming step completes
# 
# Explanation:
# - Non-streaming parts act like buffers in your pipeline; place them early and keep them fast.
# - If you must include them, prefer small/quick transforms before the streaming model.
# 

# In[22]:


import time

# Non-streaming CPU-bound transform

def slow_upper(text: str) -> str:
    time.sleep(1.0)  # simulate work
    return text.upper()

pre = RunnableLambda(lambda x: {"text": slow_upper(x["text"])})
non_stream_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are concise."),
    ("human", "Rewrite politely: {text}")
])
non_stream_chain = pre | non_stream_prompt | chat

print_stream(non_stream_chain.stream({"text": "give me a hint about Hanoi food"}))


# ### Using Stream Events
# 
# `astream_events` lets you observe start/end/stream events for each runnable in a graph. This is useful for tracing, live UIs, and debugging.
# 

# #### Event Reference
# 
# Common event names include:
# - `on_chain_start`, `on_chain_stream`, `on_chain_end`
# - `on_chat_model_start`, `on_chat_model_stream`, `on_chat_model_end`
# - `on_tool_start`, `on_tool_end` (if using tools)
# 
# We will print a compact view of events.
# 

# In[23]:


import json

MAX_LEN = 120

def _safe(obj):
    """Recursively convert event payloads to JSON-serializable primitives.
    - Strings are trimmed
    - Objects are stringified if not serializable
    - AI/Human/System message-like objects use their `content` if present
    """
    try:
        if isinstance(obj, dict):
            return {k: _safe(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_safe(v) for v in obj]
        if isinstance(obj, str):
            return obj if len(obj) <= MAX_LEN else obj[:MAX_LEN] + "…"
        # Prefer `.content` if available (e.g., AIMessageChunk, HumanMessage)
        content = getattr(obj, "content", None)
        if isinstance(content, str):
            return _safe(content)
        # If it's already JSON-serializable, keep it
        json.dumps(obj)
        return obj
    except TypeError:
        rep = repr(obj)
        return rep if len(rep) <= MAX_LEN else rep[:MAX_LEN] + "…"


def show_event(e):
    name = e.get("event", e.get("name"))
    typ = e.get("type")
    meta = {k: v for k, v in e.items() if k in {"event", "name", "type", "tags", "RunName", "run_id"}}
    data = _safe(e.get("data"))
    print(json.dumps({"name": name, "type": typ, "meta": _safe(meta), "data": data}, ensure_ascii=False))


# #### Chat Model
# 
# Small steps:
# 1) Use `chat.astream_events` to observe token streaming
# 2) Print a filtered subset of fields for readability
# 
# Explanation:
# - Events include model start, streamed tokens, and end. This is great for building real-time UIs.
# 

# In[24]:


async def events_for_chat():
    async for e in chat.astream_events(
        [HumanMessage(content="List 3 must-try foods in Hanoi.")],
        version="v1",
    ):
        show_event(e)
# (Run inside a single orchestrated event loop at the end of the file)


# In[ ]:


if False:
    # Bind the function tools and the structured tool together (use tool-capable model)
    llm_with_tools = llm_tools.bind_tools(TOOLS_WITH_STRUCTURED)

    query = "What is 3 * 12? Also, what is 11 + 49? And compute 2^10."
    msg = llm_with_tools.invoke(query)

    print("Model content:\n", msg.content)
    print("\nTool calls:")
    for i, tc in enumerate(getattr(msg, "tool_calls", []) or []):
        print(i, tc["name"], tc["args"])


# In[ ]:


if False:
    # Bind the function tools and the structured tool together (use tool-capable model)
    llm_with_tools = llm_tools.bind_tools(TOOLS_WITH_STRUCTURED)

    query = "What is 3 * 12? Also, what is 11 + 49? And compute 2^10."
    msg = llm_with_tools.invoke(query)

    print("Model content:\n", msg.content)
    print("\nTool calls:")
    for i, tc in enumerate(getattr(msg, "tool_calls", []) or []):
        print(i, tc["name"], tc["args"])


# In[ ]:


if False:
    # Bind the function tools and the structured tool together (use tool-capable model)
    llm_with_tools = llm_tools.bind_tools(TOOLS_WITH_STRUCTURED)

    query = "What is 3 * 12? Also, what is 11 + 49? And compute 2^10."
    msg = llm_with_tools.invoke(query)

    print("Model content:\n", msg.content)
    print("\nTool calls:")
    for i, tc in enumerate(getattr(msg, "tool_calls", []) or []):
        print(i, tc["name"], tc["args"])


# In[ ]:


if False:
    # Bind the function tools and the structured tool together (use tool-capable model)
    llm_with_tools = llm_tools.bind_tools(TOOLS_WITH_STRUCTURED)

    query = "What is 3 * 12? Also, what is 11 + 49? And compute 2^10."
    msg = llm_with_tools.invoke(query)

    print("Model content:\n", msg.content)
    print("\nTool calls:")
    for i, tc in enumerate(getattr(msg, "tool_calls", []) or []):
        print(i, tc["name"], tc["args"])


# #### Chain
# 
# Small steps:
# 1) Observe events for a prompt → chat chain
# 2) Notice both chain-level and chat-model-level events
# 
# Explanation:
# - Chain events wrap the model events; useful to see where latency accumulates.
# 

# In[25]:


async def events_for_chain():
    async for e in chain.astream_events({"text": "Good evening."}, version="v1"):
        show_event(e)
# (Run inside a single orchestrated event loop at the end of the file)


# #### Filtering Events
# 
# Small steps:
# 1) Filter to only `on_chat_model_stream` to see token payloads
# 2) Show the token text
# 
# Explanation:
# - This pattern reduces noise while keeping the live token stream visible.
# 

# In[26]:


async def only_token_stream():
    async for e in chat.astream_events(
        [HumanMessage(content="Name 3 popular Vietnamese desserts.")],
        version="v1",
    ):
        name = e.get("event", e.get("name"))
        if name == "on_chat_model_stream":
            data = e.get("data", {})
            chunk = data.get("chunk")
            token_text = getattr(chunk, "content", chunk)
            if token_text:
                print(token_text, end="", flush=True)
    print()
# (Run inside a single orchestrated event loop at the end of the file)


# #### Non-streaming components
# 
# Small steps:
# 1) Add a non-streaming pre-processor before the chain
# 2) Observe events: no token stream until the pre-processor finishes
# 
# Explanation:
# - You’ll see a gap between `on_chain_start` and `on_chat_model_start` proportional to your pre-processing time.
# 

# In[27]:


slow_pre = RunnableLambda(lambda x: {"text": slow_upper(x["text"])})
events_chain = slow_pre | prompt | chat

async def events_with_non_streaming():
    async for e in events_chain.astream_events({"text": "Hello from Saigon."}, version="v1"):
        show_event(e)
# (Run inside a single orchestrated event loop at the end of the file)


# #### Propagating Callbacks
# 
# Small steps:
# 1) Write a small custom runnable that forwards callbacks
# 2) Compose it in a chain and observe events still flow
# 
# Explanation:
# - Custom runnables should accept the `config` and pass `callbacks`/`tags` along to downstream components to preserve tracing and streaming.
# 

# In[28]:


from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig

class ForwardCallbacks(Runnable):
    def invoke(self, input, config: RunnableConfig | None = None):
        # Do a tiny transform, but keep config to forward callbacks later
        text = input["text"].strip()
        return {"text": text}

forward = ForwardCallbacks()
cb_chain = forward | prompt | chat

async def events_with_forwarder():
    async for e in cb_chain.astream_events({"text": "  Please greet in Vietnamese.  "}, version="v1"):
        show_event(e)
# (Run inside a single orchestrated event loop at the end of the file)

# Orchestrate all async demos once to avoid "Event loop is closed" issues
import asyncio as _asyncio_for_top_level

async def _run_all_async_demos():
    await demo_streaming_input()
    await events_for_chat()
    await events_for_chain()
    await only_token_stream()
    await events_with_non_streaming()
    await events_with_forwarder()

_asyncio_for_top_level.run(_run_all_async_demos())


# #### Working with Input Streams
# 
# Small steps:
# 1) Create a `RunnableLambda` that accepts streamed input
# 2) Use `astream` to push input as an async generator
# 3) Show the model consuming partial input
# 
# Explanation:
# - `astream` supports async iteration both for inputs and outputs.
# - This pattern is useful when your upstream UI produces partial input (e.g., speech-to-text).
# 
