import os
import time
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# Configure Gemini API
API_KEY = "AIzaSyDGcEK-0nno_80QYBy-__6i8kkSIHYQ58g"
genai.configure(api_key=API_KEY)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

def get_gemini_response(prompt, image_data):
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content([prompt, image_data[0]])
        return response.text
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None

def process_image(uploaded_file):
    if uploaded_file:
        return [{"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()}]
    return None

# Streamlit UI Configuration
st.set_page_config(page_title="BAT Health AI", layout="wide", page_icon="🌱")
st.header("🍏 BAT Health AI - Advanced Nutritional Analysis")

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Settings")
    analysis_mode = st.selectbox("Analysis Mode", ["Standard", "Detailed Scan", "Diet Planning"], 
                               help="Choose analysis depth and focus")
    diet_type = st.selectbox("Dietary Preference", ["Any", "Vegetarian", "Vegan", "Keto", "Low-Carb"],
                            help="Set dietary preferences for recommendations")

# Main Interface Columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📤 Image Upload")
    uploaded_file = st.file_uploader("Upload food image", type=["jpg", "jpeg", "png"], 
                                   help="Clear well-lit photos work best!")
    if uploaded_file:
        st.session_state.uploaded_image = process_image(uploaded_file)
        st.image(Image.open(uploaded_file), use_column_width=True)

with col2:
    st.subheader("🔍 Analysis Panel")
    if uploaded_file:
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            with st.spinner("🔍 Scanning image with AI..."):
                start_time = time.time()
                response = get_gemini_response("Analyze this food image for nutrition details.", st.session_state.uploaded_image)
                if response:
                    st.success(f"Analysis completed in {time.time()-start_time:.1f}s")
                    st.write(response)

# Chat Interface
st.divider()
st.subheader("💬 Follow-up Questions")
if 'uploaded_image' in st.session_state:
    user_query = st.chat_input("Ask about this meal...")
    if user_query:
        with st.spinner("Analyzing..."):
            chat_response = get_gemini_response(user_query, st.session_state.uploaded_image)
            st.session_state.chat_history.append({"user": user_query, "ai": chat_response})
        for entry in st.session_state.chat_history[-3:]:
            with st.chat_message("user"):
                st.write(entry["user"])
            with st.chat_message("assistant"):
                st.write(entry["ai"])
