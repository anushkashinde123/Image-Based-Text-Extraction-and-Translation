# # import streamlit as st
# # import easyocr
# # from PIL import Image
# # import numpy as np
# # from deep_translator import GoogleTranslator
# # from gtts import gTTS
# # import base64
# # import os
# # import io



# # # ========== Styling ==========
# # st.markdown("""
# #     <style>
# #         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
# #         body {
# #             font-family: 'Poppins', sans-serif;
# #             background: linear-gradient(135deg, #eef2f3, #dfe9f3);
# #         }
# #         .main-container {
# #             background-color: white;
# #             padding: 30px;
# #             border-radius: 12px;
# #             box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
# #             max-width: 700px;
# #             margin: auto;
# #         }
# #         .stButton>button {
# #             background-color: #0056b3;
# #             color: white;
# #             border-radius: 8px;
# #             padding: 8px 16px;
# #             font-size: 14px;
# #             font-weight: bold;
# #             transition: background-color 0.3s, transform 0.1s;
# #             display: block;
# #             margin: 10px auto;
# #             width: auto;
# #         }
# #         .stButton>button:hover {
# #             background-color: #003f7f;
# #             transform: scale(1.05);
# #         }
# #         h1, h2, h3 {
# #             color: #2c3e50;
# #             text-align: center;
# #         }
# #         .text-box {
# #             background-color: #f8f9fa;
# #             border: 2px solid #0056b3;
# #             padding: 15px;
# #             border-radius: 10px;
# #             margin-top: 15px;
# #             font-size: 16px;
# #             font-weight: 500;
# #             color: #333;
# #             white-space: pre-wrap;
# #             word-wrap: break-word;
# #             box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
# #             max-width: 90%;
# #             margin-left: auto;
# #             margin-right: auto;
# #         }
# #     </style>
# # """, unsafe_allow_html=True)

# # st.markdown("<div class='main-container'>", unsafe_allow_html=True)

# # # ========== Title ==========
# # st.title("📷 Text Extraction & Translation App")


# # # ========== Initialize Session State ==========
# # if "translation_history" not in st.session_state:
# #     st.session_state.translation_history = []

# # if "show_history" not in st.session_state:
# #     st.session_state.show_history = False
# # if "show_camera" not in st.session_state:
# #     st.session_state["show_camera"] = False
# # # ========== Language Options ==========
# # lang_options = {
# #     "English": "en", "Marathi": "mr", "Kannada": "kn", "Hindi": "hi",
# #     "Korean": "ko", "Japanese": "ja", "Chinese": "ch_sim"
# # }
# # selected_langs = st.sidebar.multiselect("Select Input Languages:", list(lang_options.keys()), default=["English"])
# # lang_list = [lang_options[lang] for lang in selected_langs]
# # target_lang = st.sidebar.selectbox("Choose Translation Language:", list(lang_options.keys()), index=0)
# # target_lang_code = lang_options[target_lang]


# # # Toggle History
# # if st.sidebar.button("📜 View History"):
# #     st.session_state.show_history = not st.session_state.show_history

# # if st.sidebar.button("🗑️ Clear History"):
# #     st.session_state.translation_history.clear()

# # # ========== EasyOCR Reader ==========
# # reader = easyocr.Reader(lang_list, gpu=False)  # Use CPU

# # # ========== Utility Functions ==========
# # def resize_image(image, max_size=800):
# #     """Resize image to a reasonable size to speed up OCR."""
# #     w, h = image.size
# #     scale = max_size / max(w, h)
# #     new_size = (int(w * scale), int(h * scale)) if scale < 1 else (w, h)
# #     return image.resize(new_size, Image.LANCZOS)

# # def text_to_speech(text, lang="en"):
# #     """Convert text to speech and return audio bytes."""
# #     tts = gTTS(text=text, lang=lang)
# #     audio_file = f"translation_audio_{lang}.mp3"
# #     tts.save(audio_file)
# #     with open(audio_file, "rb") as f:
# #         audio_bytes = f.read()
# #     os.remove(audio_file)
# #     return audio_bytes

# # def process_image_from_bytes(image_bytes, image_index):
# #     try:
# #         image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
# #         image = resize_image(image)
# #         st.image(image, caption=f"Processed Image {image_index + 1}", use_column_width=True)

# #         st.write("🔍 Extracting text...")
# #         image_array = np.array(image)
# #         result = reader.readtext(image_array)
# #         detected_texts = [d[1] for d in result]

# #         if detected_texts:
# #             st.subheader("📝 Detected Text:")
# #             text_block = "\n".join(detected_texts)
# #             st.markdown(f"<div class='text-box'>{text_block}</div>", unsafe_allow_html=True)

# #             if st.button(f"🌍 Translate Image {image_index + 1}", key=f"translate_{image_index}"):
# #                 st.subheader("📖 Translated Text:")
# #                 translated_texts = [GoogleTranslator(source='auto', target=target_lang_code).translate(t) for t in detected_texts]
# #                 translated_text_block = "\n".join(translated_texts)
# #                 st.markdown(f"<div class='text-box'>{translated_text_block}</div>", unsafe_allow_html=True)
# #                 audio_bytes = text_to_speech(translated_text_block, target_lang_code)
# #                 st.audio(audio_bytes, format="audio/mp3")

# #                  # Save to history
# #                 st.session_state.translation_history.append({
# #                     "source": text_block,
# #                     "translated": translated_text_block,
# #                     "type": f"Image {image_index + 1}"
# #                 })
# #         else:
# #             st.warning("⚠ No text detected.")
# #     except Exception as e:
# #         st.error(f"❌ Failed to process image: {e}")

# # # ========== File Upload ==========
# # if not st.session_state.show_history:
# #     uploaded_files = st.file_uploader("Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# #     if uploaded_files:
# #         for idx, file in enumerate(uploaded_files):
# #             process_image_from_bytes(file.read(), idx)

# # # ========== Take Photo Button & Camera ==========
# #     if "show_camera" not in st.session_state:
# #         st.session_state["show_camera"] = False

# #     if st.button("📷 Take Photo"):
# #         st.session_state["show_camera"] = True

# #     if st.session_state["show_camera"]:
# #         camera_image = st.camera_input("Capture your image")
# #         if camera_image is not None:
# #             st.session_state["show_camera"] = False
# #             process_image_from_bytes(camera_image.getvalue(), 0)

# #     st.markdown("</div>", unsafe_allow_html=True)

# #     # ========== Dictionary Feature ==========
# #     st.subheader("📚 Dictionary Translation")
# #     word_input = st.text_input("Enter a word or phrase to translate:")

# #     if word_input:
# #         try:
# #             translated_word = GoogleTranslator(source='auto', target=target_lang_code).translate(word_input)
# #             st.markdown(f"<div class='text-box'><strong>Translated:</strong><br>{translated_word}</div>", unsafe_allow_html=True)

# #             if st.button("🔊 Hear Translation"):
# #                 audio_bytes = text_to_speech(translated_word, target_lang_code)
# #                 st.audio(audio_bytes, format="audio/mp3")

# #                 st.session_state.translation_history.append({
# #                     "source": word_input,
# #                     "translated": translated_word,
# #                     "type": "Dictionary"
# #                 })
# #         except Exception as e:
# #             st.error(f"❌ Failed to translate: {e}")



# # # ========== Translation History ==========
# # if st.session_state.show_history:
# #     st.subheader("📜 Translation History")
# #     if st.session_state.translation_history:
# #         for idx, item in enumerate(reversed(st.session_state.translation_history)):
# #             st.markdown(f"""
# #             <div class='text-box'>
# #                 <strong>{item['type']}</strong><br>
# #                 <strong>Original:</strong> {item['source']}<br>
# #                 <strong>Translated:</strong> {item['translated']}
# #             </div>
# #             """, unsafe_allow_html=True)
# #     else:
# #         st.info("No history available yet.")



# import streamlit as st
# import easyocr
# from PIL import Image
# import numpy as np
# from deep_translator import GoogleTranslator
# from gtts import gTTS
# import base64
# import os
# import io

# # ========== Styling ==========
# st.markdown("""
#     <style>
#         @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
#         body {
#             font-family: 'Poppins', sans-serif;
#             background: linear-gradient(135deg, #eef2f3, #dfe9f3);
#         }
#         .main-container {
#             background-color: white;
#             padding: 30px;
#             border-radius: 12px;
#             box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.1);
#             max-width: 700px;
#             margin: auto;
#         }
#         .stButton>button {
#             background-color: #0056b3;
#             color: white;
#             border-radius: 8px;
#             padding: 8px 16px;
#             font-size: 14px;
#             font-weight: bold;
#             transition: background-color 0.3s, transform 0.1s;
#             display: block;
#             margin: 10px auto;
#             width: auto;
#         }
#         .stButton>button:hover {
#             background-color: #003f7f;
#             transform: scale(1.05);
#         }
#         h1, h2, h3 {
#             color: #2c3e50;
#             text-align: center;
#         }
#         .text-box {
#             background-color: #f8f9fa;
#             border: 2px solid #0056b3;
#             padding: 15px;
#             border-radius: 10px;
#             margin-top: 15px;
#             font-size: 16px;
#             font-weight: 500;
#             color: #333;
#             white-space: pre-wrap;
#             word-wrap: break-word;
#             box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
#             max-width: 90%;
#             margin-left: auto;
#             margin-right: auto;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ========== Title ==========
# st.title("📷 Text Extraction & Translation App")

# # ========== Initialize Session State ==========
# if "translation_history" not in st.session_state:
#     st.session_state.translation_history = []

# if "show_history" not in st.session_state:
#     st.session_state.show_history = False

# if "show_camera" not in st.session_state:
#     st.session_state["show_camera"] = False

# if "show_dictionary" not in st.session_state:
#     st.session_state.show_dictionary = False

# # ========== Language Options ==========
# lang_options = {
#     "English": "en", "Marathi": "mr", "Kannada": "kn", "Hindi": "hi",
#     "Korean": "ko", "Japanese": "ja", "Chinese": "ch_sim"
# }
# selected_langs = st.sidebar.multiselect("Select Input Languages:", list(lang_options.keys()), default=["English"])
# lang_list = [lang_options[lang] for lang in selected_langs]
# target_lang = st.sidebar.selectbox("Choose Translation Language:", list(lang_options.keys()), index=0)
# target_lang_code = lang_options[target_lang]

# # Toggle History
# if st.sidebar.button("📜 View History"):
#     st.session_state.show_history = not st.session_state.show_history

# if st.sidebar.button("🗑️ Clear History"):
#     st.session_state.translation_history.clear()

# if st.sidebar.button("📚 Toggle Dictionary Translation"):
#     st.session_state.show_dictionary = not st.session_state.show_dictionary

# # ========== EasyOCR Reader ==========
# reader = easyocr.Reader(lang_list, gpu=False)  # Use CPU

# # ========== Utility Functions ==========
# def resize_image(image, max_size=800):
#     """Resize image to a reasonable size to speed up OCR."""
#     w, h = image.size
#     scale = max_size / max(w, h)
#     new_size = (int(w * scale), int(h * scale)) if scale < 1 else (w, h)
#     return image.resize(new_size, Image.LANCZOS)

# def text_to_speech(text, lang="en"):
#     """Convert text to speech and return audio bytes."""
#     tts = gTTS(text=text, lang=lang)
#     audio_file = f"translation_audio_{lang}.mp3"
#     tts.save(audio_file)
#     with open(audio_file, "rb") as f:
#         audio_bytes = f.read()
#     os.remove(audio_file)
#     return audio_bytes

# def process_image_from_bytes(image_bytes, image_index):
#     try:
#         image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
#         image = resize_image(image)
#         st.image(image, caption=f"Processed Image {image_index + 1}", use_column_width=True)

#         st.write("🔍 Extracting text...")
#         image_array = np.array(image)
#         result = reader.readtext(image_array)
#         detected_texts = [d[1] for d in result]

#         if detected_texts:
#             st.subheader("📝 Detected Text:")
#             text_block = "\n".join(detected_texts)
#             st.markdown(f"<div class='text-box'>{text_block}</div>", unsafe_allow_html=True)

#             if st.button(f"🌍 Translate Image {image_index + 1}", key=f"translate_{image_index}"):
#                 st.subheader("📖 Translated Text:")
#                 translated_texts = [GoogleTranslator(source='auto', target=target_lang_code).translate(t) for t in detected_texts]
#                 translated_text_block = "\n".join(translated_texts)
#                 st.markdown(f"<div class='text-box'>{translated_text_block}</div>", unsafe_allow_html=True)
#                 audio_bytes = text_to_speech(translated_text_block, target_lang_code)
#                 st.audio(audio_bytes, format="audio/mp3")

#                 # Save to history
#                 st.session_state.translation_history.append({
#                     "source": text_block,
#                     "translated": translated_text_block,
#                     "type": f"Image {image_index + 1}"
#                 })
#         else:
#             st.warning("⚠ No text detected.")
#     except Exception as e:
#         st.error(f"❌ Failed to process image: {e}")

# # ========== Dictionary Section (only visible if show_dictionary is True) ==========
# if st.session_state.show_dictionary:
#     st.subheader("📚 Dictionary Translation")
#     word_input = st.text_input("Enter a word or phrase to translate:")

#     if word_input:
#         try:
#             translated_word = GoogleTranslator(source='auto', target=target_lang_code).translate(word_input)
#             st.markdown(f"<div class='text-box'><strong>Translated:</strong><br>{translated_word}</div>", unsafe_allow_html=True)

#             if st.button("🔊 Hear Translation"):
#                 audio_bytes = text_to_speech(translated_word, target_lang_code)
#                 st.audio(audio_bytes, format="audio/mp3")

#                 st.session_state.translation_history.append({
#                     "source": word_input,
#                     "translated": translated_word,
#                     "type": "Dictionary"
#                 })
#         except Exception as e:
#             st.error(f"❌ Failed to translate: {e}")

#     # "Back to Home" button
#     if st.button("🔙 Back to Home"):
#         st.session_state.show_dictionary = False

# # ========== Hide other sections when dictionary is toggled ==========
# if not st.session_state.show_dictionary:
#     # ========== File Upload ==========
#     uploaded_files = st.file_uploader("Upload Image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

#     if uploaded_files:
#         for idx, file in enumerate(uploaded_files):
#             process_image_from_bytes(file.read(), idx)

#     # ========== Take Photo Button & Camera ==========
#     if st.button("📷 Take Photo"):
#         st.session_state["show_camera"] = True

#     if st.session_state["show_camera"]:
#         camera_image = st.camera_input("Capture your image")
#         if camera_image is not None:
#             st.session_state["show_camera"] = False
#             process_image_from_bytes(camera_image.getvalue(), 0)

# # ========== Translation History ==========
# if st.session_state.show_history:
#     st.subheader("📜 Translation History")
#     if st.session_state.translation_history:
#         for idx, item in enumerate(reversed(st.session_state.translation_history)):
#             st.markdown(f"""
#             <div class='text-box'>
#                 <strong>{item['type']}</strong><br>
#                 <strong>Original:</strong> {item['source']}<br>
#                 <strong>Translated:</strong> {item['translated']}
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No history available yet.")


# import streamlit as st
# from PIL import Image
# import easyocr
# from gtts import gTTS
# import os
# import io
# from deep_translator import GoogleTranslator
# import base64

# # Set up page config
# st.set_page_config(page_title="Multilingual OCR Translator", layout="wide")

# # Define supported languages
# lang_dict = {
#     'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr', 'Tamil': 'ta',
#     'Telugu': 'te', 'Kannada': 'kn', 'Gujarati': 'gu', 'Bengali': 'bn',
#     'Punjabi': 'pa', 'Urdu': 'ur'
# }
# lang_names = list(lang_dict.keys())

# # Initialize session states
# if 'history' not in st.session_state:
#     st.session_state.history = []
# if 'selected_feature' not in st.session_state:
#     st.session_state.selected_feature = "📸 OCR + Translate"

# # Sidebar Navigation
# st.sidebar.title("📚 Features")
# feature = st.sidebar.radio("Choose a feature", ["📸 OCR + Translate", "📖 Dictionary", "🕒 History"])
# st.session_state.selected_feature = feature

# # Custom styling
# st.markdown("""
#     <style>
#     .main-title { text-align: center; font-size: 40px; font-weight: bold; color: #4A90E2; }
#     .sub-title { text-align: center; font-size: 20px; margin-bottom: 30px; }
#     .stButton>button { background-color: #4A90E2; color: white; border-radius: 8px; }
#     .stTextInput>div>input { border-radius: 8px; }
#     </style>
# """, unsafe_allow_html=True)

# # Title
# st.markdown('<div class="main-title">🌍 Multilingual OCR Translator</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-title">Capture text, translate it, and listen to it aloud!</div>', unsafe_allow_html=True)

# # ---------- 📸 OCR + Translate Feature ----------
# if feature == "📸 OCR + Translate":
#     col1, col2 = st.columns(2)

#     with col1:
#         input_method = st.radio("Input Method", ["Upload Image", "Use Camera"])
#         image = None
#         if input_method == "Upload Image":
#             uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
#             if uploaded_image:
#                 image = Image.open(uploaded_image)
#         else:
#             camera_image = st.camera_input("Capture Image")
#             if camera_image:
#                 # Convert the bytes to an image using io.BytesIO
#                 image = Image.open(io.BytesIO(camera_image))

#     with col2:
#         source_lang = st.selectbox("Select Source Language (for OCR)", lang_names, index=0)
#         target_lang = st.selectbox("Select Target Language (for Translation)", lang_names, index=1)

#         if image:
#             st.image(image, caption="Uploaded Image", use_container_width=True)
#             with st.spinner("🔍 Extracting text..."):
#                 try:
#                     reader = easyocr.Reader([lang_dict[source_lang]], gpu=False)
#                     result = reader.readtext(image)
#                     extracted_text = " ".join([text[1] for text in result])
#                     st.subheader("📄 Extracted Text")
#                     st.write(extracted_text)

#                     # Translate
#                     translated_text = GoogleTranslator(source=lang_dict[source_lang], target=lang_dict[target_lang]).translate(extracted_text)
#                     st.subheader("🌐 Translated Text")
#                     st.write(translated_text)

#                     # Add to history
#                     st.session_state.history.append({
#                         "original": extracted_text,
#                         "translated": translated_text,
#                         "source_lang": source_lang,
#                         "target_lang": target_lang
#                     })

#                     # TTS
#                     if st.button("🔊 Listen"):
#                         tts = gTTS(text=translated_text, lang=lang_dict[target_lang])
#                         audio_file = "output.mp3"
#                         tts.save(audio_file)
#                         audio_bytes = open(audio_file, "rb").read()
#                         st.audio(audio_bytes, format="audio/mp3")
#                         os.remove(audio_file)

#                 except Exception as e:
#                     st.error(f"❌ Error processing image: {e}")
#         else:
#             st.info("📌 Please upload or capture an image.")


# import streamlit as st
# from PIL import Image
# import easyocr
# from gtts import gTTS
# import os
# import io
# from deep_translator import GoogleTranslator

# # Set up page config
# st.set_page_config(page_title="Multilingual OCR Translator", layout="wide")

# # Define supported languages
# lang_dict = {
#     'English': 'en', 'Hindi': 'hi', 'Marathi': 'mr', 'Tamil': 'ta',
#     'Telugu': 'te', 'Kannada': 'kn', 'Gujarati': 'gu', 'Bengali': 'bn',
#     'Punjabi': 'pa', 'Urdu': 'ur'
# }
# lang_names = list(lang_dict.keys())

# # Initialize session states
# if 'history' not in st.session_state:
#     st.session_state.history = []
# if 'selected_feature' not in st.session_state:
#     st.session_state.selected_feature = "📸 OCR + Translate"

# # Sidebar Navigation
# st.sidebar.title("📚 Features")
# feature = st.sidebar.radio("Choose a feature", ["📸 OCR + Translate", "📖 Dictionary", "🕒 History"])
# st.session_state.selected_feature = feature

# # Custom styling
# st.markdown("""
#     <style>
#     .main-title { text-align: center; font-size: 40px; font-weight: bold; color: #4A90E2; }
#     .sub-title { text-align: center; font-size: 20px; margin-bottom: 30px; }
#     .stButton>button { background-color: #4A90E2; color: white; border-radius: 8px; }
#     .stTextInput>div>input { border-radius: 8px; }
#     </style>
# """, unsafe_allow_html=True)

# # Title
# st.markdown('<div class="main-title">🌍 Multilingual OCR Translator</div>', unsafe_allow_html=True)
# st.markdown('<div class="sub-title">Capture text, translate it, and listen to it aloud!</div>', unsafe_allow_html=True)

# # ---------- 📸 OCR + Translate Feature ----------
# if feature == "📸 OCR + Translate":
#     col1, col2 = st.columns(2)

#     with col1:
#         input_method = st.radio("Input Method", ["Upload Image", "Use Camera"])
#         image = None
#         if input_method == "Upload Image":
#             uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
#             if uploaded_image:
#                 image = Image.open(uploaded_image)
#         else:
#             camera_image = st.camera_input("Capture Image")
#             if camera_image:
#                 # Ensure the image is loaded properly from camera input
#                 image = Image.open(io.BytesIO(camera_image))  # Correct way to handle bytes input

#     with col2:
#         source_lang = st.selectbox("Select Source Language (for OCR)", lang_names, index=0)
#         target_lang = st.selectbox("Select Target Language (for Translation)", lang_names, index=1)

#         if image:
#             st.image(image, caption="Uploaded Image")
#             with st.spinner("🔍 Extracting text..."):
#                 try:
#                     reader = easyocr.Reader([lang_dict[source_lang]], gpu=False)
#                     result = reader.readtext(image)
#                     extracted_text = " ".join([text[1] for text in result])
#                     st.subheader("📄 Extracted Text")
#                     st.write(extracted_text)

#                     # Translate
#                     translated_text = GoogleTranslator(source=lang_dict[source_lang], target=lang_dict[target_lang]).translate(extracted_text)
#                     st.subheader("🌐 Translated Text")
#                     st.write(translated_text)

#                     # Add to history
#                     st.session_state.history.append({
#                         "original": extracted_text,
#                         "translated": translated_text,
#                         "source_lang": source_lang,
#                         "target_lang": target_lang
#                     })

#                     # TTS
#                     if st.button("🔊 Listen"):
#                         tts = gTTS(text=translated_text, lang=lang_dict[target_lang])
#                         audio_file = "output.mp3"
#                         tts.save(audio_file)
#                         audio_bytes = open(audio_file, "rb").read()
#                         st.audio(audio_bytes, format="audio/mp3")
#                         os.remove(audio_file)

#                 except Exception as e:
#                     st.error(f"❌ Error processing image: {e}")
#         else:
#             st.info("📌 Please upload or capture an image.")
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
