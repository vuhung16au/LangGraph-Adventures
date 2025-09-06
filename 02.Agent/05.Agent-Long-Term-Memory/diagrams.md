# Agent with Long-Term Memory - System Diagrams

This document contains visual diagrams to help understand the `task_mAIstro` agent system architecture and flow.

## 1. System Architecture Overview

```mermaid
graph TB
    subgraph "User Interface"
        UI[User Input]
        RESP[Agent Response]
    end
    
    subgraph "Agent Core"
        AGENT[task_mAIstro Agent]
        ROUTER[route_message Router]
    end
    
    subgraph "Memory Management"
        subgraph "Short-term Memory"
            MEMSAVER[MemorySaver<br/>Within-thread Context]
        end
        
        subgraph "Long-term Memory"
            INMEMSTORE[InMemoryStore<br/>Across-thread Persistence]
            PROFILE[Profile Memory<br/>User Information]
            TODO[ToDo Memory<br/>Task Collection]
            INSTRUCT[Instructions Memory<br/>Procedural Knowledge]
        end
    end
    
    subgraph "Schema Management"
        TRUSTCALL[Trustcall Extractor]
        SPY[Spy Pattern<br/>Monitoring & Debugging]
        SCHEMAS[Pydantic Schemas<br/>Profile, ToDo, Memory]
    end
    
    subgraph "Update Nodes"
        UPD_PROF[update_profile]
        UPD_TODO[update_todos]
        UPD_INST[update_instructions]
    end
    
    UI --> AGENT
    AGENT --> ROUTER
    ROUTER --> UPD_PROF
    ROUTER --> UPD_TODO
    ROUTER --> UPD_INST
    ROUTER --> RESP
    
    UPD_PROF --> TRUSTCALL
    UPD_TODO --> TRUSTCALL
    UPD_INST --> TRUSTCALL
    
    TRUSTCALL --> SPY
    TRUSTCALL --> SCHEMAS
    TRUSTCALL --> INMEMSTORE
    
    AGENT --> MEMSAVER
    AGENT --> INMEMSTORE
    
    INMEMSTORE --> PROFILE
    INMEMSTORE --> TODO
    INMEMSTORE --> INSTRUCT
    
    UPD_PROF --> AGENT
    UPD_TODO --> AGENT
    UPD_INST --> AGENT
```

## 2. LangGraph Flow Diagram

```mermaid
graph TD
    START([START]) --> TASK[task_mAIstro Node]
    
    TASK --> DECISION{Has Tool Calls?}
    
    DECISION -->|No| END([END])
    DECISION -->|Yes| ROUTE[route_message Router]
    
    ROUTE --> TYPE{Update Type?}
    
    TYPE -->|user| UPD_PROF[update_profile Node]
    TYPE -->|todo| UPD_TODO[update_todos Node]
    TYPE -->|instructions| UPD_INST[update_instructions Node]
    
    UPD_PROF --> TASK
    UPD_TODO --> TASK
    UPD_INST --> TASK
    
    subgraph "Memory Retrieval"
        TASK --> LOAD_PROF[Load Profile Memory]
        TASK --> LOAD_TODO[Load ToDo Memory]
        TASK --> LOAD_INST[Load Instructions Memory]
    end
    
    subgraph "Decision Making"
        TASK --> ANALYZE[Analyze User Input]
        ANALYZE --> TOOL_CALL[Make UpdateMemory Tool Call]
    end
    
    subgraph "Memory Updates"
        UPD_PROF --> TRUST_PROF[Trustcall Profile Update]
        UPD_TODO --> TRUST_TODO[Trustcall ToDo Update]
        UPD_INST --> TRUST_INST[Direct Instructions Update]
    end
```

## 3. Memory Architecture Diagram

```mermaid
graph TB
    subgraph "Memory Layers"
        subgraph "Short-term Memory (Within-thread)"
            THREAD1[Thread 1<br/>MemorySaver]
            THREAD2[Thread 2<br/>MemorySaver]
            THREADN[Thread N<br/>MemorySaver]
        end
        
        subgraph "Long-term Memory (Across-thread)"
            STORE[InMemoryStore]
        end
    end
    
    subgraph "Memory Organization"
        subgraph "User: Lance"
            LANCE_PROF["profile, Lance<br/>User Profile Data"]
            LANCE_TODO["todo, Lance<br/>ToDo Collection"]
            LANCE_INST["instructions, Lance<br/>Procedural Instructions"]
        end
        
        subgraph "User: Alice"
            ALICE_PROF["profile, Alice<br/>User Profile Data"]
            ALICE_TODO["todo, Alice<br/>ToDo Collection"]
            ALICE_INST["instructions, Alice<br/>Procedural Instructions"]
        end
    end
    
    subgraph "Memory Types"
        PROFILE_SCHEMA[Profile Schema<br/>name, location, job<br/>connections, interests]
        TODO_SCHEMA[ToDo Schema<br/>task, time_to_complete<br/>deadline, solutions, status]
        INSTRUCT_SCHEMA[Instructions Schema<br/>custom preferences<br/>for ToDo creation]
    end
    
    THREAD1 --> STORE
    THREAD2 --> STORE
    THREADN --> STORE
    
    STORE --> LANCE_PROF
    STORE --> LANCE_TODO
    STORE --> LANCE_INST
    STORE --> ALICE_PROF
    STORE --> ALICE_TODO
    STORE --> ALICE_INST
    
    LANCE_PROF --> PROFILE_SCHEMA
    LANCE_TODO --> TODO_SCHEMA
    LANCE_INST --> INSTRUCT_SCHEMA
    ALICE_PROF --> PROFILE_SCHEMA
    ALICE_TODO --> TODO_SCHEMA
    ALICE_INST --> INSTRUCT_SCHEMA
```

## 4. Tool Calling Decision Tree

```mermaid
flowchart TD
    INPUT[User Input] --> ANALYZE{Analyze Content}
    
    ANALYZE --> PERSONAL{Personal<br/>Information?}
    ANALYZE --> TASK{Task<br/>Mentioned?}
    ANALYZE --> PREF{Preferences<br/>Specified?}
    
    PERSONAL -->|Yes| USER_TOOL[UpdateMemory<br/>update_type: 'user']
    TASK -->|Yes| TODO_TOOL[UpdateMemory<br/>update_type: 'todo']
    PREF -->|Yes| INST_TOOL[UpdateMemory<br/>update_type: 'instructions']
    
    PERSONAL -->|No| NO_ACTION1[No Action]
    TASK -->|No| NO_ACTION2[No Action]
    PREF -->|No| NO_ACTION3[No Action]
    
    USER_TOOL --> ROUTE_USER[Route to update_profile]
    TODO_TOOL --> ROUTE_TODO[Route to update_todos]
    INST_TOOL --> ROUTE_INST[Route to update_instructions]
    
    NO_ACTION1 --> END([END])
    NO_ACTION2 --> END
    NO_ACTION3 --> END
    
    ROUTE_USER --> PROFILE_UPDATE[Update User Profile<br/>via Trustcall]
    ROUTE_TODO --> TODO_UPDATE[Update ToDo List<br/>via Trustcall + Spy]
    ROUTE_INST --> INST_UPDATE[Update Instructions<br/>via Direct Model Call]
    
    PROFILE_UPDATE --> RESPONSE[Generate Response]
    TODO_UPDATE --> RESPONSE
    INST_UPDATE --> RESPONSE
    
    RESPONSE --> END
    
    subgraph "Decision Logic"
        ANALYZE
        PERSONAL
        TASK
        PREF
    end
    
    subgraph "Tool Calls"
        USER_TOOL
        TODO_TOOL
        INST_TOOL
    end
    
    subgraph "Routing"
        ROUTE_USER
        ROUTE_TODO
        ROUTE_INST
    end
```

## 5. Trustcall Integration Diagram

```mermaid
graph TB
    subgraph "Trustcall System"
        subgraph "Schema Definitions"
            PROFILE_SCHEMA["Profile Schema<br/>name: Optional[str]<br/>location: Optional[str]<br/>job: Optional[str]<br/>connections: list[str]<br/>interests: list[str]"]
            
            TODO_SCHEMA["ToDo Schema<br/>task: str<br/>time_to_complete: Optional[int]<br/>deadline: Optional[datetime]<br/>solutions: list[str]<br/>status: Literal[...]"]
            
            MEMORY_SCHEMA["Memory Schema<br/>content: str"]
        end
        
        subgraph "Trustcall Extractors"
            PROF_EXTRACTOR["Profile Extractor<br/>create_extractor(model, Profile)"]
            TODO_EXTRACTOR["ToDo Extractor<br/>create_extractor(model, ToDo)<br/>enable_inserts=True"]
            MEM_EXTRACTOR["Memory Extractor<br/>create_extractor(model, Memory)<br/>enable_inserts=True"]
        end
        
        subgraph "Trustcall Features"
            VALIDATION[Schema Validation<br/>Pydantic Models]
            SELF_CORRECT[Self-Correction<br/>Automatic Error Fixing]
            PATCHING[Document Patching<br/>Update Existing Records]
            PARALLEL[Parallel Tool Calling<br/>Multiple Operations]
        end
    end
    
    subgraph "Integration Points"
        subgraph "Agent Nodes"
            UPD_PROF[update_profile Node]
            UPD_TODO[update_todos Node]
        end
        
        subgraph "Memory Store"
            STORE[InMemoryStore]
        end
        
        subgraph "Spy Monitoring"
            SPY[Spy Pattern<br/>Tool Call Interception]
        end
    end
    
    UPD_PROF --> PROF_EXTRACTOR
    UPD_TODO --> TODO_EXTRACTOR
    
    PROF_EXTRACTOR --> PROFILE_SCHEMA
    TODO_EXTRACTOR --> TODO_SCHEMA
    
    PROF_EXTRACTOR --> VALIDATION
    TODO_EXTRACTOR --> VALIDATION
    
    VALIDATION --> SELF_CORRECT
    SELF_CORRECT --> PATCHING
    
    TODO_EXTRACTOR --> SPY
    SPY --> PARALLEL
    
    PROF_EXTRACTOR --> STORE
    TODO_EXTRACTOR --> STORE
    
    subgraph "Trustcall Operations"
        NEW_MEM[Create New Memory]
        UPDATE_MEM[Update Existing Memory]
        VALIDATE_MEM[Validate Schema]
        PATCH_MEM[Patch Document]
    end
    
    PATCHING --> NEW_MEM
    PATCHING --> UPDATE_MEM
    VALIDATION --> VALIDATE_MEM
    SELF_CORRECT --> PATCH_MEM
```

## Diagram Usage Notes

### System Architecture Overview
- Shows the complete system with all major components
- Illustrates data flow between agent, memory stores, and schema management
- Highlights the dual-layer memory architecture

### LangGraph Flow Diagram
- Demonstrates the agent's decision-making process
- Shows conditional routing based on tool calls
- Illustrates the circular flow back to the main agent node

### Memory Architecture Diagram
- Visualizes the separation between short-term and long-term memory
- Shows namespace organization by user and memory type
- Demonstrates schema relationships

### Tool Calling Decision Tree
- Shows the agent's logic for deciding when to update memory
- Illustrates the three types of memory updates
- Demonstrates the routing mechanism

### Trustcall Integration Diagram
- Details how Trustcall manages schema-based memory operations
- Shows self-correction and validation capabilities
- Illustrates integration with the spy pattern for monitoring

These diagrams provide a comprehensive visual understanding of the `task_mAIstro` agent system, from high-level architecture to detailed implementation patterns.
