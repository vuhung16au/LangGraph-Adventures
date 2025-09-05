# Project Flow

This document describes the detailed flow of the Research Collective system, including step-by-step processes and decision points.

## Overall System Flow

```mermaid
flowchart TD
    START([User Starts Research]) --> INPUT[Input Research Topic]
    INPUT --> ANALYST[Generate Analyst Team]
    ANALYST --> HUMAN{Human Review}
    HUMAN -->|Approve| PARALLEL[Parallel Interviews]
    HUMAN -->|Modify| ANALYST
    PARALLEL --> SYNTHESIS[Synthesize Results]
    SYNTHESIS --> REPORT[Generate Final Report]
    REPORT --> END([Research Complete])
    
    style START fill:#e1f5fe
    style END fill:#e8f5e8
    style HUMAN fill:#fff3e0
```

## Detailed Process Flow

### Phase 1: Initialization and Setup

```mermaid
sequenceDiagram
    participant U as User
    participant NB as Jupyter Notebook
    participant ENV as Environment
    participant LLM as Gemini LLM
    participant LS as LangSmith
    
    U->>NB: Start Notebook
    NB->>ENV: Load .env.local
    ENV->>NB: API Keys
    NB->>LLM: Initialize Gemini
    NB->>LS: Setup Tracing
    NB->>U: System Ready
```

### Phase 2: Analyst Generation Flow

```mermaid
flowchart TD
    START([User Input]) --> TOPIC[Research Topic]
    TOPIC --> AG[Analyst Generator]
    AG --> LLM1[LLM: Generate Analysts]
    LLM1 --> ANALYSTS[Analyst List]
    ANALYSTS --> DISPLAY[Display Analysts]
    DISPLAY --> HUMAN{Human Review}
    HUMAN -->|Satisfied| APPROVE[Approve Analysts]
    HUMAN -->|Needs Changes| FEEDBACK[Provide Feedback]
    FEEDBACK --> AG
    APPROVE --> NEXT[Proceed to Interviews]
    
    style START fill:#e1f5fe
    style HUMAN fill:#fff3e0
    style NEXT fill:#e8f5e8
```

### Phase 3: Parallel Interview Flow

```mermaid
graph TB
    subgraph "Map Phase - Parallel Execution"
        A1[Analyst 1] --> I1[Interview 1]
        A2[Analyst 2] --> I2[Interview 2]
        A3[Analyst 3] --> I3[Interview 3]
    end
    
    subgraph "Interview Sub-Process"
        I1 --> Q1[Ask Question]
        Q1 --> S1[Search Sources]
        S1 --> AQ1[Answer Question]
        AQ1 --> R1{Route Decision}
        R1 -->|Continue| Q1
        R1 -->|Complete| SAVE1[Save Interview]
    end
    
    subgraph "Reduce Phase"
        SAVE1 --> SYNTH[Synthesize Results]
        SAVE2[Save Interview 2] --> SYNTH
        SAVE3[Save Interview 3] --> SYNTH
        SYNTH --> REPORT[Generate Report]
    end
```

## Individual Interview Flow

### Interview Sub-Graph Process

```mermaid
flowchart TD
    START([Interview Start]) --> INIT[Initialize Interview State]
    INIT --> QUESTION[Generate Question]
    QUESTION --> SEARCH[Search Information]
    
    subgraph "Parallel Search"
        SEARCH --> WEB[Web Search via Tavily]
        SEARCH --> WIKI[Wikipedia Search]
    end
    
    WEB --> CONTEXT[Format Context]
    WIKI --> CONTEXT
    CONTEXT --> ANSWER[Generate Answer]
    ANSWER --> ROUTE{Route Decision}
    
    ROUTE -->|Continue Interview| QUESTION
    ROUTE -->|Interview Complete| SAVE[Save Interview]
    SAVE --> SECTION[Write Section]
    SECTION --> END([Interview End])
    
    style START fill:#e1f5fe
    style END fill:#e8f5e8
    style ROUTE fill:#fff3e0
```

### Question-Answer Cycle

```mermaid
sequenceDiagram
    participant A as Analyst
    participant E as Expert AI
    participant S as Search Sources
    participant L as LLM
    
    A->>L: Generate Question
    L->>A: Question
    A->>E: Ask Question
    E->>S: Search Web
    E->>S: Search Wikipedia
    S->>E: Search Results
    E->>L: Generate Answer
    L->>E: Answer with Citations
    E->>A: Provide Answer
    A->>A: Evaluate Response
    A->>E: Next Question (if needed)
```

## Data Flow Through the System

### Information Gathering Flow

```mermaid
graph LR
    subgraph "Input"
        Q[Analyst Question]
    end
    
    subgraph "Search Layer"
        Q --> QG[Query Generator]
        QG --> TS[Tavily Search]
        QG --> WP[Wikipedia]
    end
    
    subgraph "Processing"
        TS --> WS[Web Sources]
        WP --> WS
        WS --> FC[Format Context]
    end
    
    subgraph "Generation"
        FC --> EA[Expert AI]
        EA --> GM[Gemini Model]
        GM --> A[Answer with Citations]
    end
    
    subgraph "Output"
        A --> I[Interview Transcript]
    end
```

## Report Generation Flow

### Synthesis and Report Creation

```mermaid
flowchart TD
    START([All Interviews Complete]) --> SECTIONS[Individual Sections]
    SECTIONS --> PARALLEL[Parallel Processing]
    
    subgraph "Parallel Report Generation"
        PARALLEL --> INTRO[Write Introduction]
        PARALLEL --> CONTENT[Write Main Content]
        PARALLEL --> CONCLUSION[Write Conclusion]
    end
    
    INTRO --> COMBINE[Combine Sections]
    CONTENT --> COMBINE
    CONCLUSION --> COMBINE
    COMBINE --> FINAL[Final Report]
    FINAL --> DISPLAY[Display Report]
    DISPLAY --> END([Process Complete])
    
    style START fill:#e1f5fe
    style END fill:#e8f5e8
```

## State Management Flow

### State Transitions

```mermaid
stateDiagram-v2
    [*] --> Initialization
    Initialization --> AnalystGeneration
    AnalystGeneration --> HumanReview
    HumanReview --> AnalystGeneration : Feedback Provided
    HumanReview --> InterviewPhase : Approved
    InterviewPhase --> ReportGeneration
    ReportGeneration --> [*]
    
    state InterviewPhase {
        [*] --> QuestionGeneration
        QuestionGeneration --> InformationSearch
        InformationSearch --> AnswerGeneration
        AnswerGeneration --> RoutingDecision
        RoutingDecision --> QuestionGeneration : Continue
        RoutingDecision --> InterviewComplete : Done
        InterviewComplete --> [*]
    }
    
    state ReportGeneration {
        [*] --> SectionSynthesis
        SectionSynthesis --> IntroductionWriting
        SectionSynthesis --> ConclusionWriting
        IntroductionWriting --> ReportCombination
        ConclusionWriting --> ReportCombination
        ReportCombination --> [*]
    }
```


## Human-in-the-Loop Flow

### Human Interaction Points

```mermaid
flowchart TD
    START([Process Start]) --> AUTO[Automatic Processing]
    AUTO --> CHECK{Checkpoint?}
    CHECK -->|No| AUTO
    CHECK -->|Yes| PAUSE[Pause for Human]
    
    PAUSE --> DISPLAY[Display Current State]
    DISPLAY --> HUMAN[Human Review]
    HUMAN --> DECISION{Human Decision}
    
    DECISION -->|Approve| CONTINUE[Continue Process]
    DECISION -->|Modify| MODIFY[Apply Modifications]
    DECISION -->|Cancel| CANCEL[Cancel Process]
    
    MODIFY --> AUTO
    CONTINUE --> AUTO
    CANCEL --> END([Process End])
    
    style PAUSE fill:#fff3e0
    style HUMAN fill:#e3f2fd
    style DECISION fill:#fff3e0
```
