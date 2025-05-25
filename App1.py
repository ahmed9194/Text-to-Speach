import streamlit as st
import pyttsx3
import base64
import os
from datetime import datetime
from langdetect import detect
from gtts import gTTS
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(
    page_title="Professional Text-to-Speech Converter",
    page_icon="🔊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextArea textarea {
        min-height: 300px;
        font-size: 18px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s;
        margin: 10px 0;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2C3E50, #4CA1AF);
        color: white;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 12px;
        background-color: #2C3E50;
        color: white;
        font-size: 14px;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def setup_session_state():
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""
    if 'selected_lang' not in st.session_state:
        st.session_state.selected_lang = "en"

def reshape_arabic(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def text_to_speech(text, language, voice_type, speed):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"speech_output_{timestamp}.mp3"
    
    if language == "ar":
        with st.spinner("Processing Arabic text..."):
            tts = gTTS(text=text, lang='ar', slow=False)
            tts.save(filename)
    else:
        with st.spinner("Converting text to speech..."):
            engine = pyttsx3.init()
            engine.setProperty('rate', speed)
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[0 if voice_type == "Male" else 1].id)
            engine.save_to_file(text, filename)
            engine.runAndWait()
    
    return filename

def create_download_link(filename):
    with open(filename, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/mp3;base64,{b64}" download="{filename}" style="text-decoration: none; color: white; background: #4CAF50; padding: 10px 20px; border-radius: 5px; font-weight: bold;">Download Audio</a>'
    return href

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def main_interface():
    st.title("Professional Text-to-Speech Converter")
    st.markdown("---")
    
    with st.sidebar:
        st.header("Settings")
        
        st.session_state.selected_lang = st.radio(
            "Select Language:",
            ["English", "Arabic"],
            index=0,
            key="lang_radio"
        )
        
        if st.session_state.selected_lang == "English":
            voice_type = st.selectbox("Voice Type", ["Male", "Female"], index=0)
        else:
            voice_type = "Female"
        
        speed = st.slider("Speech Speed", 80, 300, 175)
        
        st.markdown("---")
        st.markdown("### Quick Examples:")
        
        if st.session_state.selected_lang == "Arabic":
            examples = {
                "Welcome Message": "مرحبا بكم في نظام تحويل النص إلى كلام",
                "Commercial": "خصم خاص 50% على جميع المنتجات هذا الأسبوع",
                "News": "أعلنت الحكومة عن خطة جديدة للتنمية الاقتصادية"
            }
        else:
            examples = {
                "Welcome": "Welcome to our professional text-to-speech service",
                "Advertisement": "Limited time offer: 50% off all premium plans",
                "News": "Scientists discover breakthrough in renewable energy"
            }
        
        for name, text in examples.items():
            if st.button(name):
                st.session_state.text_input = text
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        label = "Enter your text here" if st.session_state.selected_lang == "English" else "أدخل النص هنا"
        placeholder = "Type or paste your text..." if st.session_state.selected_lang == "English" else "اكتب أو الصق النص هنا..."
        
        text_input = st.text_area(
            label,
            height=300,
            value=st.session_state.get("text_input", ""),
            placeholder=placeholder
        )
        
        button_text = "Convert to Speech" if st.session_state.selected_lang == "English" else "تحويل إلى كلام"
        if st.button(button_text, key="convert"):
            if text_input.strip():
                language = "en" if st.session_state.selected_lang == "English" else "ar"
                
                with st.spinner("Processing..."):
                    audio_file = text_to_speech(text_input, language, voice_type, speed)
                    
                    st.success("Conversion completed successfully!")
                    st.audio(audio_file)
                    st.markdown(create_download_link(audio_file), unsafe_allow_html=True)
                    
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
            else:
                st.warning("Please enter some text to convert")
    
    with col2:
        st.markdown("### Usage Tips:")
        
        if st.session_state.selected_lang == "Arabic":
            tips = [
                "استخدم علامات الترقيم لتقسيم الجمل",
                "تجنب النصوص الطويلة جدا",
                "اضبط السرعة حسب السياق",
                "جرب أمثلة قصيرة أولا"
            ]
        else:
            tips = [
                "Use punctuation for natural pauses",
                "Break long texts into paragraphs",
                "Adjust speed for different content",
                "Try short examples first"
            ]
        
        for tip in tips:
            st.markdown(f"- {tip}")
        
        st.markdown("### Features:")
        
        features = [
            "Multi-language support",
            "High-quality audio output",
            "MP3 download capability",
            "Real-time preview"
        ]
        
        for feature in features:
            st.markdown(f"- {feature}")

def footer():
    st.markdown("""
    <div class="footer">
        <p>© 2025 Professional TTS Converter | Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    setup_session_state()
    main_interface()
    footer()