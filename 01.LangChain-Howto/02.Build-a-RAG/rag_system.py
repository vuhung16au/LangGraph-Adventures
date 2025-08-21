"""
RAG System using LangGraph and Ollama

This module implements a Retrieval-Augmented Generation (RAG) system that can:
1. Fetch and process content from URLs
2. Create embeddings and store them in a vector database
3. Retrieve relevant documents for user queries
4. Generate answers using an Ollama model

Author: AI Assistant
Date: 2024
"""

import os
import logging
import time
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from langchain_ollama import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langgraph.graph import StateGraph, END
from langchain.tools import tool

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'rag_system.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RAGSystem:
    """
    A Retrieval-Augmented Generation system using LangGraph and Ollama
    """
    
    def __init__(self, model_name: str = None):
        """
        Initialize the RAG system
        
        Args:
            model_name: Name of the Ollama model to use
        """
        self.model_name = model_name or os.getenv('OLLAMA_MODEL', 'llama3.1:8b-instruct-q8_0')
        self.llm = None
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None
        
        # Initialize components
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all RAG system components"""
        try:
            logger.info("Initializing RAG system components...")
            
            # Initialize Ollama LLM
            self.llm = OllamaLLM(
                model=self.model_name,
                temperature=float(os.getenv('TEMPERATURE', '0.1')),
                max_tokens=int(os.getenv('MAX_TOKENS', '4096'))
            )
            
            # Initialize embeddings
            embedding_model = os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
            self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
            
            logger.info(f"RAG system initialized with model: {self.model_name}")
            
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
            raise
    
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
            
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
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
    
    def create_documents(self, texts: List[str], urls: List[str]) -> List[Document]:
        """
        Create Document objects from texts and URLs
        
        Args:
            texts: List of text contents
            urls: List of corresponding URLs
            
        Returns:
            List of Document objects
        """
        documents = []
        for text, url in zip(texts, urls):
            # Create metadata
            metadata = {
                'source': url,
                'domain': urlparse(url).netloc,
                'length': len(text)
            }
            
            # Create document
            doc = Document(page_content=text, metadata=metadata)
            documents.append(doc)
            
        logger.info(f"Created {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of split Document objects
        """
        try:
            chunk_size = int(os.getenv('CHUNK_SIZE', '1000'))
            chunk_overlap = int(os.getenv('CHUNK_OVERLAP', '200'))
            
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                separators=["\n\n", "\n", " ", ""]
            )
            
            split_docs = text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(split_docs)} chunks")
            
            return split_docs
            
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise
    
    def create_vectorstore(self, documents: List[Document]) -> Chroma:
        """
        Create a vector store from documents
        
        Args:
            documents: List of Document objects
            
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
                persist_directory="./chroma_db"
            )
            
            # Persist the vector store
            vectorstore.persist()
            
            creation_time = time.time() - start_time
            logger.info(f"Vector store created in {creation_time:.2f}s")
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def setup_retrieval_qa(self, vectorstore: Chroma):
        """
        Set up the retrieval QA chain
        
        Args:
            vectorstore: Chroma vector store
        """
        try:
            # Create retriever
            self.retriever = vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 4}
            )
            
            # Create prompt template
            prompt_template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            
            Context: {context}
            
            Question: {question}
            
            Answer:"""
            
            prompt = PromptTemplate(
                template=prompt_template,
                input_variables=["context", "question"]
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": prompt}
            )
            
            logger.info("Retrieval QA chain set up successfully")
            
        except Exception as e:
            logger.error(f"Error setting up retrieval QA: {e}")
            raise
    
    def build_rag_from_urls(self, urls: List[str]):
        """
        Build the RAG system from a list of URLs
        
        Args:
            urls: List of URLs to fetch and process
        """
        try:
            logger.info(f"Building RAG system from {len(urls)} URLs")
            start_time = time.time()
            
            # Fetch content from URLs
            texts = []
            for url in urls:
                text = self.fetch_url_content(url)
                texts.append(text)
            
            # Create documents
            documents = self.create_documents(texts, urls)
            
            # Split documents
            split_docs = self.split_documents(documents)
            
            # Create vector store
            self.vectorstore = self.create_vectorstore(split_docs)
            
            # Set up retrieval QA
            self.setup_retrieval_qa(self.vectorstore)
            
            build_time = time.time() - start_time
            logger.info(f"RAG system built successfully in {build_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error building RAG system: {e}")
            raise
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the RAG system with a question
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing answer and source documents
        """
        try:
            if not self.qa_chain:
                raise ValueError("RAG system not initialized. Call build_rag_from_urls() first.")
            
            logger.info(f"Processing query: {question}")
            start_time = time.time()
            
            # Get response from QA chain
            response = self.qa_chain({"query": question})
            
            query_time = time.time() - start_time
            logger.info(f"Query processed in {query_time:.2f}s")
            
            return {
                'answer': response['result'],
                'source_documents': response['source_documents'],
                'query_time': query_time
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise

# LangGraph state definition
from typing import TypedDict, List

class RAGState(TypedDict):
    """State for the RAG system workflow"""
    question: str
    answer: str
    source_documents: List[Document]
    error: str
    rag_system: Any

# LangGraph nodes
def retrieve_documents(state: RAGState) -> RAGState:
    """Retrieve relevant documents for the question"""
    try:
        rag_system = state['rag_system']
        question = state['question']
        
        # Get relevant documents
        docs = rag_system.retriever.get_relevant_documents(question)
        
        state['source_documents'] = docs
        return state
        
    except Exception as e:
        state['error'] = f"Error retrieving documents: {e}"
        return state

def generate_answer(state: RAGState) -> RAGState:
    """Generate answer using the LLM"""
    try:
        rag_system = state['rag_system']
        question = state['question']
        docs = state.get('source_documents', [])
        
        # Create context from documents
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Generate answer
        prompt = f"""Use the following context to answer the question. If you don't know the answer, say so.

Context: {context}

Question: {question}

Answer:"""
        
        answer = rag_system.llm.invoke(prompt)
        state['answer'] = answer
        
        return state
        
    except Exception as e:
        state['error'] = f"Error generating answer: {e}"
        return state

def create_rag_graph(rag_system: RAGSystem):
    """Create the LangGraph workflow for RAG"""
    
    # Create the graph
    workflow = StateGraph(RAGState)
    
    # Add nodes
    workflow.add_node("retrieve", retrieve_documents)
    workflow.add_node("generate", generate_answer)
    
    # Add edges
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    # Compile the graph
    return workflow.compile()

def query_with_langgraph(rag_system: RAGSystem, question: str) -> Dict[str, Any]:
    """Query using LangGraph workflow"""
    try:
        # Create graph
        graph = create_rag_graph(rag_system)
        
        # Initialize state
        initial_state = {
            'question': question,
            'answer': '',
            'source_documents': [],
            'error': '',
            'rag_system': rag_system
        }
        
        # Run the graph
        result = graph.invoke(initial_state)
        
        return {
            'answer': result['answer'],
            'source_documents': result['source_documents'],
            'error': result.get('error', '')
        }
        
    except Exception as e:
        return {
            'answer': '',
            'source_documents': [],
            'error': str(e)
        }

if __name__ == "__main__":
    # Example usage
    urls = [
        "https://python.langchain.com/docs/tutorials/rag/",
        "https://lilianweng.github.io/posts/2023-06-23-agent/"
    ]
    
    # Initialize RAG system
    rag = RAGSystem()
    
    # Build RAG from URLs
    rag.build_rag_from_urls(urls)
    
    # Test query
    question = "What is RAG and how does it work?"
    result = rag.query(question)
    
    print(f"Question: {question}")
    print(f"Answer: {result['answer']}")
    print(f"Query time: {result['query_time']:.2f}s")
