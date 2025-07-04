# app.py - Main Streamlit application (WORKING VERSION)
import streamlit as st
import requests
import json
from utils import SimpleMedicalAI, SymptomChecker

# Initialize AI
@st.cache_resource
def load_ai():
    return SimpleMedicalAI(), SymptomChecker()

medical_ai, symptom_checker = load_ai()

def main():
    st.set_page_config(
        page_title="BharatHealthGPT Demo",
        page_icon="🏥",
        layout="wide"
    )
    
    # Header
    st.title("🏥 BharatHealthGPT - Healthcare AI Demo")
    st.markdown("### Multilingual AI Healthcare Assistant")
    
    # Sidebar for language selection
    st.sidebar.title("Settings")
    language = st.sidebar.selectbox(
        "Select Language / भाषा चुनें",
        ["english", "hindi"],
        index=0
    )
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["💬 Chat Consultation", "🔍 Symptom Checker", "ℹ️ About"])
    
    with tab1:
        chat_interface(language)
    
    with tab2:
        symptom_checker_interface(language)
    
    with tab3:
        about_interface()

def chat_interface(language):
    """Chat consultation interface"""
    st.markdown("### 💬 Chat with AI Doctor")
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # User input
    user_input = st.text_area(
        "Describe your health concern:",
        height=100,
        placeholder="Type your symptoms or health questions here..." if language == 'english' 
                   else "अपने लक्षण या स्वास्थ्य संबंधी प्रश्न यहाँ लिखें..."
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send", type="primary"):
            if user_input.strip():
                # Add user message to history
                st.session_state.chat_history.append({
                    "type": "user",
                    "message": user_input,
                    "language": language
                })
                
                # Get AI response
                with st.spinner("AI Doctor is thinking..."):
                    response = medical_ai.generate_response(user_input, language)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    "type": "ai",
                    "message": response['response'],
                    "emergency": response['emergency'],
                    "confidence": response['confidence']
                })
                
                # Clear input
                st.rerun()
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["type"] == "user":
            st.markdown(f"**You:** {chat['message']}")
        else:
            if chat.get("emergency", False):
                st.error(f"**AI Doctor:** {chat['message']}")
            else:
                st.success(f"**AI Doctor:** {chat['message']}")
            
            # Show confidence
            if 'confidence' in chat:
                st.caption(f"Confidence: {chat['confidence']:.1%}")

def symptom_checker_interface(language):
    """Symptom checker interface"""
    st.markdown("### 🔍 Quick Symptom Checker")
    
    # Symptom options
    symptoms_options = {
        'english': ['Fever', 'Headache', 'Cough', 'Stomach Pain', 'Nausea', 'Chest Pain', 'Fatigue'],
        'hindi': ['बुखार (Fever)', 'सिरदर्द (Headache)', 'खांसी (Cough)', 'पेट दर्द (Stomach Pain)', 
                 'जी मिचलाना (Nausea)', 'छाती में दर्द (Chest Pain)', 'थकान (Fatigue)']
    }
    
    selected_symptoms = st.multiselect(
        "Select your symptoms:",
        symptoms_options[language]
    )
    
    if st.button("Check Symptoms"):
        if selected_symptoms:
            # Convert to English for processing
            english_symptoms = []
            for symptom in selected_symptoms:
                if '(' in symptom:
                    english_symptoms.append(symptom.split('(')[1].replace(')', ''))
                else:
                    english_symptoms.append(symptom)
            
            advice = symptom_checker.check_symptoms(english_symptoms, language)
            
            if "emergency" in advice.lower() or "आपातकाल" in advice:
                st.error(f"⚠️ {advice}")
            else:
                st.info(advice)
        else:
            st.warning("Please select at least one symptom.")

def about_interface():
    """About page"""
    st.markdown("### ℹ️ About BharatHealthGPT Demo")
    
    st.markdown("""
    **BharatHealthGPT** is a demonstration of AI-powered healthcare assistance supporting multiple Indian languages.
    
    **Features:**
    - 🗣️ Multilingual support (Hindi, English, and more)
    - 🤖 AI-powered symptom analysis
    - ⚠️ Emergency situation detection
    - 💡 Health recommendations
    - 🔒 Privacy-focused design
    
    **Technology Stack:**
    - Frontend: Streamlit
    - Backend: FastAPI
    - AI: Transformer models with medical knowledge
    - Languages: Python
    
    **Disclaimer:**
    This is a demonstration system for educational purposes. Always consult qualified healthcare professionals for medical advice.
    
    **For Intel Unnati Program:**
    This demo showcases the potential of AI in healthcare accessibility across India's diverse linguistic landscape.
    """)

if __name__ == "__main__":
    main()
