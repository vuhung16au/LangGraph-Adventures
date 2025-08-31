# RAG From Scratch

A comprehensive tutorial series that builds Retrieval Augmented Generation (RAG) systems from scratch using LangChain and modern AI technologies.

## 📖 Overview

This project is a hands-on learning journey through the complete RAG pipeline, from basic concepts to advanced implementations. It consists of 5 progressive notebooks that teach you how to build production-ready RAG applications using LangChain, Google Gemini, and other cutting-edge tools.

**🎥 Accompanying Video Series**: [RAG From Scratch Playlist](https://www.youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)

Note: We use Google Gemini in this project. 

## 🎯 Targeted Audiences

- **AI/ML Engineers** looking to implement RAG in production systems
- **Data Scientists** wanting to enhance LLM capabilities with external knowledge
- **Software Developers** building AI-powered applications
- **Students & Researchers** learning about modern AI architectures
- **Product Managers** understanding RAG capabilities and limitations
- **Anyone** interested in building intelligent, knowledge-aware AI systems

## 🚀 Key Takeaways

By completing this tutorial series, you will:

- **Master RAG Fundamentals**: Understand the complete RAG pipeline (Indexing → Retrieval → Generation)
- **Build Production Systems**: Create scalable, efficient RAG applications
- **Optimize Performance**: Learn advanced techniques for better retrieval and generation
- **Handle Real-World Data**: Work with various document types and data sources
- **Implement Best Practices**: Follow industry standards for RAG development
- **Debug & Monitor**: Use LangSmith for tracing and debugging RAG applications

## 🤔 What is RAG?

**Retrieval Augmented Generation (RAG)** is a powerful AI architecture that combines the reasoning capabilities of Large Language Models (LLMs) with external knowledge retrieval. Unlike traditional LLMs that rely solely on their training data, RAG systems can:

- **Access Current Information**: Retrieve up-to-date information from external sources
- **Handle Private Data**: Work with proprietary or confidential documents
- **Provide Citations**: Reference specific sources for generated answers
- **Reduce Hallucinations**: Ground responses in retrieved facts
- **Scale Knowledge**: Expand beyond the model's training cutoff

## 🎯 Why RAG?

### **The Problem with Traditional LLMs**
- **Fixed Knowledge**: Trained on static datasets with cutoff dates
- **No Access to Private Data**: Cannot access proprietary or confidential information
- **Hallucinations**: May generate plausible but incorrect information
- **Limited Context**: Cannot reference specific sources or documents
- **Expensive Fine-tuning**: Updating knowledge requires costly retraining

### **RAG as the Solution**
- **Dynamic Knowledge**: Access real-time, up-to-date information
- **Private Data Integration**: Work with internal documents and databases
- **Factual Grounding**: Base responses on retrieved evidence
- **Transparency**: Provide source citations and references
- **Cost-Effective**: Update knowledge without retraining models

## 🛠️ How We Implement RAG Using LangChain

This project demonstrates a complete RAG implementation through 5 progressive notebooks:

### **01-rag-basics.ipynb** - Foundation
- Document loading and preprocessing
- Text splitting and chunking strategies
- Vector embeddings with Google Generative AI
- ChromaDB vector store setup
- Basic retrieval and generation pipeline

### **02-query-enhancement.ipynb** - Query Optimization
- Multi-query retrieval techniques
- Query expansion and reformulation
- Contextual query processing
- Query understanding and analysis

### **03-intelligent-routing.ipynb** - Smart Routing
- Function calling for query classification
- Multi-index routing and classification
- Structured output with Pydantic models
- Intelligent query routing based on content type

### **04-advanced-indexing.ipynb** - Advanced Indexing
- Multi-representation indexing
- Semi-structured document processing
- Multi-modal indexing techniques
- Summary-based indexing strategies

### **05-retrieval-optimization.ipynb** - Performance
- Re-ranking techniques for better relevance
- Hybrid search combining semantic and keyword search
- Contextual retrieval strategies
- Advanced retrieval optimization

## 🏗️ Tech Stack

Our implementation uses a modern, production-ready tech stack:

- **[LangChain](https://python.langchain.com/)**: Core RAG framework and orchestration
- **[Google Gemini](https://ai.google.dev/)**: Advanced LLM for generation and embeddings
- **[ChromaDB](https://www.trychroma.com/)**: Vector database for similarity search
- **[LangSmith](https://smith.langchain.com/)**: Observability and debugging platform


For detailed technical specifications and setup instructions, see our **[Tech Stack Documentation](docs/techstack.md)**.

## 🎓 Learning Path

```
01-rag-basics.ipynb     → Understand core RAG concepts
         ↓
02-query-enhancement.ipynb → Optimize query processing
         ↓
03-intelligent-routing.ipynb → Add smart routing
         ↓
04-advanced-indexing.ipynb → Implement advanced indexing
         ↓
05-retrieval-optimization.ipynb → Optimize for production
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd RAG-from-scratch
   ```

2. **Set up your environment**
   - Install Python 3.13+
   - Create a virtual environment
   - Install dependencies: `pip install -r requirements.txt`

3. **Configure credentials**
   - Set up your Google Gemini API key
   - Configure LangSmith for tracing (optional)

4. **Start learning**
   - Begin with `01-rag-basics.ipynb`
   - Follow the notebooks in order
   - Experiment with your own data

For detailed setup instructions, see **[Setup and Run Guide](docs/rag_from_scratch-setup-and-run.md)**.

## 📊 Project Structure

```
RAG-from-scratch/
├── 📓 01-rag-basics.ipynb              # Core RAG concepts
├── 📓 02-query-enhancement.ipynb       # Query optimization
├── 📓 03-intelligent-routing.ipynb     # Smart routing
├── 📓 04-advanced-indexing.ipynb       # Advanced indexing
├── 📓 05-retrieval-optimization.ipynb  # Performance optimization
├── 📁 docs/                            # Documentation
│   ├── techstack.md                    # Technical specifications
│   ├── setup-and-run.md               # Setup instructions
│   └── security-scan.md               # Security documentation
├── 📄 requirements.txt                 # Python dependencies
└── 📄 README.md                        # This file
```

## 🎯 Conclusions

This tutorial series provides a comprehensive foundation for building production-ready RAG applications. By following these notebooks, you'll gain:

- **Practical Experience**: Hands-on implementation of real RAG systems
- **Best Practices**: Industry-standard approaches and techniques
- **Production Readiness**: Scalable, maintainable, and secure implementations
- **Problem-Solving Skills**: Ability to tackle real-world RAG challenges

RAG represents a fundamental shift in how we build AI applications, enabling systems that are more accurate, transparent, and capable than traditional LLM approaches. This project equips you with the knowledge and skills to leverage this powerful technology effectively.

**Ready to build the future of AI? Start with the first notebook and begin your RAG journey! 🚀**

---

Happy learning!