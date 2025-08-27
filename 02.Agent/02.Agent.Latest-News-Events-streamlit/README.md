# 📰 Personalized News Dashboard

A Streamlit application that provides an easy way to read news based on your specific interests using AI-powered news aggregation.

## 🎯 News Categories

The app includes the following news categories:

- **🤖 LLM/AI News**: Latest developments in AI and Large Language Models
- **🌍 Russia-Ukraine Conflict**: Recent updates on the ongoing conflict
- **🌊 Vietnam Flood Status**: Current situation of flooding in Vietnam
- **♟️ Magnus Carlsen Chess**: Latest chess games and achievements
- **📊 Data Mining Case Studies**: Recent data mining success stories
- **🇦🇺 ABC Australia News**: Latest news from ABC Australia

## 🚀 Setup Instructions

### Prerequisites

1. Make sure you have Python 3.8+ installed
2. Ensure you have the same virtual environment setup as the original notebook
3. Make sure your `.env.local` file is properly configured with API keys

### Installation

1. Navigate to the project directory:
   ```bash
   cd /Users/vuhung/Desktop/LangGraph-Adventures/02.Agent/02.Agent.Latest-News-Events-streamlit
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## 🎨 Features

- **Clean, Modern UI**: Beautiful interface with custom styling
- **Real-time News**: Get the latest news from multiple sources
- **Easy Navigation**: Sidebar with categorized news sections
- **Refresh Functionality**: Click refresh to get updated news
- **Source Attribution**: All news includes proper source links
- **Responsive Design**: Works well on different screen sizes

## 🔧 Configuration

The app uses the same environment setup as your notebook:
- Google Generative AI API key
- Tavily API key
- Other environment variables from `.env.local`

## 📱 Usage

1. **Select a Category**: Use the sidebar to choose your preferred news category
2. **Read News**: The selected category's latest news will be displayed
3. **Refresh**: Click the refresh button to get the most recent updates
4. **Explore Sources**: Click on source links to read full articles

## 🛠️ Technical Details

- **Framework**: Streamlit
- **AI Agent**: LangGraph with ReAct pattern
- **LLM**: Google Gemini 2.5 Flash
- **Search Tool**: Tavily Search API
- **Styling**: Custom CSS for enhanced user experience

## 🔄 Updates

The app automatically fetches fresh news each time you:
- Select a different category
- Click the refresh button
- Reload the page

## 📝 Notes

- News fetching may take a few seconds depending on the category
- All news content is sourced from reliable news outlets
- The app maintains the same agent setup as your notebook for consistency

## 🐛 Troubleshooting

If you encounter issues:

1. **Agent Initialization Error**: Check your API keys in `.env.local`
2. **Import Errors**: Ensure all dependencies are installed
3. **News Fetching Errors**: Check your internet connection and API limits

## 📄 License

This project is part of the LangGraph Adventures series.
