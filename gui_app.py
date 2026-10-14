import os
import streamlit as st
from google import genai
from PIL import Image

# 1. Page Configuration and Layout Initialization
st.set_page_config(page_title="OmniAssistant AI", page_icon="🤖", layout="wide")
st.title("OmniAssistant AI - Multifunctional Suite")

# =====================================================================
# API CONFIGURATION & CLIENT INITIALIZATION
# =====================================================================
API_KEY = "api__key" 
MODEL_NAME = "gemini-3.8-flash"

if "gemini_client" not in st.session_state:
    try:
        st.session_state.gemini_client = genai.Client(api_key=API_KEY)
    except Exception as e:
        st.error(f"Failed to initialize Gemini Client: {e}")
client = st.session_state.gemini_client
# =====================================================================
# SIDEBAR NAVIGATION
# =====================================================================
with st.sidebar:
    st.header("Control Panel")
    module_choice = st.radio(
        "Choose a Module:", 
        ["Text Summarizer", "Interactive Chatbot", "Computer Vision"]
    )
    st.markdown("---")
    st.caption("Powered by Google Gemini 3.8 Flash & Streamlit")

# =====================================================================
# MODULE 1: TEXT SUMMARIZER & ANALYZER
# =====================================================================
if module_choice == "Text Summarizer":
    st.header("Text Summarizer & Sentiment Analyzer")
    
    with st.form("summarizer_form"):
        user_text = st.text_area("Paste or type the text you want to analyze:", height=250)
        submit_button = st.form_submit_button("Analyze Text", type="primary")
        
    if submit_button:
        if not user_text.strip():
            st.warning("Please enter some text before analyzing.")
        else:
            prompt = f"Analyze and summarize this text in 3-5 bullet points with sentiment analysis:\n{user_text}"
            output_container = st.empty()
            full_response = ""
            
            try:
                stream = client.models.generate_content_stream(model=MODEL_NAME, contents=prompt)
                for chunk in stream:
                    if chunk.text:
                        full_response += chunk.text
                        output_container.markdown(full_response + "▌")
                output_container.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred during execution: {e}")

# =====================================================================
# MODULE 2: INTERACTIVE CHATBOT (Safe Isolation)
# =====================================================================
elif module_choice == "Interactive Chatbot":
    st.header("Continuous Chatbot")
    
    # SAFE INITIALIZATION: Initialize internal structures only within this scope execution block
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat_session" not in st.session_state:
        try:
            st.session_state.chat_session = client.chats.create(model=MODEL_NAME)
        except Exception as e:
            st.error(f"Could not connect to Gemini Chat servers. Check your API key. Error: {e}")
            st.stop() # Halts rendering gracefully instead of triggering a fatal application crash

    # Re-draw the entire past conversation log container on screen refresh
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Monitor user text submissions into the input bar
    if user_message := st.chat_input("Type your message here..."):
        with st.chat_message("user"):
            st.markdown(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})

        # Generate and stream the assistant's reply inside a structural chat container
        with st.chat_message("assistant"):
            output_container = st.empty()
            full_response = ""
            try:
                stream = st.session_state.chat_session.send_message_stream(user_message)
                for chunk in stream:
                    if chunk.text:
                        full_response += chunk.text
                        output_container.markdown(full_response + "▌")
                output_container.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"An error occurred during streaming execution: {e}")

# =====================================================================
# MODULE 3: COMPUTER VISION (IMAGE ANALYSIS)
# =====================================================================
elif module_choice == "Computer Vision":
    st.header("Computer Vision (Image Analysis)")
    
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png", "webp"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with st.form("vision_form"):
            user_question = st.text_input("What do you want to know about this image?", "Describe this image in detail.")
            submit_vision = st.form_submit_button("Analyze Image", type="primary")
        
        if submit_vision:
            output_container = st.empty()
            full_response = ""
            try:
                stream = client.models.generate_content_stream(
                    model=MODEL_NAME,
                    contents=[user_question, image]
                )
                for chunk in stream:
                    if chunk.text:
                        full_response += chunk.text
                        output_container.markdown(full_response + "▌")
                output_container.markdown(full_response)
            except Exception as e:
                st.error(f"An error occurred during vision processing: {e}")
