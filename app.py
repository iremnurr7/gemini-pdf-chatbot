import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Akıllı PDF Botu", layout="wide")
st.title("📄 PDF ile Konuş (Otomatik Model Seçimi)")

# --- Yan Menü ---
with st.sidebar:
    st.header("1. Ayarlar")
    api_key = st.text_input("Google Gemini API Key:", type="password")
    st.markdown("[Key Almak İçin Tıkla](https://aistudio.google.com/app/apikey)")
    
    # --- DİNAMİK MODEL SEÇİCİ ---
    selected_model_name = None
    if api_key:
        try:
            # API'yi kur
            genai.configure(api_key=api_key)
            
            # Google'a sor: "Hangi modellerin var?"
            model_list = []
            for m in genai.list_models():
                # Sadece sohbet edebilen modelleri al
                if 'generateContent' in m.supported_generation_methods:
                    model_list.append(m.name)
            
            # Listeyi kutuya koy
            if model_list:
                selected_model_name = st.selectbox("Kullanılacak Model:", model_list, index=0)
                st.success(f"✅ {selected_model_name} seçildi.")
            else:
                st.error("Hiçbir model bulunamadı. API Key yetkilerini kontrol et.")
                
        except Exception as e:
            st.error(f"API Hatası: {e}")

    st.header("2. Dosya Yükle")
    uploaded_files = st.file_uploader("PDF Dosyalarını Seç", accept_multiple_files=True, type="pdf")

# --- Ana Fonksiyon ---
def get_response(files, user_question, key, model_name):
    genai.configure(api_key=key)
    model = genai.GenerativeModel(model_name) # Seçilen modeli kullan
    
    # PDF Oku
    full_text = ""
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
    
    # Prompt
    prompt = f"""
    Aşağıdaki metne göre soruyu cevapla.
    METİN: {full_text}
    SORU: {user_question}
    """
    
    with st.spinner(f"Yapay zeka ({model_name}) düşünüyor..."):
        response = model.generate_content(prompt)
        return response.text

# --- Çalıştırma ---
if api_key and uploaded_files and selected_model_name:
    user_question = st.chat_input("Sorunu sor...")
    
    if "history" not in st.session_state:
        st.session_state.history = []
        
    for role, text in st.session_state.history:
        with st.chat_message(role):
            st.write(text)
            
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
            st.error(f"Hata: {e}")

elif not api_key:
    st.info("👈 Önce API Key gir, sonra model listesi yüklenecek.")