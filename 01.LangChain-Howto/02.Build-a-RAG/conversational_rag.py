"""
Conversational RAG System with Chat History
===========================================

This module implements a conversational RAG system that maintains conversation history
and allows for follow-up questions using LangGraph for workflow orchestration.
"""

import os
import time
import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# LangChain imports
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document, BaseMessage, HumanMessage, AIMessage
from langchain_ollama import OllamaLLM
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# LangGraph imports
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Web scraping
import requests
from bs4 import BeautifulSoup

# Rich for beautiful output
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversational_rag.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

console = Console()

@dataclass
class ConversationMessage:
    """Represents a message in the conversation"""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class ConversationSession:
    """Represents a conversation session"""
    session_id: str
    messages: List[ConversationMessage]
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None

class ConversationalRAGSystem:
    """
    Conversational RAG System with chat history support
    """
    
    def __init__(
        self,
        model_name: str = "llama3.1:8b-instruct-q8_0",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        vector_store_path: str = "./conversational_chroma_db",
        max_tokens: int = 4096,
        temperature: float = 0.1,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        k_retrieve: int = 4
    ):
        """
        Initialize the conversational RAG system
        
        Args:
            model_name: Ollama model name
            embedding_model: HuggingFace embedding model
            vector_store_path: Path to store vector database
            max_tokens: Maximum tokens for responses
            temperature: Model temperature
            chunk_size: Document chunk size
            chunk_overlap: Document chunk overlap
            k_retrieve: Number of documents to retrieve
        """
        self.model_name = model_name
        self.embedding_model = embedding_model
        self.vector_store_path = vector_store_path
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.k_retrieve = k_retrieve
        
        # Initialize components
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.conversation_chain = None
        self.memory = None
        
        # Conversation sessions
        self.sessions: Dict[str, ConversationSession] = {}
        
        # Initialize the system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the RAG system components"""
        logger.info("Initializing conversational RAG system components...")
        
        try:
            # Initialize LLM
            self.llm = OllamaLLM(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embedding_model
            )
            
            # Initialize memory
            self.memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer"
            )
            
            # Try to load existing vector store
            self._load_existing_vectorstore()
            
            logger.info(f"Conversational RAG system initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing conversational RAG system: {e}")
            raise
    
    def _load_existing_vectorstore(self):
        """Load existing vector store if available"""
        try:
            if os.path.exists(self.vector_store_path):
                logger.info(f"Loading existing vector store from: {self.vector_store_path}")
                self.vectorstore = Chroma(
                    persist_directory=self.vector_store_path,
                    embedding_function=self.embeddings
                )
                
                # Set up conversational chain if vector store is loaded
                self.setup_conversational_chain(self.vectorstore)
                logger.info("Existing vector store loaded successfully")
            else:
                logger.info("No existing vector store found")
        except Exception as e:
            logger.warning(f"Could not load existing vector store: {e}")
            logger.info("Will create new vector store when building system")
    
    def validate_url(self, url: str) -> str:
        """
        Validate and normalize a URL
        
        Args:
            url: URL to validate
            
        Returns:
            Normalized URL
        """
        try:
            # Basic URL validation
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Parse URL to check for common issues
            from urllib.parse import urlparse
            parsed = urlparse(url)
            
            # Check for common typos in domain names
            domain = parsed.netloc.lower()
            if 'github.ioposts' in domain:
                domain = domain.replace('github.ioposts', 'github.io/posts')
                url = f"{parsed.scheme}://{domain}{parsed.path}"
                logger.info(f"Fixed URL typo: {url}")
            
            return url
            
        except Exception as e:
            logger.error(f"Error validating URL {url}: {e}")
            raise
    
    def fetch_url_content(self, url: str) -> str:
        """
        Fetch content from a URL
        
        Args:
            url: URL to fetch content from
            
        Returns:
            Extracted text content from the URL
        """
        try:
            # Validate and normalize URL
            url = self.validate_url(url)
            
            logger.info(f"Fetching content from: {url}")
            start_time = time.time()
            
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            fetch_time = time.time() - start_time
            logger.info(f"Fetched content in {fetch_time:.2f}s, length: {len(text)} characters")
            
            return text
            
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {e}")
            raise
    
    def create_documents(self, urls: List[str]) -> List[Document]:
        """
        Create documents from URLs
        
        Args:
            urls: List of URLs to fetch
            
        Returns:
            List of Document objects
        """
        documents = []
        
        for url in urls:
            try:
                content = self.fetch_url_content(url)
                doc = Document(
                    page_content=content,
                    metadata={"source": url, "type": "webpage"}
                )
                documents.append(doc)
                logger.info(f"Created document from: {url}")
                
            except Exception as e:
                logger.error(f"Error creating document from {url}: {e}")
                continue
        
        logger.info(f"Created {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        
        Args:
            documents: List of documents to split
            
        Returns:
            List of split documents
        """
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
            )
            
            split_docs = text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")
            
            return split_docs
            
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create vector store from documents
        
        Args:
            documents: List of documents to index
            
        Returns:
            Chroma vector store
        """
        try:
            logger.info("Creating vector store...")
            start_time = time.time()
            
            # Create vector store
            vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.vector_store_path
            )
            
            # Persist the vector store
            vectorstore.persist()
            
            create_time = time.time() - start_time
            logger.info(f"Vector store created in {create_time:.2f}s")
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def setup_conversational_chain(self, vectorstore: Chroma):
        """
        Set up the conversational retrieval chain
        
        Args:
            vectorstore: Chroma vector store
        """
        try:
            logger.info("Setting up conversational retrieval chain...")
            
            # Create the conversational chain
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": self.k_retrieve}),
                memory=self.memory,
                return_source_documents=True,
                verbose=False
            )
            
            logger.info("Conversational retrieval chain set up successfully")
            
        except Exception as e:
            logger.error(f"Error setting up conversational chain: {e}")
            raise
    
    def build_rag_from_urls(self, urls: List[str], output_file: str = "conversational_rag_system.json") -> Dict[str, Any]:
        """
        Build RAG system from URLs
        
        Args:
            urls: List of URLs to fetch
            output_file: Output file for system info
            
        Returns:
            System information dictionary
        """
        try:
            logger.info(f"Building conversational RAG system from {len(urls)} URLs")
            start_time = time.time()
            
            # Create documents
            documents = self.create_documents(urls)
            
            # Split documents
            split_docs = self.split_documents(documents)
            
            # Create vector store
            self.vectorstore = self.create_vectorstore(split_docs)
            
            # Set up conversational chain
            self.setup_conversational_chain(self.vectorstore)
            
            # Save system info
            system_info = {
                "model": self.model_name,
                "embedding_model": self.embedding_model,
                "urls": urls,
                "vector_store_path": self.vector_store_path,
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
                "k_retrieve": self.k_retrieve,
                "created_at": datetime.now().isoformat(),
                "document_count": len(documents),
                "chunk_count": len(split_docs)
            }
            
            with open(output_file, 'w') as f:
                json.dump(system_info, f, indent=2)
            
            build_time = time.time() - start_time
            logger.info(f"Conversational RAG system built successfully in {build_time:.2f}s")
            
            return system_info
            
        except Exception as e:
            logger.error(f"Error building conversational RAG system: {e}")
            raise
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """
        Create a new conversation session
        
        Args:
            session_id: Optional session ID, auto-generated if not provided
            
        Returns:
            Session ID
        """
        if session_id is None:
            session_id = f"session_{int(time.time())}"
        
        session = ConversationSession(
            session_id=session_id,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            metadata={"model": self.model_name}
        )
        
        self.sessions[session_id] = session
        logger.info(f"Created conversation session: {session_id}")
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ConversationSession]:
        """
        Get a conversation session
        
        Args:
            session_id: Session ID
            
        Returns:
            Conversation session or None if not found
        """
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[str]:
        """
        List all session IDs
        
        Returns:
            List of session IDs
        """
        return list(self.sessions.keys())
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session
        
        Args:
            session_id: Session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Deleted conversation session: {session_id}")
            return True
        return False
    
    def add_message(self, session_id: str, role: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Add a message to a conversation session
        
        Args:
            session_id: Session ID
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        message = ConversationMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata
        )
        
        self.sessions[session_id].messages.append(message)
        self.sessions[session_id].updated_at = datetime.now()
        
        logger.info(f"Added {role} message to session {session_id}")
    
    def get_conversation_history(self, session_id: str) -> List[ConversationMessage]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session ID
            
        Returns:
            List of conversation messages
        """
        if session_id not in self.sessions:
            return []
        
        return self.sessions[session_id].messages.copy()
    
    def query(self, question: str, session_id: str) -> Dict[str, Any]:
        """
        Query the conversational RAG system
        
        Args:
            question: User question
            session_id: Session ID for conversation history
            
        Returns:
            Response dictionary with answer, sources, and metadata
        """
        try:
            if self.conversation_chain is None:
                raise ValueError("Conversational RAG system not built. Run build_rag_from_urls() first.")
            
            if session_id not in self.sessions:
                self.create_session(session_id)
            
            logger.info(f"Processing conversational query: {question}")
            start_time = time.time()
            
            # Add user message to session
            self.add_message(session_id, "user", question)
            
            # Query the system
            response = self.conversation_chain({"question": question})
            
            answer = response.get("answer", "")
            source_documents = response.get("source_documents", [])
            
            # Add assistant message to session
            self.add_message(session_id, "assistant", answer, {
                "source_documents": len(source_documents),
                "query_time": time.time() - start_time
            })
            
            query_time = time.time() - start_time
            logger.info(f"Conversational query processed in {query_time:.2f}s")
            
            return {
                "answer": answer,
                "source_documents": source_documents,
                "query_time": query_time,
                "session_id": session_id,
                "message_count": len(self.sessions[session_id].messages)
            }
            
        except Exception as e:
            logger.error(f"Error processing conversational query: {e}")
            raise
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information
        
        Returns:
            System information dictionary
        """
        return {
            "model": self.model_name,
            "embedding_model": self.embedding_model,
            "vector_store_path": self.vector_store_path,
            "session_count": len(self.sessions),
            "sessions": list(self.sessions.keys()),
            "memory_type": "ConversationBufferMemory",
            "retriever_k": self.k_retrieve
        }
    
    def save_sessions(self, filepath: str):
        """
        Save conversation sessions to file
        
        Args:
            filepath: File path to save sessions
        """
        try:
            sessions_data = {}
            for session_id, session in self.sessions.items():
                sessions_data[session_id] = {
                    "session_id": session.session_id,
                    "messages": [
                        {
                            "role": msg.role,
                            "content": msg.content,
                            "timestamp": msg.timestamp.isoformat(),
                            "metadata": msg.metadata
                        }
                        for msg in session.messages
                    ],
                    "created_at": session.created_at.isoformat(),
                    "updated_at": session.updated_at.isoformat(),
                    "metadata": session.metadata
                }
            
            with open(filepath, 'w') as f:
                json.dump(sessions_data, f, indent=2)
            
            logger.info(f"Saved {len(self.sessions)} sessions to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving sessions: {e}")
            raise
    
    def load_sessions(self, filepath: str):
        """
        Load conversation sessions from file
        
        Args:
            filepath: File path to load sessions from
        """
        try:
            with open(filepath, 'r') as f:
                sessions_data = json.load(f)
            
            self.sessions.clear()
            for session_id, session_data in sessions_data.items():
                session = ConversationSession(
                    session_id=session_data["session_id"],
                    messages=[
                        ConversationMessage(
                            role=msg["role"],
                            content=msg["content"],
                            timestamp=datetime.fromisoformat(msg["timestamp"]),
                            metadata=msg.get("metadata")
                        )
                        for msg in session_data["messages"]
                    ],
                    created_at=datetime.fromisoformat(session_data["created_at"]),
                    updated_at=datetime.fromisoformat(session_data["updated_at"]),
                    metadata=session_data.get("metadata")
                )
                self.sessions[session_id] = session
            
            logger.info(f"Loaded {len(self.sessions)} sessions from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")
            raise
