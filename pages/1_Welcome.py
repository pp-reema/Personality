import streamlit as st
from streamlit.components.v1 import html
from gtts import gTTS
import os
import base64
import uuid


# Function to convert text to auto-playing audio
def autoplay_audio(text, lang='en'):
    filename = f"{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    with open(filename, "rb") as f:
        audio_bytes = f.read()
    os.remove(filename)

    b64 = base64.b64encode(audio_bytes).decode()

    audio_html = f"""
        <audio autoplay="true" style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    return audio_html

# Instagram light theme colors
instagram_light_css = """
<style>
    /* Main Instagram light theme colors */
    .main {
        background-color: #fafafa;
        color: #262626;
    }
    .stApp {
        background-color: #fafafa;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #0095F6;
        color: white;
        border-radius: 4px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5 {
        color: #262626 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }
    p {
        color: #262626;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Instagram message container */
    .message-container {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        margin: 30px 0;
        border: 1px solid #efefef;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease;
    }
    
    .message-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }
    
    /* Title styling */
    .title-text {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #fd1d1d, #833ab4, #405de6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
        margin-bottom: 10px;
    }
</style>
"""

# Streamlit Page 1: Welcome
st.set_page_config(page_title="AI Personality Interview", layout="centered")

# Apply Instagram light theme CSS
st.markdown(instagram_light_css, unsafe_allow_html=True)

# Title with gradient effect
st.markdown('<div class="title-text">Welcome to the AI Personality Test</div>', unsafe_allow_html=True)

# Message in Instagram style container
st.markdown("""
<div class="message-container">
    <p>You will now have a conversation with an AI personality analyst.<br>
    Make sure you are in a quiet and comfortable environment.<br>
    The more detailed your answers are, the better your analysis will be.</p>
</div>
""", unsafe_allow_html=True)

welcome_message = """
You will now have a conversation with an AI personality analyst. 
Make sure you are in a quiet and comfortable environment. 
The more detailed your answers are, the better your analysis will be.
"""

html(autoplay_audio(welcome_message), height=0)

# Button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("✅ Ready to go", use_container_width=True):
        st.switch_page("pages/2_Conversation.py")  # Adjust path if needed
