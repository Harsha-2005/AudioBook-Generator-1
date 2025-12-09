import streamlit as st
from io import BytesIO
from pathlib import Path
from core.extractor import extract_texts

st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")

st.title("🎧 AI Audiobook Generator")
st.write("Upload PDF, DOCX or TXT files and extract text")

uploaded_files = st.file_uploader(
    "Upload one or more files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    st.subheader("📄 Extracted Text")

    extracted_text = extract_texts(uploaded_files)
    st.text_area("Extracted text preview", extracted_text, height=300)

    st.subheader("🔊 Audio Generation")
    st.info("""
On this laptop, online text-to-speech (TTS) is unstable,
so audio generation is disabled to keep the app stable.

However, the code structure supports converting the audiobook text to audio
using a TTS service (like gTTS or another API) and offering it as a downloadable file.
    """)

else:
    st.warning("📌 Please upload at least one file.")
