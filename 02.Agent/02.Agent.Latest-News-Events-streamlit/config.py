# Configuration file for the News Dashboard Streamlit App

# News categories with their prompts and descriptions
NEWS_CATEGORIES = {
    "🤖 LLM/AI News": {
        "prompt": "What are the top five news headlines today regarding advancements in LLM/AI? Cite the sources with links.",
        "description": "Latest developments in AI and Large Language Models",
        "icon": "🤖"
    },
    "🌍 Russia-Ukraine Conflict": {
        "prompt": "Summarize the latest developments in the conflict between Russia and Ukraine in the past 24 hours. Cite the sources with links.",
        "description": "Recent updates on the ongoing conflict",
        "icon": "🌍"
    },
    "🌊 Vietnam Flood Status": {
        "prompt": "What is the current status of the flood in Vietnam, according to recent reports? Cite the sources with links.",
        "description": "Current situation of flooding in Vietnam",
        "icon": "🌊"
    },
    "♟️ Magnus Carlsen Chess": {
        "prompt": "Tell me about the recent games of Magnus Carlsen and provide the key highlights. Cite the sources with links.",
        "description": "Recent chess games and achievements",
        "icon": "♟️"
    },
    "📊 Data Mining Case Studies": {
        "prompt": "Research and list 5 recent case studies where data mining improved outcomes or efficiency. Prefer the newest cases. Include brief impact metrics and cite sources with links.",
        "description": "Recent data mining success stories",
        "icon": "📊"
    },
    "🇦🇺 ABC Australia News": {
        "prompt": "Search for the latest 5 news headlines from ABC Australia (abc.net.au). For each headline, provide: a) the title, b) a brief summary (under 50 words). Make sure to search specifically for 'ABC Australia news' or 'abc.net.au latest news' to get the Australian ABC, not the US ABC.",
        "description": "Latest news from ABC Australia",
        "icon": "🇦🇺"
    }
}

# App configuration
APP_CONFIG = {
    "page_title": "News Reader - Your Personalized News Dashboard",
    "page_icon": "📰",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Agent configuration
AGENT_CONFIG = {
    "model": "gemini-2.5-flash",
    "temperature": 0.2,
    "max_results": 3
}

# Styling configuration
STYLE_CONFIG = {
    "primary_color": "#1f77b4",
    "secondary_color": "#2c3e50",
    "background_color": "#f8f9fa",
    "text_color": "#34495e"
}
