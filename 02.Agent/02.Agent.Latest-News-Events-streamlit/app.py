import streamlit as st
import sys
import platform
from pathlib import Path
import os

# Add parent directory to path to import from the notebook environment
sys.path.append(str(Path(__file__).parent.parent))

# Setup environment
from dotenv import load_dotenv
load_dotenv(Path("/Users/vuhung/Desktop/LangGraph-Adventures/02.Agent/.env.local"))

# Import the agent components
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# Import configuration
from config import NEWS_CATEGORIES, APP_CONFIG, AGENT_CONFIG, STYLE_CONFIG

# Page configuration
st.set_page_config(
    page_title=APP_CONFIG["page_title"],
    page_icon=APP_CONFIG["page_icon"],
    layout=APP_CONFIG["layout"],
    initial_sidebar_state=APP_CONFIG["initial_sidebar_state"]
)

# Custom CSS for better styling (dark theme)
st.markdown("""
<style>
    /* Dark theme base */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0e1117 !important;
        color: #e6e6e6 !important;
    }
    [data-testid="stSidebar"] {
        background: #0c0f14 !important;
        color: #e6e6e6 !important;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #e6f0ff;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .news-card {
        background-color: #1a2030;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #4ea1ff;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.35);
        transition: transform 0.2s ease-in-out;
        color: #e6e6e6;
    }
    /* Force high-contrast text inside the news card even in dark theme */
    .news-card * {
        color: #e6e6e6 !important;
    }
    .news-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(0,0,0,0.45);
    }
    .news-title {
        font-size: 1.4rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4ea1ff;
        padding-bottom: 0.5rem;
    }
    .news-summary {
        background-color: #111726;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2ecc71;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.35);
        color: #e6e6e6;
    }
    .news-content {
        color: #e6e6e6;
        line-height: 1.8;
        font-size: 1.1rem;
    }
    .sources-section {
        background-color: #111726;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1.5rem;
        border-top: 3px solid #ff6b6b;
        color: #e6e6e6;
    }
    .source-link {
        color: #66b3ff;
        text-decoration: none;
        font-size: 0.95rem;
        display: block;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
        transition: background-color 0.2s ease;
    }
    .source-link:hover {
        background-color: rgba(102,179,255,0.12);
        text-decoration: none;
        color: #99ccff;
    }
    /* Ensure markdown headings and paragraphs inside cards are dark */
    .news-card h1, .news-card h2, .news-card h3, .news-card h4, .news-card h5, .news-card h6, .news-card p, .news-card li {
        color: #e6e6e6 !important;
    }
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    .sidebar-section {
        background: linear-gradient(135deg, #0c0f14 0%, #121723 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .category-header {
        font-size: 1.3rem;
        font-weight: bold;
        color: #e6f0ff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .timestamp {
        color: #aab1bc;
        font-size: 0.9rem;
        font-style: italic;
        text-align: right;
        margin-top: 1rem;
    }
    .highlight-box {
        background: linear-gradient(135deg, #3a2d00 0%, #4a3800 100%);
        border: 1px solid #ffb300;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_agent():
    """Initialize the news agent with caching"""
    try:
        # LLM
        llm = ChatGoogleGenerativeAI(
            model=AGENT_CONFIG["model"], 
            temperature=AGENT_CONFIG["temperature"]
        )
        
        # Tools
        search = TavilySearchResults(max_results=AGENT_CONFIG["max_results"])
        
        # Agent
        agent = create_react_agent(llm, tools=[search])
        
        return agent
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        return None

def get_news_content(agent, prompt):
    """Get news content from the agent"""
    try:
        response = agent.invoke({
            "messages": [
                ("user", prompt)
            ]
        })
        last = response["messages"][-1]
        content = getattr(last, "content", last)
        return format_news_content(content)
    except Exception as e:
        return f"""
## ❌ Error Loading News

<div class="highlight-box">
**Error Details:** {str(e)}

**Troubleshooting Tips:**
- Check your internet connection
- Verify API keys are properly configured
- Try refreshing the page
- Contact support if the issue persists
</div>
"""

def format_news_content(content):
    """Format news content into structured markdown"""
    import re
    from datetime import datetime
    
    # Split content into sections
    lines = content.split('\n')
    formatted_sections = []
    
    # Extract summary and sources
    summary = ""
    sources = []
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a source line (contains URL)
        if 'http' in line and ('[' in line or 'https://' in line):
            sources.append(line)
        elif 'Summary:' in line or 'summary:' in line:
            current_section = "summary"
        elif 'Sources:' in line or 'sources:' in line:
            current_section = "sources"
        elif current_section == "summary":
            summary += line + " "
        elif current_section == "sources":
            if 'http' in line:
                sources.append(line)
    
    # If no structured format found, treat the whole content as summary
    if not summary:
        summary = content
    
    # Format as markdown
    markdown_content = f"""
## 📰 Latest News Summary

<div class="news-summary">
{summary.strip()}
</div>

## 🔗 Sources

<div class="sources-section">
"""
    
    # Format sources
    for i, source in enumerate(sources, 1):
        # Extract URL and title if available
        if '[' in source and '](' in source:
            # Already in markdown format
            markdown_content += f"\n{i}. {source}\n"
        elif 'http' in source:
            # Convert to markdown link
            url = re.search(r'https?://[^\s]+', source)
            if url:
                url = url.group(0)
                title = source.replace(url, '').strip()
                if not title:
                    title = url
                markdown_content += f"\n{i}. [{title}]({url})\n"
            else:
                markdown_content += f"\n{i}. {source}\n"
        else:
            markdown_content += f"\n{i}. {source}\n"
    
    markdown_content += f"""
</div>

<div class="timestamp">
📅 Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
</div>
"""
    
    return markdown_content

def main():
    # Header
    st.markdown('<h1 class="main-header">📰 Your Personalized News Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar with enhanced styling
    st.sidebar.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.sidebar.markdown("## 🎯 News Categories")
    
    # Use news categories from configuration
    news_categories = NEWS_CATEGORIES
    
    # Sidebar selection
    selected_category = st.sidebar.selectbox(
        "Choose a news category:",
        list(news_categories.keys()),
        index=0
    )
    
    # Display category description
    st.sidebar.markdown(f"**{news_categories[selected_category]['description']}**")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Initialize agent
    with st.spinner("Initializing news agent..."):
        agent = initialize_agent()
    
    if agent is None:
        st.error("Failed to initialize the news agent. Please check your environment setup.")
        return
    
    # Main content area with enhanced styling
    st.markdown(f'<div class="category-header">🌍 {selected_category}</div>', unsafe_allow_html=True)
    
    # Add a refresh button
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Refresh News", type="primary"):
            st.rerun()
    
    with col2:
        st.markdown("*Click refresh to get the latest news*")
    
    # Get and display news with enhanced loading state
    with st.spinner(f"🔍 Fetching latest {selected_category.lower()} news..."):
        news_content = get_news_content(agent, news_categories[selected_category]["prompt"])
    
    # Display news content using streamlit.markdown() with custom styling
    st.markdown(f"""<div class="news-card">
{news_content}
</div>""", unsafe_allow_html=True)
    
    # Success message
    st.success("✅ News content loaded successfully!")
    
    # Footer with enhanced styling
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius: 10px; margin-top: 2rem;">
        📰 Powered by LangGraph Agent | 🔍 Real-time news from multiple sources | ⚡ AI-Powered Content Curation
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
