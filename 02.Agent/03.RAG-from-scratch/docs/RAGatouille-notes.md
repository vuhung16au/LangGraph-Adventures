# RAGatouille Removal Notes

## Overview

RAGatouille was removed from the project dependencies due to significant dependency conflicts with the current LangChain ecosystem. This document explains the issues encountered and provides alternative solutions.

## 🚨 Why RAGatouille Was Removed

### **Primary Issues**

1. **Missing Private Dependency**: `voyager`
   - RAGatouille depends on a private `voyager` package not available on PyPI
   - This package is required for core functionality but cannot be installed publicly
   - Attempts to create mock implementations were insufficient for full functionality

2. **Version Conflicts with LangChain**
   - **LangChain**: RAGatouille 0.0.8.x requires `langchain<0.2.0`, but we use `langchain>=0.3.20`
   - **Sentence Transformers**: RAGatouille 0.0.8.x requires `sentence-transformers<3.0.0`, but we use `sentence-transformers>=5.0.0`
   - **AioHTTP**: RAGatouille 0.0.7.x requires `aiohttp==3.9.1`, but LangChain requires `aiohttp>=3.8.3`

3. **Dependency Resolution Failures**
   ```
   ERROR: ResolutionImpossible: 
   - ragatouille 0.0.9.post2 depends on voyager (not available)
   - ragatouille 0.0.8.post4 depends on sentence-transformers<3.0.0
   - ragatouille 0.0.8.post3 depends on langchain<0.2.0
   - langchain-community 0.3.26 depends on aiohttp<4.0.0,>=3.8.3
   - ragatouille 0.0.7.post11 depends on aiohttp==3.9.1
   ```

### **Attempted Solutions**

1. **Mock Voyager Implementation**
   - Created mock `voyager` module with basic classes
   - Provided `Index`, `Space`, `StorageDataType` classes
   - Insufficient for full RAGatouille functionality

2. **Version Pinning**
   - Attempted to pin specific versions to resolve conflicts
   - Resulted in breaking other core dependencies
   - Not sustainable for long-term maintenance

3. **Alternative Installation Methods**
   - Tried installing from source
   - Attempted manual dependency resolution
   - All approaches failed due to fundamental incompatibilities

## 🔄 Alternative Solutions

### **1. LlamaIndex (Recommended)**

**What it provides:**
- Advanced document processing pipelines
- Sophisticated indexing strategies
- Query engines and retrievers
- Structured data handling
- RAG-specific optimizations

**Installation:**
```bash
pip install llama-index>=0.13.0
```

**Key Features:**
- Document processing and chunking
- Advanced retrieval strategies
- Query optimization
- Structured outputs
- Multi-modal support

**Example Usage:**
```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine

# Load documents
documents = SimpleDirectoryReader('data/').load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Create retriever
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# Create query engine
query_engine = RetrieverQueryEngine.from_args(retriever)
response = query_engine.query("Your question here")
```

### **2. Custom RAG Implementation with LangChain**

**Components Available:**
- **Document Loaders**: `langchain.document_loaders`
- **Text Splitters**: `langchain.text_splitter`
- **Embeddings**: `langchain.embeddings`
- **Vector Stores**: `langchain.vectorstores`
- **Retrievers**: `langchain.retrievers`
- **Rerankers**: `langchain.retrievers.document_compressors`

**Example Implementation:**
```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Load and split documents
loader = TextLoader("data.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = GoogleGenerativeAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)

# Create retriever with reranking
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
compressor = CohereRerank()
retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=compressor
)
```

### **3. Advanced Retrieval with FAISS**

**High-performance similarity search:**
```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create FAISS index
dimension = model.get_sentence_embedding_dimension()
index = faiss.IndexFlatIP(dimension)  # Inner product for cosine similarity

# Add vectors to index
embeddings = model.encode(texts)
index.add(embeddings.astype('float32'))

# Search
query_embedding = model.encode([query])
D, I = index.search(query_embedding.astype('float32'), k=5)
```

### **4. Reranking with Cohere**

**Improve retrieval quality:**
```python
from langchain.retrievers.document_compressors import CohereRerank
from langchain.retrievers import ContextualCompressionRetriever

# Create reranker
reranker = CohereRerank(
    model="rerank-english-v2.0",
    top_n=5
)

# Apply to existing retriever
compression_retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=reranker
)
```

## 📊 Feature Comparison

| Feature | RAGatouille | LlamaIndex | Custom LangChain | FAISS + Cohere |
|---------|-------------|------------|------------------|----------------|
| Document Processing | ✅ | ✅ | ✅ | ✅ |
| Advanced Indexing | ✅ | ✅ | ✅ | ✅ |
| Reranking | ✅ | ✅ | ✅ | ✅ |
| Query Optimization | ✅ | ✅ | ✅ | ✅ |
| Structured Outputs | ✅ | ✅ | ✅ | ✅ |
| Multi-modal | ✅ | ✅ | ✅ | ✅ |
| Production Ready | ✅ | ✅ | ✅ | ✅ |
| Active Maintenance | ❌ | ✅ | ✅ | ✅ |
| Dependency Conflicts | ❌ | ✅ | ✅ | ✅ |

## 🛠️ Migration Guide

### **From RAGatouille to LlamaIndex**

**Before (RAGatouille):**
```python
from ragatouille import RAGPretrainedModel

# Initialize model
rag = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")

# Index documents
rag.index(
    collection=documents,
    index_name="my_index",
    max_document_length=512
)

# Search
results = rag.search("query", k=5)
```

**After (LlamaIndex):**
```python
from llama_index import VectorStoreIndex, Document
from llama_index.retrievers import VectorIndexRetriever

# Create documents
docs = [Document(text=doc) for doc in documents]

# Create index
index = VectorStoreIndex.from_documents(docs)

# Create retriever
retriever = VectorIndexRetriever(index=index, similarity_top_k=5)

# Search
results = retriever.retrieve("query")
```

### **From RAGatouille to Custom LangChain**

**Before (RAGatouille):**
```python
from ragatouille import RAGTrainer

# Train custom model
trainer = RAGTrainer(
    model_name="colbert-ir/colbertv2.0",
    data_path="training_data.json"
)
trainer.train()
```

**After (Custom LangChain):**
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Create advanced retriever
base_retriever = vectorstore.as_retriever(search_kwargs={"k": 20})
reranker = CohereRerank(model="rerank-english-v2.0", top_n=5)
retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    base_compressor=reranker
)
```

## 🎯 Recommendations

### **For New Projects**
1. **Start with LlamaIndex** - Most comprehensive RAG framework
2. **Use LangChain for orchestration** - Best for complex workflows
3. **Add Cohere reranking** - For improved retrieval quality
4. **Consider FAISS for large-scale** - For high-performance similarity search

### **For Existing Projects**
1. **Migrate to LlamaIndex** - If you need advanced RAG features
2. **Use Custom LangChain** - If you prefer more control
3. **Implement Cohere reranking** - For better retrieval results
4. **Add FAISS** - For performance optimization

### **For Production**
1. **LangChain + ChromaDB** - For robust, scalable solutions
2. **LlamaIndex** - For advanced RAG capabilities
3. **Cohere Reranking** - For improved accuracy
4. **FAISS** - For high-performance search

## 📚 Additional Resources

- **LlamaIndex Documentation**: [https://docs.llamaindex.ai/](https://docs.llamaindex.ai/)
- **LangChain RAG Guide**: [https://python.langchain.com/docs/use_cases/question_answering/](https://python.langchain.com/docs/use_cases/question_answering/)
- **Cohere Reranking**: [https://docs.cohere.ai/reference/rerank](https://docs.cohere.ai/reference/rerank)
- **FAISS Documentation**: [https://github.com/facebookresearch/faiss](https://github.com/facebookresearch/faiss)

## 🔮 Future Considerations

### **Potential RAGatouille Return**
- If RAGatouille resolves dependency conflicts
- If `voyager` package becomes publicly available
- If version compatibility improves

### **Alternative RAG Frameworks**
- **Haystack**: Deepset's RAG framework
- **Weaviate**: Vector database with RAG capabilities
- **Pinecone**: Managed vector database with RAG features

### **Custom Solutions**
- Build custom RAG implementations using available components
- Combine multiple frameworks for specific use cases
- Use specialized libraries for specific domains

---

*This document will be updated as new alternatives become available or if RAGatouille resolves its dependency issues.*
