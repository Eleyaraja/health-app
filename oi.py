import os
import time
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import json

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = "your api"
if not api_key:
    st.error("API key is missing. Please set the GOOGLE_API_KEY.")
else:
    genai.configure(api_key=api_key)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None

# Enhanced analysis prompt
DEFAULT_PROMPT = """You are a professional nutritionist and dietitian. Analyze the food items in this image with extreme detail.
Provide:
1. Detailed list of all visible food items
2. Estimated quantities/serving sizes
3. Calories per item (include measurement unit)
4. Macronutrients breakdown (proteins, carbs, fats in grams)
5. Micronutrients highlights (vitamins, minerals)
6. Health score (1-10) for each item
7. Potential allergens
8. Total nutritional summary

Format response in JSON structure with this schema:
{
    "food_analysis": {
        "items": [
            {
                "name": "item name",
                "quantity": "estimated amount",
                "calories": "X kcal",
                "proteins": "X g",
                "carbs": "X g",
                "fats": "X g",
                "health_score": X,
                "allergens": ["list"],
                "micronutrients": ["key nutrients"]
            }
        ],
        "total_calories": "X kcal",
        "overall_health_score": X,
        "dietary_recommendations": ["list"]
    }
}"""

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
    st.download_button("Example Image", "https://github.com/.../example.jpg", 
                      "example_food.jpg", "Try with our example image")

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
        with st.expander("Advanced Options", expanded=True):
            custom_prompt = st.text_area("Customize Analysis Prompt", DEFAULT_PROMPT,
                                        height=200,
                                        help="Modify the expert instructions as needed")
            st.caption("💡 Tip: Ask for specific diet comparisons or meal suggestions!")
        
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            with st.spinner("🔍 Scanning image with AI..."):
                start_time = time.time()
                
                response = get_gemini_response(custom_prompt, st.session_state.uploaded_image)
                
                if response:
                    try:
                        analysis_data = json.loads(response)
                        st.session_state.analysis = analysis_data
                        
                        # Display Results
                        st.success(f"Analysis completed in {time.time()-start_time:.1f}s")
                        
                        with st.container():
                            st.subheader("📊 Nutritional Breakdown")
                            
                            # Convert to DataFrame
                            df = pd.DataFrame(analysis_data['food_analysis']['items'])
                            
                            # Summary Cards
                            cols = st.columns(3)
                            cols[0].metric("Total Calories", 
                                          analysis_data['food_analysis']['total_calories'])
                            cols[1].metric("Overall Health Score", 
                                          f"{analysis_data['food_analysis']['overall_health_score']}/10")
                            cols[2].metric("Items Identified", len(df))
                            
                            # Interactive Data Table
                            st.dataframe(df, use_container_width=True)
                            
                            # Visualizations
                            tab1, tab2, tab3 = st.tabs(["Macronutrients", "Health Scores", "Recommendations"])
                            
                            with tab1:
                                macronutrients = df[['name', 'proteins', 'carbs', 'fats']]
                                macronutrients = macronutrients.set_index('name')
                                st.bar_chart(macronutrients)
                            
                            with tab2:
                                st.write("Health Quality Assessment")
                                st.scatter_chart(df[['name', 'health_score']].set_index('name'))
                            
                            with tab3:
                                st.write("Dietary Recommendations")
                                for rec in analysis_data['food_analysis']['dietary_recommendations']:
                                    st.write(f"- {rec}")
                        
                    except json.JSONDecodeError:
                        st.markdown("### Analysis Results")
                        st.write(response)
        
        # Chat Interface
        st.divider()
        st.subheader("💬 Follow-up Questions")
        
        if 'analysis' in st.session_state:
            user_query = st.chat_input("Ask about this meal...")
            if user_query:
                with st.spinner("Analyzing..."):
                    chat_response = get_gemini_response(
                        f"Based on previous analysis: {user_query}", 
                        st.session_state.uploaded_image
                    )
                    st.session_state.chat_history.append({"user": user_query, "ai": chat_response})
                
                for entry in st.session_state.chat_history[-3:]:
                    with st.chat_message("user"):
                        st.write(entry["user"])
                    with st.chat_message("assistant"):
                        st.write(entry["ai"])

# Help Section
with st.expander("📌 Usage Guide"):
    st.markdown("""
    **How to Use:**
    1. Upload clear food photo
    2. Select analysis mode
    3. Review automatic results
    4. Ask follow-up questions
    
    **Tips:**
    - Use natural lighting for best results
    - Show portion sizes clearly
    - Ask for alternatives or diet-specific advice
    """)

# Footer
st.divider()
st.markdown("""
*Powered by Google Gemini AI • 🍎 Health Data from USDA Database • 
[Report Issues](https://example.com) • [Privacy Policy](https://example.com/privacy)*
""")
