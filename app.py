import streamlit as st
import ollama
from duckduckgo_search import DDGS
from datetime import datetime
import re
from typing import List, Dict
import time

class StreamlitChatbot:
    def __init__(self):
        self.ddgs = DDGS()
        # Initialize session state for chat history if it doesn't exist
        if 'history' not in st.session_state:
            st.session_state.history = []
        
        # Initialize callback for input handling
        if 'submit' not in st.session_state:
            st.session_state.submit = False

    def extract_date_from_content(self, text: str) -> str:
        """Extract dates from content to help with temporal analysis"""
        year_pattern = r'\b20[12]\d\b'  # Years between 2010-2029
        years = re.findall(year_pattern, text)
        return years[-1] if years else None

    def analyze_content(self, search_results: List[Dict], query: str) -> Dict:
        """Analyze search results to extract relevant information"""
        combined_content = " ".join([result['body'] for result in search_results])
        latest_year = self.extract_date_from_content(combined_content)
        
        return {
            'current_year': datetime.now().year,
            'content_year': latest_year,
            'raw_content': combined_content,
            'query': query
        }

    def create_time_aware_prompt(self, analysis: Dict) -> str:
        """Create a prompt that considers temporal context"""
        current_year = analysis['current_year']
        
        return f"""
        Based on the following information from {current_year}:
        
        {analysis['raw_content']}
        
        Please provide a factual response about "{analysis['query']}" that:
        1. Is accurate to the current year ({current_year})
        2. Explicitly mentions relevant dates and timeframes
        3. Synthesizes information from multiple sources
        4. Provides context when discussing time-sensitive information
        
        Format the response as a clear, direct statement.
        """

    def search_internet(self, query: str) -> List[Dict]:
        """Perform internet search using DuckDuckGo"""
        try:
            with st.spinner('Searching the web...'):
                results = self.ddgs.text(query, max_results=5)
                return [result for result in results if 'body' in result]
        except Exception as e:
            st.error(f"Error searching internet: {e}")
            return []

    def get_search_response(self, query: str) -> str:
        """Generate a response based on search results and AI processing"""
        search_results = self.search_internet(query)
        
        if not search_results:
            return "No search results found."
        
        analysis = self.analyze_content(search_results, query)
        prompt = self.create_time_aware_prompt(analysis)

        try:
            with st.spinner('Generating response...'):
                response = ollama.chat(
                    model='llama3.2',
                    messages=[
                        {
                            'role': 'system',
                            'content': f'You are an AI assistant in {analysis["current_year"]}. Provide accurate, time-aware responses based on the provided information.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                )
                
                ai_response = response['message']['content']
                
                if str(analysis['current_year']) not in ai_response:
                    ai_response = f"As of {analysis['current_year']}, " + ai_response
                    
                return ai_response
                
        except Exception as e:
            return f"Sorry, there was an error generating a response: {e}"

    def get_direct_response(self, query: str) -> str:
        """Generate a direct response using LLM without web search"""
        try:
            with st.spinner('Thinking...'):
                response = ollama.chat(
                    model='llama3.2',
                    messages=[
                        {
                            'role': 'system',
                            'content': 'You are a helpful AI assistant. Provide direct and engaging responses.'
                        },
                        {
                            'role': 'user',
                            'content': query
                        }
                    ]
                )
                return response['message']['content']
        except Exception as e:
            return f"Sorry, there was an error generating a response: {e}"

    def display_chat_history(self):
        """Display chat history in Streamlit with most recent messages on top"""
        chat_container = st.container()
        with chat_container:
            # Reverse the chat history to show the most recent messages first
            for message in reversed(st.session_state.history):
                if message['role'] == 'user':
                    st.markdown(f"<div style='text-align: left;'><b>You:</b> {message['content']}</div>", unsafe_allow_html=True)
                else:
                    # AI response is right-aligned but text is left-aligned
                    st.markdown(f"<div style='text-align: right;'><b>AI:</b> <div style='text-align: left; display: inline-block;'>{message['content']}</div></div>", unsafe_allow_html=True)
                st.divider()

    def submit_callback(self):
        """Callback function for form submission"""
        st.session_state.submit = True

    def animate_text(self, text: str, speed: float = 0.05):
        """Animate text generation"""
        placeholder = st.empty()
        for i in range(len(text) + 1):
            placeholder.markdown(f"<div style='text-align: right;'><b>AI:</b> <div style='text-align: left; display: inline-block;'>{text[:i]}</div></div>", unsafe_allow_html=True)
            time.sleep(speed)

    def run(self):
        """Run the Streamlit chatbot interface"""
        st.title("AI Research Assistant")
        
        # Add a toggle for web search
        enable_search = st.toggle("Enable web search", value=False)
        
        # Create a form for input
        with st.form(key='message_form', clear_on_submit=True):
            user_input = st.text_input("You:", key='message')
            submit_button = st.form_submit_button("Send", on_click=self.submit_callback)

        # Handle form submission
        if st.session_state.submit and user_input:
            if enable_search:
                response = self.get_search_response(user_input)
            else:
                response = self.get_direct_response(user_input)
            
            # Add to history
            st.session_state.history.append({'role': 'user', 'content': user_input})
            st.session_state.history.append({'role': 'assistant', 'content': response})
            
            # Reset submit flag
            st.session_state.submit = False
            st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.history = []
            st.rerun()
        
        # Display chat history
        self.display_chat_history()

if __name__ == "__main__":
    chatbot = StreamlitChatbot()
    chatbot.run()