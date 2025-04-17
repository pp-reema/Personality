import os
import streamlit as st
from openai import OpenAI
import time
import random
import base64
from audio_recorder_streamlit import audio_recorder
import io
from gtts import gTTS

st.set_page_config(page_title="Personality Conversation", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Instagram-like light theme with improved message spacing
st.markdown("""
<style>
    /* Instagram-inspired light theme */
.main {
    background-color: #FFFFFF;
    color: #262626;
}
.stApp {
    background-color: #FFFFFF;
}
.chat-container {
    max-width: 450px; 
    margin: 0 auto;
    padding: 10px;
}
.message-container {
    display: flex;
    margin-bottom: 10px;
    animation: fadeIn 0.3s ease-in;
}
.message {
    padding: 10px 15px;
    border-radius: 15px;
    /* Removed max-width to let it be determined by content */
    word-wrap: break-word;
    display: inline-block;
    max-width: 80%;
}
.bot-message {
    background-color: #EFEFEF;
    color: #262626;
    margin-right: auto;
    border-radius: 18px 18px 18px 4px;
}
.user-message {
    background-color: #0095F6;
    color: white;
    margin-left: auto;
    border-radius: 18px 18px 4px 18px;
}
.message-time {
    font-size: 0.7em;
    color: #8e8e8e;
    margin-top: 2px;
    text-align: right;
}
.input-container {
    display: flex;
    align-items: center;
    background-color: #EFEFEF;
    border-radius: 22px;
    padding: 8px 15px;
    margin-top: 20px;
}
/* Space between Q&A pairs */
.qa-pair-separator {
    height: 20px;
}
/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
/* Custom input field */
.stTextInput input {
    background-color: #EFEFEF !important;
    color: #262626 !important;
    border: none !important;
    padding: 10px !important;
    border-radius: 20px !important;
}
.stTextInput div[data-baseweb="base-input"] {
    background-color: #EFEFEF !important;
    border-radius: 20px !important;
}
/* Button styling */
.stButton button {
    background-color: #0095F6 !important;
    color: white !important;
    border-radius: 20px !important;
    border: none !important;
    padding: 5px 15px !important;
}
/* Send button styling */
.send-button {
    background-color: #0095F6 !important;
    color: white !important;
    border-radius: 50% !important;
    border: none !important;
    width: 36px !important;
    height: 36px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}
/* Timer styling - moved below input */
.timer-container {
    margin-top: 15px;
    text-align: center;
    font-size: 1.2em;
    color: #262626;
}
</style>
""", unsafe_allow_html=True)

# Function to autoplay audio
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

# Function for text-to-speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    # Save temporarily
    with open("temp_speech.mp3", "wb") as f:
        f.write(fp.read())
    
    autoplay_audio("temp_speech.mp3")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
except Exception as e:
    st.error(f"Error initializing OpenAI client: {e}")
    client = None

# Custom header
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.write("")
    with col2:
        st.markdown("<div class='header'><h2> Personality Test </h2></div>", unsafe_allow_html=True)
    with col3:
        st.write("")

# Session state initialization
if 'first_question' not in st.session_state:
    st.session_state.first_question = "Welcome. I will ask you a couple of questions over 5 minutes to understand who you really are. So can I ask you, what's been the highlight of your week so far?"

if 'question_index' not in st.session_state:
    st.session_state.question_index = 0

if 'responses' not in st.session_state:
    st.session_state.responses = []

if 'convo_log' not in st.session_state:
    st.session_state.convo_log = []

if 'voice_mode' not in st.session_state:
    st.session_state.voice_mode = False

if 'first_load' not in st.session_state:
    st.session_state.first_load = True

# Timer setup
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()

# Get current question
if st.session_state.question_index == 0:
    current_q = st.session_state.first_question
else:
    prev_ans = st.session_state.responses[-1]
    
    if client:
        try:
            # Updated OpenAI API call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an insightful psychologist. Based on the user's previous response, ask an open-ended follow-up question to understand their personality better."},
                    {"role": "user", "content": prev_ans}
                ]
            )
            current_q = response.choices[0].message.content.strip()
        except Exception as e:
            st.warning(f"Using a fallback question due to API error: {e}")
            current_q = random.choice([
                "What motivates you the most in life?",
                "How do you usually handle challenging situations?",
                "Can you share a moment when you felt truly proud?",
                "What do you value most in your relationships?",
                "How would your close friends describe you?"
            ])
    else:
        st.warning("API key not available. Using fallback questions.")
        current_q = random.choice([
            "What motivates you the most in life?",
            "How do you usually handle challenging situations?",
            "Can you share a moment when you felt truly proud?",
            "What do you value most in your relationships?",
            "How would your close friends describe you?"
        ])

# Auto-play the question audio when a new question appears
if len(st.session_state.convo_log) <= st.session_state.question_index or st.session_state.first_load:
    text_to_speech(current_q)
    st.session_state.first_load = False

# Chat container for messages
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display previous conversations with improved spacing
for convo in st.session_state.convo_log:
    if convo['answer']:  # Only show completed Q&A pairs
        st.markdown(f"""
        <div class='message-container'>
            <div class='message bot-message'>{convo['question']}</div>
        </div>
        <div class='message-container' style="margin-top: 16px;">
            <div class='message user-message'>{convo['answer']}</div>
        </div>
        <div class='qa-pair-separator'></div>
        """, unsafe_allow_html=True)

# Display current question
st.markdown(f"""
<div class='message-container'>
    <div class='message bot-message'>{current_q}</div>
</div>
""", unsafe_allow_html=True)

# Store current question
if len(st.session_state.convo_log) <= st.session_state.question_index:
    st.session_state.convo_log.append({"question": current_q, "answer": ""})

# Create columns for input, send button, and mic button
col1, col2, col3 = st.columns([6, 0.7, 0.7])

# Text input
with col1:
    user_input = st.text_input("", 
                              key=f"response_{st.session_state.question_index}", 
                              placeholder="Type your response here...")
    
    # JavaScript to submit form on Enter key
    st.markdown("""
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Add event listener once DOM is fully loaded
        setTimeout(function() {
            const textInputs = document.querySelectorAll('input[type="text"]');
            textInputs.forEach(function(input) {
                input.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        // Find the closest send button
                        const buttons = document.querySelectorAll('button');
                        for (let button of buttons) {
                            if (button.innerText === '➤') {
                                button.click();
                                break;
                            }
                        }
                    }
                });
            });
        }, 1000); // Delay to ensure elements are loaded
    });
    </script>
    """, unsafe_allow_html=True)

# Send button
with col2:
    if st.button("➤", key="send_button", help="Send message"):
        if user_input.strip():
            st.session_state.responses.append(user_input)
            st.session_state.convo_log[st.session_state.question_index]["answer"] = user_input
            st.session_state.question_index += 1
            st.rerun()
        else:
            st.warning("Please enter a response before continuing.")

# Handle voice input toggle
with col3:
    mic_icon = "🎤" if not st.session_state.voice_mode else "⌨️"
    if st.button(mic_icon):
        st.session_state.voice_mode = not st.session_state.voice_mode
        st.rerun()

# Voice input display
if st.session_state.voice_mode:
    st.write("Speak now... (Click the 'Stop' button when finished)")
    audio_bytes = audio_recorder()
    
    if audio_bytes:
        st.info("Processing your audio...")
        try:
            # Save audio to file with error handling
            try:
                with open("temp_audio.wav", "wb") as f:
                    f.write(audio_bytes)
                st.success("Audio saved successfully")
            except Exception as e:
                st.error(f"Error saving audio file: {e}")
                st.stop()
            
            # Check if file exists and has content
            import os
            if os.path.exists("temp_audio.wav") and os.path.getsize("temp_audio.wav") > 0:
                st.success("Audio file verified")
            else:
                st.error("Audio file is empty or not created properly")
                st.stop()
            
            # Verify client initialization
            if not client:
                st.error("OpenAI client not properly initialized")
                st.stop()
                
            # Open file for API
            audio_file = open("temp_audio.wav", "rb")
            
            # Process with Whisper API with more detailed error handling
            try:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                user_input = transcript.text
                st.success(f"Transcription successful: '{user_input}'")
                
                # Display the transcribed text
                st.markdown(f"""
                <div class='message-container'>
                    <div class='message user-message'>{user_input}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Store and proceed
                if user_input.strip():
                    st.session_state.responses.append(user_input)
                    st.session_state.convo_log[st.session_state.question_index]["answer"] = user_input
                    st.session_state.question_index += 1
                    st.rerun()
                
            except Exception as e:
                st.error(f"Whisper API transcription error: {e}")
                
            # Close the file
            audio_file.close()
                
        except Exception as e:
            st.error(f"Error processing audio: {e}")
            import traceback
            st.code(traceback.format_exc())
            
st.markdown("</div>", unsafe_allow_html=True)  # Close chat container

# Timer logic - Moved below input
elapsed = int(time.time() - st.session_state.start_time)
remaining = 300 - elapsed

if remaining <= 0:
    st.success("Interview finished! Generating your results...")
    st.switch_page("pages/3_Results.py")
else:
    mins, secs = divmod(remaining, 60)
    st.markdown(f"""
    <div class='timer-container'>
        ⏱️ {mins:02d}:{secs:02d}
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh to update timer
st.markdown(f"""
<script>
    setTimeout(function(){{
        window.location.reload();
    }}, 5000);
</script>
""", unsafe_allow_html=True)
