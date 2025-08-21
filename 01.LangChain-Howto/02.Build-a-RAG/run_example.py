#!/usr/bin/env python3
"""
Example script to demonstrate the RAG system

This script shows how to use the RAG system with the specified URLs.
"""

import os
import sys
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.append('.')

def main():
    """Main example function"""
    
    print("🚀 RAG System Example")
    print("=" * 50)
    
    try:
        # Import RAG system
        from rag_system import RAGSystem
        
        # Define URLs (from the prompt)
        urls = [
            "https://python.langchain.com/docs/tutorials/rag/",
            "https://lilianweng.github.io/posts/2023-06-23-agent/"
        ]
        
        print(f"📚 Processing {len(urls)} URLs:")
        for i, url in enumerate(urls, 1):
            print(f"   {i}. {url}")
        
        # Initialize RAG system
        print(f"\n🤖 Initializing RAG system with Ollama...")
        rag = RAGSystem()
        
        # Build RAG system
        print(f"\n🔨 Building RAG system from URLs...")
        start_time = time.time()
        rag.build_rag_from_urls(urls)
        build_time = time.time() - start_time
        
        print(f"✅ RAG system built in {build_time:.2f} seconds")
        
        # Test questions
        test_questions = [
            "What is RAG and how does it work?",
            "What are the key components of a RAG system?",
            "How do agents work in AI systems?",
            "What is the difference between RAG and traditional search?"
        ]
        
        print(f"\n❓ Testing with {len(test_questions)} questions:")
        print("=" * 60)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {question}")
            print("-" * 40)
            
            # Query the system
            start_time = time.time()
            result = rag.query(question)
            query_time = time.time() - start_time
            
            # Display results
            print(f"Answer: {result['answer']}")
            print(f"Query time: {query_time:.2f}s")
            print(f"Source documents: {len(result['source_documents'])}")
            
            # Show source previews
            for j, doc in enumerate(result['source_documents'][:2], 1):
                source = doc.metadata.get('source', 'Unknown')
                preview = doc.page_content[:100] + "..."
                print(f"  Source {j}: {source}")
                print(f"  Preview: {preview}")
        
        print("\n" + "=" * 60)
        print("🎉 Example completed successfully!")
        print("\n💡 Try running the interactive mode:")
        print("   python rag_cli.py query -i")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure:")
        print("1. Ollama is running: ollama serve")
        print("2. You have the required model: ollama pull llama3.1:8b-instruct-q8_0")
        sys.exit(1)

if __name__ == "__main__":
    main()
