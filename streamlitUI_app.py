import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables and configure page
load_dotenv()
st.set_page_config(
    page_title="Social Media Expert",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .stMarkdown {
        font-size: 16px;
    }
    .warning-box {
        padding: 10px;
        background-color: red;
        border-left: 5px solid #ffeeba;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("⚠ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# Title and description
st.title("🚀 Social Media Expert")
st.markdown("""
<div class="warning-box">
⚠️ Note: I exclusively provide advice on social media topics. For other subjects, please consult a different expert.
</div>
""", unsafe_allow_html=True)

st.markdown("""
I can assist you with:
- Platform-specific strategies 📱
  - Instagram
  - Twitter/X
  - LinkedIn
  - TikTok
  - Facebook
  - YouTube
  - Pinterest
  - Snapchat
- Content creation and planning 📝
- Social media marketing campaigns 🎯
- Community management 🤝
- Analytics and metrics 📊
- Latest trends and features 🔥
""")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask your social media question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response with a loading spinner
    with st.chat_message("assistant"):
        with st.spinner("Analyzing your social media query..."):
            try:
                # Create system message and user query
                messages = [
                    {
                        "role": "system",
                        "content": """You are a specialized social media expert with STRICT guidelines:

                        ONLY respond to questions about:
                        1. Social Media Platforms (Instagram, Twitter/X, LinkedIn, TikTok, Facebook, YouTube, Pinterest, Snapchat)
                        2. Social Media Marketing (content strategy, posting, advertising)
                        3. Social Media Management (engagement, moderation, brand voice)
                        4. Social Media Analytics (metrics, tracking, ROI)
                        5. Social Media Tools (scheduling, analytics, content creation)
                        6. Social Media Trends (updates, features, best practices)

                        For ANY question not directly related to social media, respond ONLY with:
                        "I apologize, but I can only assist with social media-related questions. Your question appears to be about something else. 
                        Please ask me about social media marketing, strategy, platforms, or management instead."

                        Before providing any answer, verify that the question is genuinely about social media."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ] 
                
                # Get response from Groq
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                )
                
                response = chat_completion.choices[0].message.content
                st.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Sidebar with additional information
with st.sidebar:
    st.header("📱 Social Media Expertise")
    st.markdown("""
    ### Platforms Covered:
    - Instagram 📸
    - Twitter/X 🐦
    - LinkedIn 💼
    - TikTok 🎵
    - Facebook 👥
    - YouTube 🎥
    - Pinterest 📌
    - Snapchat 👻
    
    ### Topics Covered:
    - Platform Strategy
    - Content Creation
    - Engagement Tactics
    - Analytics & Metrics
    - Trend Analysis
    - Best Practices
    - Community Management
    - Brand Building
    """)
    
    st.markdown("""
    <div class="warning-box">
    ⚠️ Remember: This expert only discusses social media topics!
    </div>
    """, unsafe_allow_html=True)
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()