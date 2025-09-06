# Agent with Long-Term Memory

## Visual Diagrams

For a quick understanding of the system architecture and flow, see the [System Diagrams](diagrams.md) which include:

- **System Architecture Overview** - Complete system components and data flow
- **LangGraph Flow Diagram** - Agent decision-making and routing logic  
- **Memory Architecture Diagram** - Dual-layer memory system visualization
- **Tool Calling Decision Tree** - Agent's memory update decision logic
- **Trustcall Integration Diagram** - Schema management and validation flow

## Summary

This notebook demonstrates the creation of `task_mAIstro`, an intelligent agent with long-term memory capabilities that helps users manage their ToDo lists. Unlike previous chatbots that always saved memories, this agent makes intelligent decisions about **when** to save memories and **what type** of memory to update. The agent manages three distinct types of long-term memory: user profiles, ToDo collections, and procedural instructions, while also maintaining both short-term (within-thread) and long-term (across-thread) memory persistence.

The implementation showcases advanced LangGraph concepts including ReAct agent architecture, conditional routing, tool calling for decision-making, and the integration of Trustcall for schema-based memory management with full visibility into memory operations.

## Key Points

- **Intelligent Memory Management**: The agent decides when to save memories rather than always saving them
- **Multi-Type Memory Storage**: Manages user profiles, ToDo items, and procedural instructions separately
- **Dual Memory Architecture**: Combines short-term (within-thread) and long-term (across-thread) memory
- **Schema-Based Updates**: Uses Trustcall for structured memory creation and updates
- **Visibility and Debugging**: Implements spy pattern for monitoring Trustcall operations
- **Conditional Routing**: Routes messages to appropriate memory update functions based on content
- **Persistent Across Sessions**: Long-term memory persists across different conversation threads

## Key Terms

- **task_mAIstro**: The main agent that helps manage ToDo lists with long-term memory
- **Trustcall**: A library for creating and updating JSON schemas with validation and self-correction
- **ReAct Agent**: Reasoning and Acting agent architecture that combines thought and action
- **Memory Store**: Persistent storage for long-term memory across conversation threads
- **Checkpointer**: Manages short-term memory within individual conversation threads
- **Spy Pattern**: A debugging technique to monitor and inspect tool calls made by Trustcall
- **Conditional Edges**: Graph routing that directs flow based on message content and tool calls
- **Schema Validation**: Pydantic models ensure structured data for memory storage
- **Tool Calling**: Agent's ability to invoke specific functions for memory updates
- **Namespace**: Organizational structure for different types of memories in the store

## Key Concepts

### Memory Architecture
- **Short-term Memory**: Maintains conversation context within a single thread using MemorySaver
- **Long-term Memory**: Persists user data across multiple conversation sessions using InMemoryStore
- **Memory Types**: Three distinct memory categories (profile, todo, instructions) with separate namespaces

### Agent Decision Making
- **Conditional Memory Updates**: Agent analyzes user input to determine if memory should be updated
- **Tool Selection**: Uses UpdateMemory tool to specify which type of memory to modify
- **Routing Logic**: Conditional edges direct flow to appropriate memory update functions

### Schema-Based Memory Management
- **Pydantic Models**: Define structured schemas for Profile, ToDo, and Memory objects
- **Trustcall Integration**: Handles schema creation, updates, and validation automatically
- **Self-Correction**: Trustcall can fix validation errors and update existing documents

### Visibility and Monitoring
- **Spy Pattern**: Intercepts and logs all tool calls made by Trustcall
- **Tool Call Inspection**: Provides detailed visibility into memory operations
- **Change Tracking**: Monitors both new memory creation and existing memory updates

## Key Components

### Core Schemas
```python
class Profile(BaseModel):
    name: Optional[str]
    location: Optional[str] 
    job: Optional[str]
    connections: list[str]
    interests: list[str]

class ToDo(BaseModel):
    task: str
    time_to_complete: Optional[int]
    deadline: Optional[datetime]
    solutions: list[str]
    status: Literal["not started", "in progress", "done", "archived"]

class UpdateMemory(TypedDict):
    update_type: Literal['user', 'todo', 'instructions']
```

### Graph Nodes
- **task_mAIstro**: Main agent node that processes user input and decides on memory updates
- **update_profile**: Updates user profile information using Trustcall
- **update_todos**: Manages ToDo list items with spy pattern monitoring
- **update_instructions**: Updates procedural memory for ToDo creation preferences

### Memory Infrastructure
- **InMemoryStore**: Long-term memory storage across conversation threads
- **MemorySaver**: Short-term memory checkpointer for within-thread context
- **Namespace Organization**: Separate namespaces for different memory types

### Spy Implementation
```python
class Spy:
    def __init__(self):
        self.called_tools = []
    
    def __call__(self, run):
        # Collects information about tool calls made by Trustcall
        # Provides visibility into memory operations
```

## Technical Highlights

### Tool Calling for Decision Making
The agent uses sophisticated tool calling to make intelligent decisions about memory management:

- **UpdateMemory Tool**: Allows the agent to specify which type of memory to update
- **Conditional Execution**: Only updates memory when relevant information is detected
- **Parallel Tool Calls**: Supports multiple simultaneous memory operations
- **Tool Call Validation**: Ensures proper tool usage with structured arguments

**Example Implementation:**
```python
response = model.bind_tools([UpdateMemory], parallel_tool_calls=False).invoke(
    [SystemMessage(content=system_msg)] + state["messages"]
)
```

### Memory Stores for Persistence
Dual-layer memory architecture provides both immediate context and long-term persistence:

- **Short-term Memory (MemorySaver)**: Maintains conversation context within threads
- **Long-term Memory (InMemoryStore)**: Persists user data across multiple sessions
- **Namespace Separation**: Organizes memories by type and user ID
- **Automatic Retrieval**: Loads relevant memories for each conversation

**Memory Retrieval Pattern:**
```python
namespace = ("profile", user_id)
memories = store.search(namespace)
user_profile = memories[0].value if memories else None
```

### Spy Pattern for Debugging and Visibility
Advanced monitoring system provides complete visibility into Trustcall operations:

- **Tool Call Interception**: Captures all tool calls made by Trustcall
- **Change Detection**: Identifies new memory creation vs. existing memory updates
- **Operation Logging**: Provides detailed logs of memory modifications
- **Debugging Support**: Enables troubleshooting of memory operations

**Spy Implementation:**
```python
def extract_tool_info(tool_calls, schema_name="Memory"):
    changes = []
    for call_group in tool_calls:
        for call in call_group:
            if call['name'] == 'PatchDoc':
                changes.append({
                    'type': 'update',
                    'doc_id': call['args']['json_doc_id'],
                    'planned_edits': call['args']['planned_edits']
                })
            elif call['name'] == schema_name:
                changes.append({
                    'type': 'new',
                    'value': call['args']
                })
    return changes
```

### Advanced Features
- **Schema Validation**: Pydantic models ensure data integrity
- **Self-Correction**: Trustcall automatically fixes validation errors
- **Context Awareness**: Agent considers existing memories when making decisions
- **User Preferences**: Learns and applies user-specific ToDo creation preferences
- **Cross-Session Persistence**: Memories survive conversation restarts

## Conclusion

This notebook successfully demonstrates the creation of a sophisticated agent with long-term memory capabilities. The `task_mAIstro` agent showcases several advanced concepts:

**Key Achievements:**
- **Intelligent Memory Management**: Agent makes smart decisions about when and what to remember
- **Multi-Type Memory Architecture**: Seamlessly manages different types of persistent information
- **Advanced Debugging**: Spy pattern provides complete visibility into memory operations
- **Schema-Based Validation**: Ensures data integrity through structured schemas
- **Cross-Session Persistence**: Maintains user context across multiple conversations

**Technical Excellence:**
- **ReAct Architecture**: Combines reasoning and action for intelligent decision-making
- **Conditional Routing**: Dynamic flow control based on message content
- **Tool Integration**: Seamless integration with Trustcall for schema management
- **Dual Memory Layers**: Optimal balance between immediate context and long-term storage

**Practical Applications:**
This implementation serves as a foundation for building sophisticated conversational agents that can:
- Remember user preferences and personal information
- Manage complex task lists with structured data
- Learn and adapt to user-specific requirements
- Provide persistent assistance across multiple sessions
- Maintain context while offering intelligent memory management

The combination of LangGraph's graph-based architecture, Trustcall's schema management, and the spy pattern for visibility creates a robust, maintainable, and debuggable agent system that represents the state-of-the-art in conversational AI with long-term memory capabilities.
