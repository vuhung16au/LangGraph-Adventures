# Cohere Rerank Error Fix

## Problem
The original code was failing with a `NotFoundError` because it was using a deprecated model `rerank-english-v2.0` that is no longer available.

## Error Details
```
NotFoundError: model 'rerank-english-v2.0' not found, make sure the correct model ID was used and that you have access to the model.
```

## Root Causes
1. **Deprecated Model**: The model `rerank-english-v2.0` has been deprecated and is no longer available
2. **Deprecated Import**: The import path `from langchain.retrievers.document_compressors import CohereRerank` is deprecated
3. **Deprecated Method**: Using `get_relevant_documents()` instead of `invoke()`

## Solution

### 1. Install Updated Package
```bash
pip install -U langchain-cohere
```

### 2. Update the Code

**Original (Broken) Code:**
```python
from langchain.retrievers.document_compressors import CohereRerank

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Re-rank
compressor = CohereRerank()
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

compressed_docs = compression_retriever.get_relevant_documents(question)
```

**Fixed Code:**
```python
from langchain_cohere import CohereRerank  # Updated import

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

# Use the working model
compressor = CohereRerank(model="rerank-english-v3.0")
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

# Use invoke instead of get_relevant_documents
compressed_docs = compression_retriever.invoke(question)
print(f"Retrieved {len(compressed_docs)} compressed documents")
```

### 3. Key Changes Made

1. **Import Path**: Changed from `langchain.retrievers.document_compressors` to `langchain_cohere`
2. **Model**: Changed from `rerank-english-v2.0` to `rerank-english-v3.0`
3. **Method**: Changed from `get_relevant_documents()` to `invoke()`

### 4. Alternative Models to Try

If `rerank-english-v3.0` doesn't work, you can try these models in order:
- `rerank-english-v3.0` ✅ (Working)
- `rerank-multilingual-v2.0` ❌ (Not available)
- `rerank-v2.0` ❌ (Not available)
- Default model (no specification)

### 5. Error Handling Version

For production use, consider this robust version with error handling:

```python
from langchain_cohere import CohereRerank

retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

try:
    # Use the working model
    compressor = CohereRerank(model="rerank-english-v3.0")
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    
    compressed_docs = compression_retriever.invoke(question)
    print(f"✅ Successfully retrieved {len(compressed_docs)} compressed documents")
    
except Exception as e:
    print(f"❌ Cohere rerank failed: {e}")
    print("🔄 Falling back to regular retrieval...")
    compressed_docs = retriever.invoke(question)
    print(f"✅ Retrieved {len(compressed_docs)} documents using regular retrieval")
```

## Testing

The fix has been tested and confirmed working. The script `fix_cohere_rerank_final.py` demonstrates the working implementation.

## Results

After applying the fix:
- ✅ No more `NotFoundError`
- ✅ No more deprecation warnings
- ✅ Successfully retrieves 3 compressed documents
- ✅ Proper relevance scoring with metadata

## Files Created

1. `fix_cohere_rerank.py` - Initial testing script
2. `fix_cohere_rerank_final.py` - Final working solution
3. `COHERE_RERANK_FIX.md` - This documentation

## Next Steps

1. Update your notebook with the fixed code
2. Consider implementing error handling for robustness
3. Test with different queries to ensure consistency
