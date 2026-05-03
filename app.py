# Import necessary libraries 
import streamlit as st                      # Web app interface
import google.generativeai as genai        # Gemini AI for translation
from dotenv import load_dotenv             # To load API keys securely
import os                                  # For environment variable access
from gtts import gTTS                      # For text-to-speech
import speech_recognition as sr            # For speech-to-text
from audio_recorder_streamlit import audio_recorder # For web-based audio recording
import tempfile                            # For temporary files

# Load environment variables from .env 
load_dotenv()

# Configure Gemini AI using your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the Gemini model 
model = genai.GenerativeModel("gemini-2.5-flash")

# Define translation function
def language_translate(text, source_lang, target_lang):
    # Format the prompt for Gemini
    prompt = f"""
    Translate the following text from {source_lang} to {target_lang}:

    {text}

    Please don't add any extra text, only the translated text.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if response else "Translation failed."

# Generate Audio function
def generate_audio(text, lang_code="en"):
    try:
        tts = gTTS(text=text, lang=lang_code)
        # Save to a temporary file
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_audio.name)
        return temp_audio.name
    except Exception as e:
        return None

LANGUAGE_CODES = {
    "English": "en", "Spanish": "es", "French": "fr", "German": "de", "Urdu": "ur", "Hindi": "hi", 
    "Chinese": "zh-cn", "Japanese": "ja", "Korean": "ko", "Arabic": "ar", "Russian": "ru", 
    "Portuguese": "pt", "Italian": "it", "Dutch": "nl", "Greek": "el", "Polish": "pl", 
    "Swedish": "sv", "Turkish": "tr", "Thai": "th", "Vietnamese": "vi", "Indonesian": "id", 
    "Hebrew": "he", "Czech": "cs", "Hungarian": "hu", "Finnish": "fi", "Romanian": "ro", 
    "Bulgarian": "bg", "Ukrainian": "uk", "Malay": "ms", "Filipino": "tl", "Tamil": "ta", 
    "Telugu": "te", "Kannada": "kn", "Marathi": "mr", "Gujarati": "gu", "Bengali": "bn", 
    "Pashto": "ps", "Farsi": "fa", "Sinhala": "si", "Swahili": "sw", "Zulu": "zu", "Xhosa": "xh", 
    "Yoruba": "yo", "Igbo": "ig", "Hausa": "ha", "Somali": "so", "Amharic": "am", "Nepali": "ne", 
    "Burmese": "my", "Khmer": "km", "Lao": "lo"
}

# Front end design with Streamlit

# Page setup
st.set_page_config(page_title="Instant Translate AI", layout="centered", page_icon="⚡")

# Custom CSS for Modern UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
    }
    .main-title {
        text-align: center;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(90deg, #4ECDC4, #556270);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    .translation-box {
        background-color: rgba(78, 205, 196, 0.1);
        border-left: 4px solid #4ECDC4;
        padding: 1.5rem;
        border-radius: 0 10px 10px 0;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<div class='main-title'>⚡ Instant Translate AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Seamlessly translate text and voice in real-time</div>", unsafe_allow_html=True)

# List of supported languages
languages = sorted(list(LANGUAGE_CODES.keys()))

# Language selectors
st.markdown("### 🌐 Select Languages")
col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Translate from:", languages, index=languages.index("English"))
with col2:
    target_lang = st.selectbox("Translate to:", languages, index=languages.index("French"))

st.markdown("---")

# Tabs for Text vs Voice Input
tab1, tab2 = st.tabs(["📝 Text Input", "🎙️ Voice Input"])

def handle_translation(text, src_lang, tgt_lang):
    if text.strip():
        with st.spinner("Translating..."):
            translation = language_translate(text, src_lang, tgt_lang)
            
        st.markdown("### ✨ Translation")
        st.markdown(f"<div class='translation-box'>{translation}</div>", unsafe_allow_html=True)
        
        # Audio Output
        tgt_code = LANGUAGE_CODES.get(tgt_lang, "en")
        audio_file = generate_audio(translation, lang_code=tgt_code)
        if audio_file:
            st.markdown("#### 🔊 Listen")
            st.audio(audio_file, format='audio/mp3')
    else:
        st.warning("⚠️ Please provide some input to translate.")

with tab1:
    user_text = st.text_area("Enter the text you want to translate:", height=150)
    if st.button("Translate Text", key="btn_text"):
        handle_translation(user_text, source_lang, target_lang)

with tab2:
    st.markdown("<h3 style='text-align: center; color: #4ECDC4;'>🎙️ Voice Input</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; margin-bottom: 2rem;'>Click the microphone icon below to start recording. Click again to stop.</p>", unsafe_allow_html=True)
    
    # Center the audio recorder
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        audio_bytes = audio_recorder(text="", recording_color="#FF6B6B", neutral_color="#4ECDC4", icon_size="4x")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if audio_bytes:
        st.success("✅ Recording captured successfully!")
        st.audio(audio_bytes, format="audio/wav")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ Translate Voice", key="btn_voice", use_container_width=True):
            with st.spinner("Processing audio..."):
                # Save audio bytes to temp file for SpeechRecognition
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_in:
                    temp_audio_in.write(audio_bytes)
                    temp_audio_path = temp_audio_in.name
                
                # Recognize speech
                recognizer = sr.Recognizer()
                with sr.AudioFile(temp_audio_path) as source:
                    audio_data = recognizer.record(source)
                    try:
                        src_code = LANGUAGE_CODES.get(source_lang, "en")
                        recognized_text = recognizer.recognize_google(audio_data, language=src_code)
                        st.info(f"**Recognized Text:** {recognized_text}")
                        handle_translation(recognized_text, source_lang, target_lang)
                    except sr.UnknownValueError:
                        st.error("Sorry, I could not understand the audio. Please try again.")
                    except sr.RequestError as e:
                        st.error(f"Could not request results from Google Speech Recognition service; {e}")
