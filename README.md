# AI Research Assistant

A Streamlit-based chatbot that leverages Ollama for LLM capabilities and DuckDuckGo for real-time web search integration.

## Features

- **Dual Operation Modes**: 
  - Direct LLM responses using Ollama's llama3.2 model
  - Web-augmented responses with DuckDuckGo search integration

## Prerequisites

- Python 3.7+
- Streamlit
- Ollama with llama3.2 model installed
- duckduckgo-search package

## Web App

![Screenshot 2025-02-25 002813](https://github.com/user-attachments/assets/54c7b21a-ae19-47ba-b3b2-0be853c8230e)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-research-assistant.git
   cd ai-research-assistant
   ```

2. Install required packages:
   ```
   pip install streamlit ollama duckduckgo-search
   ```

3. Ensure Ollama is installed and the llama3.2 model is available:
   ```
   ollama pull llama3.2
   ```

## Usage

1. Start the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your browser and navigate to the displayed URL (typically http://localhost:8501)

3. Toggle "Enable web search" to switch between direct LLM responses and web-augmented answers

4. Enter your query in the text box and click "Send"

[Your License Here]

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
