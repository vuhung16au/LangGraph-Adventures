#!/usr/bin/env python3
"""
Test Script for Conversational RAG System
=========================================

This script tests the conversational RAG system functionality.
"""

import os
import sys
import time
import json
from datetime import datetime

# Import our conversational RAG system
from conversational_rag import ConversationalRAGSystem, ConversationSession, ConversationMessage

def test_conversational_rag_system():
    """Test the conversational RAG system"""
    print("🚀 Conversational RAG System Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: System initialization
        print("\n1. Testing system initialization...")
        system = ConversationalRAGSystem(
            model_name="llama3.1:8b-instruct-q8_0",
            embedding_model="sentence-transformers/all-MiniLM-L6-v2",
            vector_store_path="./test_conversational_chroma_db",
            chunk_size=1000,
            chunk_overlap=200,
            k_retrieve=4
        )
        print("✓ Conversational RAG system initialized")
        
        # Test 2: Create sample documents
        print("\n2. Testing with sample documents...")
        from langchain.schema import Document
        
        sample_docs = [
            Document(
                page_content="RAG (Retrieval-Augmented Generation) is a technique that combines information retrieval with text generation. It works by first retrieving relevant documents from a knowledge base and then using those documents to generate more accurate and informative responses.",
                metadata={"source": "sample1", "type": "webpage"}
            ),
            Document(
                page_content="Conversational AI systems maintain context across multiple interactions. This allows users to ask follow-up questions and have more natural conversations. The system remembers previous questions and answers to provide better responses.",
                metadata={"source": "sample2", "type": "webpage"}
            ),
            Document(
                page_content="LangGraph is a library for building stateful, multi-actor applications with Large Language Models. It provides tools for creating complex workflows and managing conversation state.",
                metadata={"source": "sample3", "type": "webpage"}
            )
        ]
        print("✓ Created 3 sample documents")
        
        # Test 3: Document splitting
        print("\n3. Testing document splitting...")
        split_docs = system.split_documents(sample_docs)
        print(f"✓ Split {len(sample_docs)} documents into {len(split_docs)} chunks")
        
        # Test 4: Vector store creation
        print("\n4. Testing vector store creation...")
        vectorstore = system.create_vectorstore(split_docs)
        print("✓ Vector store created successfully")
        
        # Test 5: Conversational chain setup
        print("\n5. Testing conversational chain setup...")
        system.setup_conversational_chain(vectorstore)
        print("✓ Conversational retrieval chain set up")
        
        # Test 6: Session management
        print("\n6. Testing session management...")
        session_id = system.create_session("test_session")
        print(f"✓ Created session: {session_id}")
        
        # Test 7: Basic conversation
        print("\n7. Testing basic conversation...")
        response = system.query("What is RAG?", session_id)
        print(f"✓ Query processed in {response['query_time']:.2f}s")
        print(f"   Answer: {response['answer'][:100]}...")
        print(f"   Sources: {len(response['source_documents'])}")
        print(f"   Messages in session: {response['message_count']}")
        
        # Test 8: Follow-up questions
        print("\n8. Testing follow-up questions...")
        follow_up_response = system.query("How does it work?", session_id)
        print(f"✓ Follow-up query processed in {follow_up_response['query_time']:.2f}s")
        print(f"   Answer: {follow_up_response['answer'][:100]}...")
        print(f"   Messages in session: {follow_up_response['message_count']}")
        
        # Test 9: Conversation history
        print("\n9. Testing conversation history...")
        messages = system.get_conversation_history(session_id)
        print(f"✓ Retrieved {len(messages)} messages from conversation history")
        
        # Test 10: Multiple sessions
        print("\n10. Testing multiple sessions...")
        session_id_2 = system.create_session("test_session_2")
        response_2 = system.query("What is conversational AI?", session_id_2)
        print(f"✓ Second session query processed in {response_2['query_time']:.2f}s")
        print(f"   Messages in session 1: {len(system.get_conversation_history(session_id))}")
        print(f"   Messages in session 2: {len(system.get_conversation_history(session_id_2))}")
        
        # Test 11: Session persistence
        print("\n11. Testing session persistence...")
        system.save_sessions("test_sessions.json")
        print("✓ Sessions saved to file")
        
        # Test 12: Session loading
        print("\n12. Testing session loading...")
        new_system = ConversationalRAGSystem()
        new_system.load_sessions("test_sessions.json")
        loaded_sessions = new_system.list_sessions()
        print(f"✓ Loaded {len(loaded_sessions)} sessions from file")
        
        # Test 13: System information
        print("\n13. Testing system information...")
        system_info = system.get_system_info()
        print(f"✓ Retrieved system information: {len(system_info)} properties")
        
        # Cleanup
        print("\n14. Cleaning up...")
        system.delete_session(session_id)
        system.delete_session(session_id_2)
        if os.path.exists("test_sessions.json"):
            os.remove("test_sessions.json")
        print("✓ Cleanup completed")
        
        print("\n🎉 All conversational RAG system tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_interface():
    """Test the CLI interface"""
    print("\n🔧 Testing CLI Interface")
    print("=" * 40)
    
    try:
        # Test CLI import
        from conversational_cli import cli, load_system_info, display_system_info
        print("✓ CLI interface imported successfully")
        
        # Test helper functions
        test_info = {"test": "data"}
        display_system_info(test_info)
        print("✓ CLI helper functions working")
        
        print("\n✓ CLI interface tests passed")
        return True
        
    except Exception as e:
        print(f"\n❌ CLI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing Conversational RAG System")
    print("=" * 50)
    
    # Test core system
    core_success = test_conversational_rag_system()
    
    # Test CLI interface
    cli_success = test_cli_interface()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    if core_success:
        print("✅ Core conversational RAG system: PASSED")
    else:
        print("❌ Core conversational RAG system: FAILED")
    
    if cli_success:
        print("✅ CLI interface: PASSED")
    else:
        print("❌ CLI interface: FAILED")
    
    if core_success and cli_success:
        print("\n🎉 All tests passed! The conversational RAG system is ready to use.")
        print("\nNext steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Build a conversational RAG system: python conversational_cli.py build -u 'https://example.com'")
        print("3. Start chatting: python conversational_cli.py chat")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
