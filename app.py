import streamlit as st
from pathlib import Path
from typing import List

from core.extractor import extract_texts
from openai import OpenAI


st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")

st.title("🎧 AI Audiobook Generator")
st.write(
    "Upload PDF, DOCX or TXT files, extract the text, and optionally rewrite it "
    "into audiobook-style narration using an LLM."
)


def generate_llm_audiobook_text(text: str, api_key: str) -> str:
    """
    Use an LLM (OpenAI) to rewrite the extracted text as audiobook-style narration.
    """
    client = OpenAI(api_key=api_key)

    prompt = (
        "You are an expert audiobook narrator. Rewrite the following document text "
        "into clear, natural, audiobook-style narration. "
        "Keep all important information, but make it engaging and easy to follow.\n\n"
        f"Document text:\n{text}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or the model your mentor specifies
        messages=[
            {
                "role": "system",
                "content": "You rewrite text into engaging audiobook-style narration.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()


# ------------- File Upload & Extraction ------------- #

uploaded_files = st.file_uploader(
    "Upload one or more files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    st.subheader("📄 Extracted Text")

    # extract_texts returns ONE big string with headings per file
    extracted_text = extract_texts(uploaded_files)
    st.text_area("Extracted text preview", extracted_text, height=300)

    # ------------- LLM Audiobook-Style Rewriting ------------- #
    st.subheader("🧠 LLM Audiobook-style Rewriting")

    api_key = st.text_input(
        "Enter your OpenAI API key (kept only in this session)", type="password"
    )

    if st.button("Generate audiobook-style text with LLM"):
        if not api_key:
            st.error("Please enter your OpenAI API key first.")
        elif not extracted_text.strip():
            st.error("Please upload a file so there is text to rewrite.")
        else:
            with st.spinner("Calling LLM to rewrite text..."):
                try:
                    llm_output = generate_llm_audiobook_text(extracted_text, api_key)
                    st.success("LLM audiobook-style text generated.")
                    st.text_area(
                        "LLM-generated audiobook-style text",
                        llm_output,
                        height=300,
                    )
                except Exception as e:
                    st.error(
                        f"Error while calling the LLM. "
                        f"Check your API key / internet connection. Details: {e}"
                    )

    # ------------- Audio (Future Work) ------------- #
    st.subheader("🔊 Audio Generation (Future Work)")
    st.info(
        "On this laptop, online text-to-speech (TTS) is unstable, "
        "so audio generation is disabled to keep the app stable.\n\n"
        "However, the code structure supports taking the LLM-generated audiobook text "
        "and sending it to any TTS API in the future."
    )

else:
    st.warning("📌 Please upload at least one file to start.")
