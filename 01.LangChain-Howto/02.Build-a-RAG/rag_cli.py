"""
CLI tool for the RAG system

This module provides a command-line interface for the RAG system,
allowing users to build RAG systems from URLs and query them interactively.

Author: AI Assistant
Date: 2024
"""

import os
import sys
import json
import click
from typing import List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

from rag_system import RAGSystem

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """RAG System CLI - Build and query RAG systems using LangGraph and Ollama
    
    Examples:
        # Build a RAG system from URLs
        python rag_cli.py build -u "https://example.com" -u "https://another.com"
        
        # Query with a single question
        python rag_cli.py query -q "What is RAG?"
        
        # Start interactive mode
        python rag_cli.py query -i
        
        # Check system status
        python rag_cli.py status
        
        # List available models
        python rag_cli.py list-models
    """
    pass

@cli.command()
@click.option('--urls', '-u', multiple=True, help='URLs to fetch and process')
@click.option('--urls-file', '-f', type=click.Path(exists=True), help='File containing URLs (one per line)')
@click.option('--model', '-m', default=None, help='Ollama model to use')
@click.option('--output', '-o', default='rag_system.json', help='Output file for system info')
def build(urls: tuple, urls_file: str, model: str, output: str):
    """Build a RAG system from URLs"""
    
    # Collect URLs
    all_urls = list(urls)
    
    if urls_file:
        with open(urls_file, 'r') as f:
            file_urls = [line.strip() for line in f if line.strip()]
            all_urls.extend(file_urls)
    
    if not all_urls:
        console.print("[red]Error: No URLs provided. Use --urls or --urls-file option.[/red]")
        sys.exit(1)
    
    console.print(f"[green]Building RAG system from {len(all_urls)} URLs...[/green]")
    
    try:
        # Initialize RAG system
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Initializing RAG system...", total=None)
            
            rag = RAGSystem(model_name=model)
            progress.update(task, description="Building RAG system from URLs...")
            
            # Build RAG system
            rag.build_rag_from_urls(all_urls)
            
            progress.update(task, description="Saving system info...")
        
        # Save system info
        system_info = {
            'model': rag.model_name,
            'urls': all_urls,
            'vectorstore_path': './chroma_db',
            'embedding_model': os.getenv('EMBEDDING_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        }
        
        with open(output, 'w') as f:
            json.dump(system_info, f, indent=2)
        
        console.print(f"[green]✓ RAG system built successfully![/green]")
        console.print(f"[blue]System info saved to: {output}[/blue]")
        
        # Display system info
        table = Table(title="RAG System Information")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Model", rag.model_name)
        table.add_row("URLs", str(len(all_urls)))
        table.add_row("Vector Store", "./chroma_db")
        table.add_row("Embedding Model", system_info['embedding_model'])
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error building RAG system: {e}[/red]")
        sys.exit(1)

@cli.command()
@click.option('--question', '-q', help='Question to ask (use -i for interactive mode)')
@click.option('--model', '-m', default=None, help='Ollama model to use')
@click.option('--system-info', '-s', default='rag_system.json', help='System info file')
@click.option('--interactive', '-i', is_flag=True, help='Run in interactive mode')
def query(question: str, model: str, system_info: str, interactive: bool):
    """Query the RAG system"""
    
    # Handle case where no question is provided and not in interactive mode
    if not question and not interactive:
        console.print("[red]Error: No question provided.[/red]")
        console.print("\nUsage examples:")
        console.print("  python rag_cli.py query -q 'What is RAG?'")
        console.print("  python rag_cli.py query -i")
        console.print("  python rag_cli.py query --help")
        sys.exit(1)
    
    try:
        # Load system info
        if os.path.exists(system_info):
            with open(system_info, 'r') as f:
                info = json.load(f)
            console.print(f"[blue]Loaded RAG system info from: {system_info}[/blue]")
        else:
            console.print(f"[yellow]Warning: System info file not found: {system_info}[/yellow]")
            info = {}
        
        # Initialize RAG system
        rag = RAGSystem(model_name=model or info.get('model'))
        
        # Check if vector store exists
        if not os.path.exists('./chroma_db'):
            console.print("[red]Error: Vector store not found. Please build the RAG system first.[/red]")
            sys.exit(1)
        
        # Load existing vector store
        from langchain_community.vectorstores import Chroma
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        embeddings = HuggingFaceEmbeddings(
            model_name=info.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')
        )
        
        vectorstore = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )
        
        rag.vectorstore = vectorstore
        rag.setup_retrieval_qa(vectorstore)
        
        if interactive:
            console.print("[green]Interactive mode started. Type 'quit' to exit.[/green]")
            
            while True:
                try:
                    # Get question from user
                    user_question = input("\n[blue]Question: [/blue]").strip()
                    
                    if user_question.lower() in ['quit', 'exit', 'q']:
                        console.print("[green]Goodbye![/green]")
                        break
                    
                    if not user_question:
                        continue
                    
                    # Process question
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        console=console
                    ) as progress:
                        task = progress.add_task("Processing question...", total=None)
                        result = rag.query(user_question)
                    
                    # Display result
                    display_result(user_question, result)
                    
                except KeyboardInterrupt:
                    console.print("\n[green]Goodbye![/green]")
                    break
                except Exception as e:
                    console.print(f"[red]Error: {e}[/red]")
        else:
            # Single query mode
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Processing question...", total=None)
                result = rag.query(question)
            
            display_result(question, result)
    
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

def display_result(question: str, result: dict):
    """Display query result in a formatted way"""
    
    # Create answer panel
    answer_panel = Panel(
        result['answer'],
        title="[bold green]Answer[/bold green]",
        border_style="green"
    )
    console.print(answer_panel)
    
    # Create metrics panel
    metrics_panel = Panel(
        f"Query Time: {result['query_time']:.2f}s\n"
        f"Source Documents: {len(result['source_documents'])}",
        title="[bold blue]Metrics[/bold blue]",
        border_style="blue"
    )
    console.print(metrics_panel)
    
    # Display source documents
    if result['source_documents']:
        console.print("\n[bold yellow]Source Documents:[/bold yellow]")
        
        for i, doc in enumerate(result['source_documents'], 1):
            source_panel = Panel(
                f"[bold]Source {i}:[/bold] {doc.metadata.get('source', 'Unknown')}\n"
                f"[bold]Content:[/bold] {doc.page_content[:200]}...",
                title=f"[bold cyan]Document {i}[/bold cyan]",
                border_style="cyan"
            )
            console.print(source_panel)

@cli.command()
@click.option('--model', '-m', default=None, help='Ollama model to use')
def test(model: str):
    """Test the RAG system with sample URLs and questions"""
    
    console.print("[green]Running RAG system test...[/green]")
    
    # Sample URLs
    urls = [
        "https://python.langchain.com/docs/tutorials/rag/",
        "https://lilianweng.github.io/posts/2023-06-23-agent/"
    ]
    
    # Sample questions
    questions = [
        "What is RAG and how does it work?",
        "What are the key components of a RAG system?",
        "How do agents work in AI systems?",
        "What is the difference between RAG and traditional search?"
    ]
    
    try:
        # Initialize and build RAG system
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Building test RAG system...", total=None)
            
            rag = RAGSystem(model_name=model)
            rag.build_rag_from_urls(urls)
            
            progress.update(task, description="Testing with sample questions...")
        
        # Test questions
        results = []
        for question in questions:
            result = rag.query(question)
            results.append((question, result))
        
        # Display results
        console.print("\n[bold green]Test Results:[/bold green]")
        
        for i, (question, result) in enumerate(results, 1):
            console.print(f"\n[bold cyan]Test {i}:[/bold cyan]")
            display_result(question, result)
        
        console.print("\n[green]✓ All tests completed successfully![/green]")
        
    except Exception as e:
        console.print(f"[red]Error during testing: {e}[/red]")
        sys.exit(1)

@cli.command()
def list_models():
    """List available Ollama models"""
    
    try:
        import subprocess
        
        console.print("[green]Fetching available Ollama models...[/green]")
        
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[bold green]Available Models:[/bold green]")
            console.print(result.stdout)
        else:
            console.print("[red]Error: Could not fetch Ollama models[/red]")
            console.print(f"Error: {result.stderr}")
            
    except FileNotFoundError:
        console.print("[red]Error: Ollama not found. Please install Ollama first.[/red]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

@cli.command()
def status():
    """Check the status of the RAG system"""
    
    console.print("[green]Checking RAG system status...[/green]")
    
    # Check system info
    if os.path.exists('rag_system.json'):
        with open('rag_system.json', 'r') as f:
            info = json.load(f)
        
        console.print("[bold green]System Info:[/bold green]")
        table = Table()
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        for key, value in info.items():
            table.add_row(key, str(value))
        
        console.print(table)
    else:
        console.print("[yellow]No system info file found.[/yellow]")
    
    # Check vector store
    if os.path.exists('./chroma_db'):
        console.print("[green]✓ Vector store exists[/green]")
    else:
        console.print("[red]✗ Vector store not found[/red]")
    
    # Check Ollama
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[green]✓ Ollama is running[/green]")
        else:
            console.print("[red]✗ Ollama is not running[/red]")
    except FileNotFoundError:
        console.print("[red]✗ Ollama not installed[/red]")

if __name__ == "__main__":
    cli()
