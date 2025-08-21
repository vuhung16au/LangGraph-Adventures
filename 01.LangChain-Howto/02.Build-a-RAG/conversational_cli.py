#!/usr/bin/env python3
"""
Conversational RAG System CLI
=============================

Command-line interface for the conversational RAG system with chat history support.
"""

import os
import sys
import json
import click
from datetime import datetime
from typing import List, Optional

# Rich for beautiful output
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.syntax import Syntax

# Import our conversational RAG system
from conversational_rag import ConversationalRAGSystem

console = Console()

def load_system_info(filepath: str = "conversational_rag_system.json") -> dict:
    """Load system information from file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        console.print(f"[red]Error loading system info: {e}[/red]")
        return {}

def display_system_info(info: dict):
    """Display system information in a table"""
    table = Table(title="Conversational RAG System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    for key, value in info.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value[:3]) + ("..." if len(value) > 3 else "")
        table.add_row(key, str(value))
    
    console.print(table)

def display_conversation_history(messages: List, max_messages: int = 10):
    """Display conversation history"""
    if not messages:
        console.print("[yellow]No conversation history[/yellow]")
        return
    
    # Show only the last N messages
    recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
    
    for i, message in enumerate(recent_messages):
        role_emoji = "👤" if message.role == "user" else "🤖"
        role_color = "blue" if message.role == "user" else "green"
        
        # Format timestamp
        timestamp = message.timestamp.strftime("%H:%M:%S")
        
        # Truncate long messages
        content = message.content
        if len(content) > 200:
            content = content[:200] + "..."
        
        console.print(f"[{role_color}]{role_emoji} {timestamp}[/{role_color}] {content}")
    
    if len(messages) > max_messages:
        console.print(f"[dim]... and {len(messages) - max_messages} more messages[/dim]")

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Conversational RAG System CLI - Chat with your documents using conversation history
    
    Examples:
        # Build a conversational RAG system from URLs
        python conversational_cli.py build -u "https://example.com" -u "https://another.com"
        
        # Start a new chat session
        python conversational_cli.py chat
        
        # Continue a specific session
        python conversational_cli.py chat -s "session_123"
        
        # List all sessions
        python conversational_cli.py sessions
        
        # Check system status
        python conversational_cli.py status
    """
    pass

@cli.command()
@click.option('--urls', '-u', multiple=True, help='URLs to fetch content from')
@click.option('--file', '-f', help='File containing URLs (one per line)')
@click.option('--model', '-m', default=None, help='Ollama model to use')
@click.option('--output', '-o', default='conversational_rag_system.json', help='Output file for system info')
@click.option('--chunk-size', default=1000, help='Document chunk size')
@click.option('--chunk-overlap', default=200, help='Document chunk overlap')
def build(urls: tuple, file: str, model: str, output: str, chunk_size: int, chunk_overlap: int):
    """Build a conversational RAG system from URLs"""
    
    if not urls and not file:
        console.print("[red]Error: No URLs provided. Use -u or -f option.[/red]")
        sys.exit(1)
    
    # Collect URLs
    url_list = list(urls)
    if file:
        try:
            with open(file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
                url_list.extend(file_urls)
        except Exception as e:
            console.print(f"[red]Error reading URL file: {e}[/red]")
            sys.exit(1)
    
    if not url_list:
        console.print("[red]Error: No valid URLs found[/red]")
        sys.exit(1)
    
    console.print(f"[blue]Building conversational RAG system from {len(url_list)} URLs...[/blue]")
    
    try:
        # Initialize system
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Initializing conversational RAG system...", total=None)
            
            # Create system with custom parameters
            system = ConversationalRAGSystem(
                model_name=model or "llama3.1:8b-instruct-q8_0",
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            
            progress.update(task, description="Building RAG system from URLs...")
            
            # Build the system
            system_info = system.build_rag_from_urls(url_list, output)
            
            progress.update(task, description="Saving system info...")
        
        console.print(f"[green]✓ Conversational RAG system built successfully![/green]")
        console.print(f"System info saved to: {output}")
        
        # Display system information
        display_system_info(system_info)
        
    except Exception as e:
        console.print(f"[red]Error building conversational RAG system: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--session', '-s', help='Session ID to use (auto-created if not provided)')
@click.option('--system-info', default='conversational_rag_system.json', help='System info file')
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
@click.option('--show-history', is_flag=True, help='Show conversation history at start')
def chat(session: str, system_info: str, sessions_file: str, show_history: bool):
    """Start an interactive chat session"""
    
    try:
        # Load system info
        info = load_system_info(system_info)
        if not info:
            console.print("[red]Error: No system info found. Run 'build' command first.[/red]")
            sys.exit(1)
        
        # Initialize system
        console.print("[blue]Initializing conversational RAG system...[/blue]")
        system = ConversationalRAGSystem(
            model_name=info.get('model', 'llama3.1:8b-instruct-q8_0'),
            vector_store_path=info.get('vector_store_path', './conversational_chroma_db')
        )
        
        # Load existing sessions if available
        if os.path.exists(sessions_file):
            system.load_sessions(sessions_file)
            console.print(f"[green]Loaded existing sessions from {sessions_file}[/green]")
        
        # Create or get session
        if session:
            if session not in system.sessions:
                system.create_session(session)
                console.print(f"[green]Created new session: {session}[/green]")
            else:
                console.print(f"[green]Using existing session: {session}[/green]")
        else:
            session = system.create_session()
            console.print(f"[green]Created new session: {session}[/green]")
        
        # Show conversation history if requested
        if show_history:
            messages = system.get_conversation_history(session)
            if messages:
                console.print("\n[blue]Conversation History:[/blue]")
                display_conversation_history(messages)
        
        console.print("\n[green]Interactive chat mode started. Type 'quit' to exit.[/green]")
        console.print("[dim]Commands: 'history', 'sessions', 'save', 'help'[/dim]\n")
        
        while True:
            try:
                # Get user input
                question = console.input("[blue]Question: [/blue]").strip()
                
                if not question:
                    continue
                
                # Handle commands
                if question.lower() in ['quit', 'exit', 'q']:
                    break
                elif question.lower() == 'history':
                    messages = system.get_conversation_history(session)
                    display_conversation_history(messages)
                    continue
                elif question.lower() == 'sessions':
                    sessions = system.list_sessions()
                    console.print(f"[blue]Available sessions: {', '.join(sessions)}[/blue]")
                    continue
                elif question.lower() == 'save':
                    system.save_sessions(sessions_file)
                    console.print(f"[green]Sessions saved to {sessions_file}[/green]")
                    continue
                elif question.lower() == 'help':
                    console.print("[blue]Available commands:[/blue]")
                    console.print("  history  - Show conversation history")
                    console.print("  sessions - List all sessions")
                    console.print("  save     - Save sessions to file")
                    console.print("  help     - Show this help")
                    console.print("  quit     - Exit chat mode")
                    continue
                
                # Process the question
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Processing question...", total=None)
                    
                    response = system.query(question, session)
                    
                    progress.update(task, description="Generating response...")
                
                # Display answer
                console.print(f"\n[green]Answer:[/green] {response['answer']}")
                
                # Display metrics
                console.print(f"\n[dim]Query time: {response['query_time']:.2f}s[/dim]")
                console.print(f"[dim]Sources: {len(response['source_documents'])}[/dim]")
                console.print(f"[dim]Session: {response['session_id']}[/dim]")
                console.print(f"[dim]Messages in session: {response['message_count']}[/dim]\n")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Error processing question: {e}[/red]")
        
        # Save sessions before exiting
        system.save_sessions(sessions_file)
        console.print(f"\n[green]Sessions saved to {sessions_file}[/green]")
        console.print("[blue]Goodbye![/blue]")
        
    except Exception as e:
        console.print(f"[red]Error in chat mode: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--session', '-s', help='Session ID to query')
@click.option('--question', '-q', prompt='Enter your question', help='Question to ask')
@click.option('--system-info', default='conversational_rag_system.json', help='System info file')
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
def query(session: str, question: str, system_info: str, sessions_file: str):
    """Query the conversational RAG system with a single question"""
    
    try:
        # Load system info
        info = load_system_info(system_info)
        if not info:
            console.print("[red]Error: No system info found. Run 'build' command first.[/red]")
            sys.exit(1)
        
        # Initialize system
        system = ConversationalRAGSystem(
            model_name=info.get('model', 'llama3.1:8b-instruct-q8_0'),
            vector_store_path=info.get('vector_store_path', './conversational_chroma_db')
        )
        
        # Load existing sessions if available
        if os.path.exists(sessions_file):
            system.load_sessions(sessions_file)
        
        # Create session if not provided
        if not session:
            session = system.create_session()
        
        # Process the question
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Processing question...", total=None)
            
            response = system.query(question, session)
            
            progress.update(task, description="Generating response...")
        
        # Display answer
        console.print(f"\n[green]Answer:[/green] {response['answer']}")
        
        # Display metrics
        console.print(f"\n[dim]Query time: {response['query_time']:.2f}s[/dim]")
        console.print(f"[dim]Sources: {len(response['source_documents'])}[/dim]")
        console.print(f"[dim]Session: {response['session_id']}[/dim]")
        console.print(f"[dim]Messages in session: {response['message_count']}[/dim]")
        
        # Save sessions
        system.save_sessions(sessions_file)
        
    except Exception as e:
        console.print(f"[red]Error processing query: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--system-info', default='conversational_rag_system.json', help='System info file')
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
def status(system_info: str, sessions_file: str):
    """Check the status of the conversational RAG system"""
    
    try:
        # Load system info
        info = load_system_info(system_info)
        
        if not info:
            console.print("[red]No system info found. Run 'build' command first.[/red]")
            sys.exit(1)
        
        # Initialize system to get current status
        system = ConversationalRAGSystem(
            model_name=info.get('model', 'llama3.1:8b-instruct-q8_0'),
            vector_store_path=info.get('vector_store_path', './conversational_chroma_db')
        )
        
        # Load sessions if available
        if os.path.exists(sessions_file):
            system.load_sessions(sessions_file)
        
        # Get current system info
        current_info = system.get_system_info()
        
        # Display status
        console.print("[blue]Conversational RAG System Status[/blue]")
        console.print("=" * 40)
        
        # System info
        console.print(f"[green]✓ System built successfully[/green]")
        console.print(f"Model: {current_info['model']}")
        console.print(f"Embedding model: {current_info['embedding_model']}")
        console.print(f"Vector store: {current_info['vector_store_path']}")
        console.print(f"Memory type: {current_info['memory_type']}")
        console.print(f"Retriever k: {current_info['retriever_k']}")
        
        # Session info
        console.print(f"\n[blue]Sessions:[/blue]")
        if current_info['sessions']:
            console.print(f"Active sessions: {len(current_info['sessions'])}")
            for session_id in current_info['sessions'][:5]:  # Show first 5
                session = system.get_session(session_id)
                if session:
                    msg_count = len(session.messages)
                    console.print(f"  {session_id}: {msg_count} messages")
            if len(current_info['sessions']) > 5:
                console.print(f"  ... and {len(current_info['sessions']) - 5} more")
        else:
            console.print("No active sessions")
        
        # File status
        console.print(f"\n[blue]Files:[/blue]")
        console.print(f"System info: {'✓' if os.path.exists(system_info) else '✗'} {system_info}")
        console.print(f"Sessions file: {'✓' if os.path.exists(sessions_file) else '✗'} {sessions_file}")
        console.print(f"Vector store: {'✓' if os.path.exists(current_info['vector_store_path']) else '✗'} {current_info['vector_store_path']}")
        
    except Exception as e:
        console.print(f"[red]Error checking status: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
def sessions(sessions_file: str):
    """List all conversation sessions"""
    
    try:
        if not os.path.exists(sessions_file):
            console.print("[yellow]No sessions file found[/yellow]")
            return
        
        # Load sessions
        with open(sessions_file, 'r') as f:
            sessions_data = json.load(f)
        
        if not sessions_data:
            console.print("[yellow]No sessions found[/yellow]")
            return
        
        # Display sessions
        table = Table(title="Conversation Sessions")
        table.add_column("Session ID", style="cyan")
        table.add_column("Messages", style="green")
        table.add_column("Created", style="yellow")
        table.add_column("Updated", style="yellow")
        
        for session_id, session_info in sessions_data.items():
            msg_count = len(session_info['messages'])
            created = session_info['created_at'][:19]  # Remove microseconds
            updated = session_info['updated_at'][:19]
            
            table.add_row(session_id, str(msg_count), created, updated)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing sessions: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--session', '-s', required=True, help='Session ID to delete')
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
def delete_session(session: str, sessions_file: str):
    """Delete a conversation session"""
    
    try:
        # Initialize system
        system = ConversationalRAGSystem()
        
        # Load existing sessions
        if os.path.exists(sessions_file):
            system.load_sessions(sessions_file)
        
        # Delete session
        if system.delete_session(session):
            # Save updated sessions
            system.save_sessions(sessions_file)
            console.print(f"[green]Deleted session: {session}[/green]")
        else:
            console.print(f"[red]Session not found: {session}[/red]")
            sys.exit(1)
        
    except Exception as e:
        console.print(f"[red]Error deleting session: {e}[/red]")
        sys.exit(1)

@cli.command()
def list_models():
    """List available Ollama models"""
    
    try:
        import subprocess
        
        # Run ollama list command
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[blue]Available Ollama Models:[/blue]")
            console.print(result.stdout)
        else:
            console.print("[red]Error running 'ollama list'[/red]")
            console.print(f"Error: {result.stderr}")
            sys.exit(1)
        
    except FileNotFoundError:
        console.print("[red]Ollama not found. Please install Ollama first.[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error listing models: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--system-info', default='conversational_rag_system.json', help='System info file')
@click.option('--sessions-file', default='conversational_sessions.json', help='Sessions file')
def test(system_info: str, sessions_file: str):
    """Test the conversational RAG system with sample questions"""
    
    try:
        # Load system info
        info = load_system_info(system_info)
        if not info:
            console.print("[red]Error: No system info found. Run 'build' command first.[/red]")
            sys.exit(1)
        
        # Initialize system
        console.print("[blue]Testing conversational RAG system...[/blue]")
        system = ConversationalRAGSystem(
            model_name=info.get('model', 'llama3.1:8b-instruct-q8_0'),
            vector_store_path=info.get('vector_store_path', './conversational_chroma_db')
        )
        
        # Load sessions if available
        if os.path.exists(sessions_file):
            system.load_sessions(sessions_file)
        
        # Create test session
        test_session = system.create_session("test_session")
        
        # Test questions
        test_questions = [
            "What is RAG?",
            "How does conversation history work?",
            "What are the main components of this system?"
        ]
        
        for i, question in enumerate(test_questions, 1):
            console.print(f"\n[blue]Test {i}: {question}[/blue]")
            
            try:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("Processing...", total=None)
                    response = system.query(question, test_session)
                
                console.print(f"[green]✓ Answer:[/green] {response['answer'][:200]}...")
                console.print(f"[dim]Time: {response['query_time']:.2f}s, Sources: {len(response['source_documents'])}[/dim]")
                
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/red]")
        
        # Clean up test session
        system.delete_session(test_session)
        system.save_sessions(sessions_file)
        
        console.print(f"\n[green]✓ Conversational RAG system test completed![/green]")
        
    except Exception as e:
        console.print(f"[red]Error testing system: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    cli()
