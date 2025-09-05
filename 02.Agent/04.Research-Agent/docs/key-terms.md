# Key Terms

This document defines the key terms, concepts, and terminology used throughout the Research Collective project.

## Core Concepts

### Research Collective
A multi-agent AI system that automates research processes by creating specialized AI analysts who conduct parallel interviews with expert AIs to gather insights on any given topic.

### Multi-Agent System
A system composed of multiple autonomous agents (AI analysts) that work together to achieve a common goal. In this project, each agent has a specific role and perspective on the research topic.

### Human-in-the-Loop (HITL)
A design pattern where human feedback is integrated into the AI workflow. In this project, humans can review and refine the AI analyst team before research begins.

## LangGraph Concepts

### StateGraph
A graph-based execution model where nodes represent functions and edges represent the flow of execution. The state is passed between nodes and can be modified at each step.

### State
The data structure that flows through the graph, containing all relevant information for the current execution context. In this project, states include topics, analysts, interviews, and reports.

### Node
A function that performs a specific task within the graph. Each node can read from and write to the state.

### Edge
A connection between nodes that defines the execution flow. Can be conditional (routing based on state) or unconditional (always follows the same path).

### Checkpointer
A mechanism for persisting and restoring graph state, enabling resumable execution and memory across sessions.

### Memory
The ability to maintain state and context across multiple interactions, allowing for conversation continuity and state persistence.

### Send API
A LangGraph feature that enables parallel execution of multiple sub-graphs, implementing a map-reduce pattern for scalable processing.

## Agent & Analyst Concepts

### Analyst
An AI persona with a specific role, affiliation, and perspective on the research topic. Each analyst focuses on a particular aspect of the research.

### Expert AI
The AI system that answers questions during interviews, drawing from multiple data sources to provide comprehensive responses.

### Interview
A multi-turn conversation between an analyst and an expert AI, designed to extract detailed insights on a specific aspect of the research topic.

### Persona
The character and perspective of an AI agent, including their role, affiliation, background, and focus area.

## Research Process Terms

### Source Selection
The process of choosing input sources for research, which can include web search, Wikipedia, documents, or other knowledge bases.

### Planning
The initial phase where the system generates a team of AI analysts, each focusing on different sub-topics of the main research question.

### Map-Reduce
A parallel processing pattern where multiple operations (interviews) are executed simultaneously (map) and then combined into a single result (reduce).

### Parallel Processing
The simultaneous execution of multiple interviews, allowing the system to gather information from multiple perspectives at the same time.

### Synthesis
The process of combining insights from multiple interviews into a coherent, comprehensive report.

## Data & Information Terms

### Context
The information and data that the expert AI uses to answer analyst questions, typically gathered from web search and Wikipedia.

### Structured Output
Data formatted according to predefined schemas (using Pydantic models) to ensure consistency and type safety.

### Citations
References to sources used in the research, formatted consistently and included in the final report.

### Memo
A structured summary of an interview, containing the key insights and findings from a specific analyst's research.

## Technical Terms

### LLM (Large Language Model)
The underlying AI model (Gemini 2.0 Flash) that powers all text generation and reasoning tasks in the system.

### Temperature
A parameter controlling the randomness of LLM outputs. Set to 0 in this project for consistent, deterministic responses.

### Retry Logic
Error handling mechanisms that automatically retry failed operations, particularly useful for API calls that may experience temporary failures.

### Quota Management
Systems for tracking and managing API usage limits to prevent exceeding service quotas.

### Tracing
The process of monitoring and logging system execution for debugging, optimization, and observability purposes.

## Workflow Terms

### Stream Mode
A LangGraph execution mode that yields intermediate results as the graph executes, allowing for real-time monitoring of progress.

### Thread
A unique identifier for a conversation or execution session, enabling multiple parallel research processes.

### Interruption
A mechanism for pausing graph execution to allow human input or review before continuing.

### Conditional Routing
Logic that determines the next node to execute based on the current state, enabling dynamic workflow adaptation.

## Output Terms

### Report
The final synthesized document containing insights from all analyst interviews, formatted with proper structure and citations.

### Section
A portion of the final report focused on a specific aspect of the research, typically corresponding to one analyst's findings.

### Introduction
The opening section of the report that provides context and previews the main findings.

### Conclusion
The closing section of the report that summarizes key insights and findings.

## API & Integration Terms

### API Key
Authentication credentials required to access external services like Gemini, Tavily, and LangSmith.

### Environment Variables
Configuration settings stored in the system environment, used to manage API keys and other sensitive information.

### Web Search
The process of querying external search engines (via Tavily) to gather real-time information on research topics.

### Document Loading
The process of retrieving and processing documents from various sources (Wikipedia, web pages) for use in research.

## State Management Terms

### TypedDict
A Python typing construct used to define the structure of graph states with type hints.

### Annotated
A Python typing feature used to add metadata to type hints, particularly useful for state field definitions.

### Operator.add
A Python operator used in state definitions to specify how multiple values should be combined when added to the state.

### MessagesState
A specialized state type for managing conversation messages in LangGraph.

## Error Handling Terms

### ResourceExhausted
A specific type of API error indicating that service quotas or rate limits have been exceeded.

### Exponential Backoff
A retry strategy where the delay between retry attempts increases exponentially, helping to handle temporary service unavailability.

### Graceful Degradation
The ability of the system to continue functioning with reduced capabilities when some services are unavailable.
