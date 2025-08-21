#!/usr/bin/env python3
"""
URL Helper Script

This script helps validate and fix common URL issues for the RAG system.
"""

import re
from urllib.parse import urlparse

def fix_common_url_issues(url: str) -> str:
    """
    Fix common URL issues and typos
    
    Args:
        url: URL to fix
        
    Returns:
        Fixed URL
    """
    original_url = url
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Parse URL
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    
    # Common fixes
    fixes = [
        ('github.ioposts', 'github.io/posts'),
        ('github.iopost', 'github.io/posts'),
        ('github.io/posts/posts', 'github.io/posts'),
        ('www.github.io', 'github.io'),
        ('docs.python.org/docs', 'docs.python.org'),
    ]
    
    for old, new in fixes:
        if old in domain:
            domain = domain.replace(old, new)
            url = f"{parsed.scheme}://{domain}{parsed.path}"
            print(f"🔧 Fixed URL: {original_url} → {url}")
            break
    
    return url

def validate_url(url: str) -> bool:
    """
    Basic URL validation
    
    Args:
        url: URL to validate
        
    Returns:
        True if URL is valid, False otherwise
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.netloc and parsed.scheme)
    except:
        return False

def main():
    """Main function"""
    print("🔗 URL Helper for RAG System")
    print("=" * 40)
    
    # Example URLs with common issues
    test_urls = [
        "lilianweng.github.ioposts/2023-06-23-agent/",
        "https://lilianweng.github.ioposts/2023-06-23-agent/",
        "python.langchain.com/docs/tutorials/rag/",
        "https://docs.python.org/docs/tutorials/rag/",
    ]
    
    print("\n📝 Common URL fixes:")
    for url in test_urls:
        fixed = fix_common_url_issues(url)
        valid = validate_url(fixed)
        status = "✅" if valid else "❌"
        print(f"  {status} {url}")
        if url != fixed:
            print(f"     → {fixed}")
    
    print("\n💡 Usage:")
    print("  python rag_cli.py build -u 'https://lilianweng.github.io/posts/2023-06-23-agent/'")
    print("  python rag_cli.py build -u 'https://python.langchain.com/docs/tutorials/rag/'")
    
    print("\n⚠️  Common issues to avoid:")
    print("  - Missing 'https://' protocol")
    print("  - Typos in domain names (e.g., 'github.ioposts' → 'github.io/posts')")
    print("  - Duplicate path segments")

if __name__ == "__main__":
    main()
