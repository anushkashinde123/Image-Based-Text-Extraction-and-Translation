import streamlit as st
from PIL import Image
import easyocr
from gtts import gTTS
import os
import io
import numpy as np
from deep_translator import GoogleTranslator

# Set up page config
st.set_page_config(page_title="Multilingual Text Translator", layout="wide")

# Define supported languages
lang_dict = {
    'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr', 'Tamil': 'ta',
    'Telugu': 'te', 'Kannada': 'kn', 'Gujarati': 'gu', 'Bengali': 'bn',
    'Punjabi': 'pa', 'Urdu': 'ur'
}
lang_names = list(lang_dict.keys())

# Initialize session states
if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = "📸 OCR + Translate"

# Sidebar Navigation
st.sidebar.title("📚 Features")
feature = st.sidebar.radio("Choose a feature", ["📸 OCR + Translate", "📖 Dictionary", "🕒 History"])
st.session_state.selected_feature = feature

# Custom styling
st.markdown("""
    <style>
    .main-title { text-align: center; font-size: 40px; font-weight: bold; color: #4A90E2; }
    .sub-title { text-align: center; font-size: 20px; margin-bottom: 30px; }
    .stButton>button { background-color: #4A90E2; color: white; border-radius: 8px; }
    .stTextInput>div>input { border-radius: 8px; }
    .stSelectbox>div { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">🌍 Multilingual OCR Translator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Capture text, translate it, and listen to it aloud!</div>', unsafe_allow_html=True)

# ---------- 📸 OCR + Translate Feature ----------
if feature == "📸 OCR + Translate":
    col1, col2 = st.columns(2)

    with col1:
        input_method = st.radio("Input Method", ["Upload Image", "Use Camera"])
        image = None
        if input_method == "Upload Image":
            uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
            if uploaded_image:
                image = Image.open(uploaded_image)
        else:
            camera_image = st.camera_input("Capture Image")
            if camera_image:
                image = Image.open(camera_image)

    with col2:
        source_lang = st.selectbox("Select Source Language (for OCR)", lang_names, index=0)
        target_lang = st.selectbox("Select Target Language (for Translation)", lang_names, index=1)

        if image:
            st.image(image, caption="Uploaded Image", use_container_width=True)
            with st.spinner("🔍 Extracting text..."):
                try:
                    reader = easyocr.Reader([lang_dict[source_lang]], gpu=False)
                    image_np = np.array(image)  # ✅ Fix: Convert PIL to numpy
                    result = reader.readtext(image_np)
                    extracted_text = " ".join([text[1] for text in result])
                    st.subheader("📄 Extracted Text")
                    st.write(extracted_text)

                    # Translate
                    translated_text = GoogleTranslator(source=lang_dict[source_lang], target=lang_dict[target_lang]).translate(extracted_text)
                    st.subheader("🌐 Translated Text")
                    st.write(translated_text)

                    # Add to history
                    st.session_state.history.append({
                        "original": extracted_text,
                        "translated": translated_text,
                        "source_lang": source_lang,
                        "target_lang": target_lang
                    })

                    # TTS
                    if st.button("🔊 Listen"):
                        tts = gTTS(text=translated_text, lang=lang_dict[target_lang])
                        audio_file = "output.mp3"
                        tts.save(audio_file)
                        audio_bytes = open(audio_file, "rb").read()
                        st.audio(audio_bytes, format="audio/mp3")
                        os.remove(audio_file)

                except Exception as e:
                    st.error(f"❌ Error processing image: {e}")
        else:
            st.info("📌 Please upload or capture an image.")

# ---------- 📖 Dictionary Feature ----------
elif feature == "📖 Dictionary":
    st.subheader("🔤 Word Translation")
    word = st.text_input("Enter a word or short sentence:")
    src = st.selectbox("From Language", lang_names, index=0, key="dict_src")
    tgt = st.selectbox("To Language", lang_names, index=1, key="dict_tgt")

    if st.button("Translate"):
        try:
            translated_word = GoogleTranslator(source=lang_dict[src], target=lang_dict[tgt]).translate(word)
            st.success(f"📘 Translated: {translated_word}")
        except Exception as e:
            st.error(f"❌ Translation error: {e}")

# ---------- 🕒 History Feature ----------
elif feature == "🕒 History":
    st.subheader("📜 Translation History")
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**{i}.** *({entry['source_lang']} ➝ {entry['target_lang']})*")
            st.markdown(f"**Original:** {entry['original']}")
            st.markdown(f"**Translated:** {entry['translated']}")
            st.markdown("---")
    else:
        st.info("No history available yet.")
