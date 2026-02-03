import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- Page Configuration ---
st.set_page_config(page_title="Smart PDF Bot", layout="wide")
st.title("📄 Chat with PDF (Smart Model Selection)")

# --- Sidebar (Settings) ---
with st.sidebar:
    st.header("1. Settings")
    api_key = st.text_input("Google Gemini API Key:", type="password")
    st.markdown("[Get API Key Here](https://aistudio.google.com/app/apikey)")
    
    # --- DYNAMIC MODEL SELECTOR ---
    selected_model_name = None
    if api_key:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            
            # Ask Google: "Which models are available?"
            model_list = []
            for m in genai.list_models():
                # Filter only models that support content generation
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            
            # Populate the dropdown
            if model_list:
                selected_model_name = st.selectbox("Select Model:", model_list, index=0)
                st.success(f"✅ {selected_model_name} selected.")
            else:
                st.error("No models found. Please check your API Key permissions.")
                
        except Exception as e:
            st.error(f"API Error: {e}")

    st.header("2. Upload Documents")
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type="pdf")

# --- Main Logic ---
def get_response(files, user_question, key, model_name):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_name) 
    
    # Read PDF Files
    full_text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    
    # English Prompt for the AI
    prompt = f"""
    You are a helpful AI assistant. Answer the question strictly based on the provided context below.
    
    CONTEXT:
    {full_text}
    
    QUESTION:
    {user_question}
    """
    
    with st.spinner(f"AI ({model_name}) is processing..."):
        response = model.generate_content(prompt)
        return response.text

# --- App Execution ---
if api_key and uploaded_files and selected_model_name:
    user_question = st.chat_input("Ask a question about your PDF...")
    
    # Session State for Chat History
    if "history" not in st.session_state:
        st.session_state.history = []
        
    # Display Chat History
    for role, text in st.session_state.history:
        with st.chat_message(role):
            st.write(text)
            
    # Handle User Input
    if user_question:
        st.session_state.history.append(("user", user_question))
        with st.chat_message("user"):
            st.write(user_question)
            
        try:
            answer = get_response(uploaded_files, user_question, api_key, selected_model_name)
            st.session_state.history.append(("assistant", answer))
            with st.chat_message("assistant"):
                st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

elif not api_key:
    st.info("👈 Please enter your API Key in the sidebar to load available models.")
elif not uploaded_files:
    st.info("👈 Please upload a PDF file to start chatting.")
