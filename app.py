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
    # ✅ Latin Scripts
    'English': 'en',
    'French': 'fr',
    'German': 'de',
    'Spanish': 'es',
    'Italian': 'it',
    'Dutch': 'nl',
    'Danish': 'da',
    'Turkish': 'tr',
    # ✅ Devanagari Scripts
    'Hindi': 'hi',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Kannada': 'kn',
    'Nepali': 'ne',
    'Bengali': 'bn',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Sanskrit': 'sa',
    'Maithili': 'mai',
    'Magahi': 'mah',
    'Awadhi': 'ang',
    'Newari': 'new',
    'Konkani': 'gom',
    'Chhattisgarhi': 'sck',
    # ✅ Other Scripts
    'Czech': 'cs',
    'Hungarian': 'hu',
    'Finnish': 'fi',
    'Polish': 'pl',
    'Romanian': 'ro',
    'Indonesian': 'id',
    'Vietnamese': 'vi',
    'Malay': 'ms',
    'Afrikaans': 'af',
    'Icelandic': 'is',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Albanian': 'sq',
    'Lithuanian': 'lt',
    'Latvian': 'lv',
    'Welsh': 'cy',
    'Irish': 'ga',
    'Bosnian': 'bs',
    'Estonian': 'et',
    'Swahili': 'sw',
    'Uzbek': 'uz',
    'Filipino': 'tl',
    'Azerbaijani': 'az',
    'Kurdish': 'ku',
    'Latin': 'la',
    'Maltese': 'mt',
    'Maori': 'mi',
    'Occitan': 'oc',
    'Pijin': 'pi',
    # ✅ Arabic Scripts
    'Arabic': 'ar',
    'Persian': 'fa',
    'Urdu': 'ur',
    'Uyghur': 'ug',

    # ✅ Cyrillic Scripts
    'Russian': 'ru',
    'Ukrainian': 'uk',
    'Bulgarian': 'bg',
    'Belarusian': 'be',
    'Mongolian (Cyrillic)': 'mn',
    'Serbian (Cyrillic)': 'rs_cyrillic',

    # ✅ Bengali Scripts 
    'Assamese': 'as',
    'Manipuri': 'mni',

    
}
lang_names = list(lang_dict.keys())

# Initialize session states
if 'history' not in st.session_state:
    st.session_state.history = []
if 'selected_feature' not in st.session_state:
    st.session_state.selected_feature = "📸 OCR + Translate"

# Sidebar Navigation
st.sidebar.title("📚 Features")
feature = st.sidebar.radio("Choose a feature", ["📘 About Us","📸 OCR + Translate", "📖 Dictionary", "🕒 History"])
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

elif feature == "📘 About Us":
    
    st.markdown("""
<style>
.qb-features {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
    margin-top: 30px;
}
.qb-feature {
    flex: 1 1 200px;
    max-width: 220px;
    padding: 20px;
    border-left: 5px solid #ddd;
    border-radius: 10px;
    background-color: #fdf8fb;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    text-align: center;
    transition: transform 0.3s ease;
}
.qb-feature:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
}
.qb-feature h4 {
    margin-top: 15px;
    font-size: 18px;
    color: #1f2937;
}
.qb-feature p {
    font-size: 14px;
    color: #4b5563;
}
.qb-btn {
    display: inline-block;
    margin-top: 40px;
    background-color: #059669;
    color: white;
    padding: 12px 28px;
    border-radius: 999px;
    font-weight: 600;
    text-decoration: none;
}
.qb-btn:hover {
    background-color: #047857;
}
</style>

<div class="qb-features">
    <div class="qb-feature" style="border-left-color: #059669;">
        <img src="https://img.icons8.com/color/48/000000/flash-on.png"/>
        <h4>Instant</h4>
        <p>Get accurate translations in just a few seconds.</p>
    </div>
    <div class="qb-feature" style="border-left-color: #facc15;">
        <img src="https://img.icons8.com/color/48/000000/idea-sharing.png"/>
        <h4>Versatile</h4>
        <p>Translate words, sentences, or full paragraphs from any image.</p>
    </div>
    <div class="qb-feature" style="border-left-color: #ef4444;">
        <img src="https://img.icons8.com/color/48/000000/language.png"/>
        <h4>Multilingual</h4>
        <p>Supports 70+ languages including Hindi, Japanese, Arabic, and more.</p>
    </div>
    <div class="qb-feature" style="border-left-color: #8b5cf6;">
        <img src="https://img.icons8.com/color/48/000000/discount.png"/>
        <h4>Free & Fast</h4>
        <p>Use all features without cost or delay — no login required.</p>
    </div>
    <div class="qb-feature" style="border-left-color: #ec4899;">
        <img src="https://img.icons8.com/color/48/000000/lock.png"/>
        <h4>Secure</h4>
        <p>Your data stays private. Nothing is stored or tracked. 100% client-side OCR.</p>
    </div>
</div>


""", unsafe_allow_html=True)


    st.markdown("""
<style>
.how-to-use-container {
    background-color: #f9fbfd;
    padding: 40px 20px;
    border-radius: 12px;
    margin-top: 30px;
    margin-bottom: 40px;
    font-family: 'Segoe UI', sans-serif;
}
.how-to-use-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 10px;
}
.how-to-use-subtitle {
    text-align: center;
    font-size: 16px;
    color: #475569;
    margin-bottom: 40px;
}
.how-to-use-steps {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 30px;
}
.step-box {
    background-color: white;
    border-radius: 12px;
    text-align: center;
    padding: 20px;
    max-width: 220px;
    min-height: 220px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    transition: transform 0.3s ease;
}
.step-box:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.step-number {
    background-color: #ec4899;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 18px;
    line-height: 40px;
    margin: 0 auto 15px auto;
}
.step-title {
    font-weight: 600;
    font-size: 18px;
    color: #1e293b;
    margin-bottom: 10px;
}
.step-desc {
    font-size: 14px;
    color: #475569;
}
</style>
<div class="how-to-use-container">
    <div class="how-to-use-title">How to use the Translator Tool?</div>
    <div class="how-to-use-subtitle">Follow these five easy steps to translate text from any image</div>
    <div class="how-to-use-steps">
        <div class="step-box">
            <div class="step-number">1</div>
            <div class="step-title">Add Image</div>
            <div class="step-desc">Begin by navigating to the OCR + Translate section in the app.</div>
        </div>
        <div class="step-box">
            <div class="step-number">2</div>
            <div class="step-title">Upload or Capture</div>
            <div class="step-desc">Upload one or more images or use your device's camera to capture live input.</div>
        </div>
        <div class="step-box">
            <div class="step-number">3</div>
            <div class="step-title">Choose Language</div>
            <div class="step-desc">Pick the source and target languages from over 70 supported options.</div>
        </div>
        <div class="step-box">
            <div class="step-number">4</div>
            <div class="step-title">Translate</div>
            <div class="step-desc">The app will detect, extract, and translate the text automatically using AI.</div>
        </div>
        <div class="step-box">
            <div class="step-number">5</div>
            <div class="step-title">Listen</div>
            <div class="step-desc">Click the “🔊 Listen” button to hear the translated content aloud.</div>
        </div>
    </div>
</div>

""", unsafe_allow_html=True)



    st.markdown("""### 🌐 Supported Languages:
""")

    # Your language dictionary
    lang_dict = {
        # Latin Scripts
        'English': 'en', 'French': 'fr', 'German': 'de', 'Spanish': 'es', 'Italian': 'it', 'Dutch': 'nl',
        'Danish': 'da', 'Turkish': 'tr', 'Czech': 'cs', 'Hungarian': 'hu', 'Finnish': 'fi', 'Polish': 'pl',
        'Romanian': 'ro', 'Indonesian': 'id', 'Vietnamese': 'vi', 'Malay': 'ms', 'Afrikaans': 'af',
        'Icelandic': 'is', 'Slovak': 'sk', 'Slovenian': 'sl', 'Albanian': 'sq', 'Lithuanian': 'lt',
        'Latvian': 'lv', 'Welsh': 'cy', 'Irish': 'ga', 'Bosnian': 'bs', 'Estonian': 'et', 'Swahili': 'sw',
        'Uzbek': 'uz', 'Filipino': 'tl', 'Azerbaijani': 'az', 'Kurdish': 'ku', 'Latin': 'la', 'Maltese': 'mt',
        'Maori': 'mi', 'Occitan': 'oc', 'Pijin': 'pi',

        # Devanagari & Indic
        'Hindi': 'hi', 'Marathi': 'mr', 'Tamil': 'ta', 'Telugu': 'te', 'Kannada': 'kn', 'Nepali': 'ne',
        'Sanskrit': 'sa', 'Maithili': 'mai', 'Magahi': 'mah', 'Awadhi': 'ang', 'Newari': 'new', 'Konkani': 'gom',
        'Chhattisgarhi': 'sck', 'Assamese': 'as', 'Manipuri': 'mni', 'Bengali': 'bn',

        # Arabic Scripts
        'Arabic': 'ar', 'Persian': 'fa', 'Urdu': 'ur', 'Uyghur': 'ug',

        # Cyrillic
        'Russian': 'ru', 'Ukrainian': 'uk', 'Bulgarian': 'bg', 'Belarusian': 'be', 'Mongolian (Cyrillic)': 'mn',
        'Serbian (Cyrillic)': 'rs_cyrillic',

        # Asian
        'Japanese': 'ja', 'Korean': 'ko', 
    }

    st.markdown(f"✅ **Total Languages Supported:** {len(lang_dict)}\n\n")

    # Display languages in cards (3 per row)
    lang_names = list(lang_dict.keys())
    cols = st.columns(3)
    for idx, lang in enumerate(lang_names):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style="background-color: #262730; padding: 10px 15px; border-radius: 8px;
                        margin-bottom: 10px; color: white; text-align: center;">
                {lang}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
### 📬 Contact Us:
For support or suggestions, reach us at:  
https://github.com/anushkashinde123/Image-Based-Text-Extraction-and-Translation
""")
   

elif feature == "📖 Dictionary":
    st.markdown("""
        <style>
            .dict-header {
                background: linear-gradient(to right, #00b09b, #96c93d);
                padding: 2rem;
                border-radius: 12px;
                color: white;
                text-align: center;
                margin-bottom: 30px;
            }
            .dict-header h2 {
                font-size: 2.2rem;
                margin-bottom: 0.5rem;
            }
            .dict-header p {
                font-size: 1.1rem;
                margin-top: 0;
            }
            .dict-container {
                background: #f5f7fa;
                padding: 2rem;
                border-radius: 12px;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            }
            .dict-label {
                font-weight: 600;
                font-size: 1.1rem;
                margin-top: 1rem;
                color: #333;
            }
            .dict-translation {
                background: #e8f0fe;
                padding: 1rem;
                border-radius: 8px;
                font-size: 1.3rem;
                font-weight: bold;
                color: #1a73e8;
                margin-top: 1rem;
            }
            .stTextInput > div > input {
                border-radius: 10px;
                padding: 0.5rem 1rem;
                font-size: 1.1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="dict-header">
            <h2>📘 Multilingual Dictionary</h2>
            <p>Find quick word translations in over 70 languages with one click</p>
        </div>
    """, unsafe_allow_html=True)

    # st.markdown('<div class="dict-container">', unsafe_allow_html=True)

    word = st.text_input("🔍 Enter a word or short sentence:")
    src = st.selectbox("From Language", lang_names, index=0, key="dict_src")
    tgt = st.selectbox("To Language", lang_names, index=1, key="dict_tgt")

    if st.button("Translate"):
        try:
            translated_word = GoogleTranslator(source=lang_dict[src], target=lang_dict[tgt]).translate(word)
            st.markdown(f"<div class='dict-translation'>📘 {translated_word}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Translation error: {e}")

    st.markdown('</div>', unsafe_allow_html=True)


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
