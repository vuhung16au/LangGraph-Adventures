# Architecture

This document describes the high-level architecture of the Research Collective system, including its components, interactions, and design patterns.

## System Overview

The Research Collective is built as a multi-agent system using LangGraph, where specialized AI analysts work in parallel to research topics through structured interviews with expert AIs.

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI[Jupyter Notebook]
    end
    
    subgraph "Core System"
        LG[LangGraph Engine]
        SM[State Manager]
        CP[Checkpointer]
    end
    
    subgraph "Agent Layer"
        AG[Analyst Generator]
        subgraph "Analyst Agents"
            A1[Analyst 1]
            A2[Analyst 2]
            A3[Analyst N]
        end
        EA[Expert AI]
    end
    
    subgraph "Data Sources"
        TS[Tavily Search]
        WP[Wikipedia]
        WS[Web Sources]
    end
    
    subgraph "External Services"
        GM[Gemini API]
        LS[LangSmith]
    end
    
    subgraph "Output Layer"
        RG[Report Generator]
        FR[Final Report]
    end
    
    UI --> LG
    LG --> SM
    LG --> CP
    LG --> AG
    AG --> A1
    AG --> A2
    AG --> A3
    A1 --> EA
    A2 --> EA
    A3 --> EA
    EA --> TS
    EA --> WP
    TS --> WS
    EA --> GM
    LG --> LS
    A1 --> RG
    A2 --> RG
    A3 --> RG
    RG --> FR
```

## Component Architecture

### 1. LangGraph Engine
The core orchestration engine that manages the entire workflow.

**Responsibilities:**
- Graph execution and state management
- Node coordination and routing
- Parallel processing with Send API
- Human-in-the-loop interactions

**Key Components:**
- StateGraph: Main graph structure
- MemorySaver: State persistence
- Checkpointer: Session management

### 2. Agent Layer

#### Analyst Generator
Creates specialized AI analyst personas based on the research topic.

```mermaid
graph LR
    TG[Topic Input] --> AG[Analyst Generator]
    HF[Human Feedback] --> AG
    AG --> AL[Analyst List]
    AL --> HITL[Human Review]
    HITL --> AG
    HITL --> AF[Analyst Final]
```

#### Individual Analysts
Each analyst is a specialized AI persona with:
- **Role**: Specific function (e.g., Technical Expert, Business Analyst)
- **Affiliation**: Organization or perspective
- **Focus**: Particular aspect of the research topic
- **Persona**: Character and communication style

#### Expert AI
The knowledge-gathering system that:
- Receives questions from analysts
- Searches multiple data sources
- Synthesizes information
- Provides comprehensive answers

### 3. Data Integration Layer

```mermaid
graph TB
    subgraph "Data Sources"
        TS[Tavily Search API]
        WP[Wikipedia API]
    end
    
    subgraph "Processing"
        QG[Query Generator]
        DL[Document Loader]
        FC[Format Context]
    end
    
    subgraph "Expert AI"
        EA[Expert AI Engine]
        GM[Gemini Model]
    end
    
    EA --> QG
    QG --> TS
    QG --> WP
    TS --> DL
    WP --> DL
    DL --> FC
    FC --> EA
    EA --> GM
```

### 4. State Management Architecture

The system uses a hierarchical state structure:

```mermaid
graph TD
    RS[Research State] --> AS[Analyst State]
    RS --> IS[Interview State]
    RS --> RS2[Report State]
    
    AS --> AL[Analyst List]
    AS --> HF[Human Feedback]
    
    IS --> MS[Messages]
    IS --> CT[Context]
    IS --> IT[Interview Transcript]
    
    RS2 --> SC[Sections]
    RS2 --> IN[Introduction]
    RS2 --> CN[Conclusion]
    RS2 --> FR[Final Report]
```

## Data Flow Architecture

### 1. Input Processing
```mermaid
sequenceDiagram
    participant U as User
    participant LG as LangGraph
    participant AG as Analyst Generator
    participant H as Human
    
    U->>LG: Research Topic
    LG->>AG: Generate Analysts
    AG->>LG: Analyst List
    LG->>H: Human Review
    H->>LG: Feedback/Approval
    LG->>AG: Refined Analysts
```

### 2. Parallel Interview Processing
```mermaid
graph TB
    subgraph "Map Phase"
        A1[Analyst 1] --> I1[Interview 1]
        A2[Analyst 2] --> I2[Interview 2]
        A3[Analyst 3] --> I3[Interview 3]
    end
    
    subgraph "Data Gathering"
        I1 --> DS1[Data Sources]
        I2 --> DS2[Data Sources]
        I3 --> DS3[Data Sources]
    end
    
    subgraph "Reduce Phase"
        I1 --> RG[Report Generator]
        I2 --> RG
        I3 --> RG
        RG --> FR[Final Report]
    end
```

### 3. Interview Sub-Graph Architecture
Each interview runs as an independent sub-graph:

```mermaid
graph LR
    AQ[Ask Question] --> SW[Search Web]
    AQ --> SWP[Search Wikipedia]
    SW --> AQ2[Answer Question]
    SWP --> AQ2
    AQ2 --> RT{Route Decision}
    RT -->|Continue| AQ
    RT -->|Complete| SI[Save Interview]
    SI --> WS[Write Section]
```

## Integration Architecture

### API Integration Layer
```mermaid
graph TB
    subgraph "External APIs"
        GM[Gemini API]
        TS[Tavily API]
        WP[Wikipedia API]
        LS[LangSmith API]
    end
    
    subgraph "Integration Layer"
        GCI[Gemini Client]
        TCI[Tavily Client]
        WCI[Wikipedia Client]
        LCI[LangSmith Client]
    end
    
    subgraph "Application Layer"
        LG[LangGraph Engine]
        EA[Expert AI]
        AG[Analyst Generator]
    end
    
    LG --> GCI
    EA --> GCI
    EA --> TCI
    EA --> WCI
    LG --> LCI
    
    GCI --> GM
    TCI --> TS
    WCI --> WP
    LCI --> LS
```

## Security & Configuration Architecture

### Environment Management
```mermaid
graph TB
    subgraph "Configuration Sources"
        ENV[.env.local File]
        OS[OS Environment]
        DEF[Default Values]
    end
    
    subgraph "Configuration Manager"
        CM[Config Manager]
        VL[Validation Layer]
    end
    
    subgraph "Application"
        APP[Research Collective]
    end
    
    ENV --> CM
    OS --> CM
    DEF --> CM
    CM --> VL
    VL --> APP
```

## Scalability Architecture

### Horizontal Scaling
The system is designed for horizontal scaling through:

1. **Parallel Processing**: Multiple interviews run simultaneously
2. **Stateless Components**: Most components can be scaled independently
3. **External APIs**: Leverages scalable cloud services
4. **Modular Design**: Components can be deployed separately

### Performance Optimization
```mermaid
graph TB
    subgraph "Performance Layers"
        CACHE[Caching Layer]
        POOL[Connection Pooling]
        ASYNC[Async Processing]
        BATCH[Batch Operations]
    end
    
    subgraph "Monitoring"
        METRICS[Performance Metrics]
        TRACING[Request Tracing]
        LOGS[Structured Logging]
    end
    
    CACHE --> METRICS
    POOL --> TRACING
    ASYNC --> LOGS
    BATCH --> METRICS
```

## Error Handling Architecture

### Resilience Patterns
```mermaid
graph TB
    subgraph "Error Handling"
        RETRY[Retry Logic]
        CIRCUIT[Circuit Breaker]
        FALLBACK[Fallback Mechanisms]
        GRACEFUL[Graceful Degradation]
    end
    
    subgraph "Monitoring"
        ALERTS[Error Alerts]
        METRICS[Error Metrics]
        LOGS[Error Logs]
    end
    
    RETRY --> ALERTS
    CIRCUIT --> METRICS
    FALLBACK --> LOGS
    GRACEFUL --> ALERTS
```

## Deployment Architecture

### Development Environment
```mermaid
graph TB
    subgraph "Development"
        JN[Jupyter Notebook]
        VE[Virtual Environment]
        LOCAL[Local APIs]
    end
    
    subgraph "External Services"
        GM[Gemini API]
        TS[Tavily API]
        LS[LangSmith]
    end
    
    JN --> VE
    VE --> LOCAL
    LOCAL --> GM
    LOCAL --> TS
    LOCAL --> LS
```

### Production Considerations
For production deployment, the architecture would include:
- Container orchestration (Docker/Kubernetes)
- API gateway for external service management
- Database for state persistence
- Load balancing for high availability
- Monitoring and alerting systems

## Key Design Principles

1. **Modularity**: Each component has a single responsibility
2. **Scalability**: Parallel processing and stateless design
3. **Resilience**: Error handling and graceful degradation
4. **Observability**: Comprehensive logging and tracing
5. **Flexibility**: Human-in-the-loop for customization
6. **Extensibility**: Easy to add new data sources or agents
