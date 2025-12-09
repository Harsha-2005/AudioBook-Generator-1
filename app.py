import streamlit as st
from io import BytesIO
from core.extractor import extract_texts
from openai import OpenAI
from gtts import gTTS

st.set_page_config(page_title="AI Audiobook Generator", page_icon="🎧")
st.title("🎧 AI Audiobook Generator")
st.write(
    "Upload PDF, DOCX or TXT files, extract the text, rewrite it using an LLM, "
    "and generate an audiobook MP3."
)

# Global store for generated text
if "llm_output" not in st.session_state:
    st.session_state.llm_output = ""


def llm_rewrite(text, api_key):
    client = OpenAI(api_key=api_key)

    prompt = (
        "Rewrite the following document text into a clear, natural, audiobook-style narration. "
        "Keep all important information.\n\n"
        f"{text}"
    )

    result = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return result.choices[0].message.content.strip()


uploaded_files = st.file_uploader(
    "Upload one or more files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

if uploaded_files:
    extracted_text = extract_texts(uploaded_files)

    st.subheader("📄 Extracted Text")
    st.text_area("Preview", extracted_text, height=250)

    st.subheader("🧠 LLM Audiobook Rewriting")
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

    if st.button("Rewrite using AI"):
        if not api_key:
            st.error("Please enter your API key.")
        else:
            with st.spinner("Generating audiobook-style content..."):
                try:
                    st.session_state.llm_output = llm_rewrite(extracted_text, api_key)
                    st.success("LLM text ready!")
                except Exception as e:
                    st.error(f"LLM Error: {e}")

if st.session_state.llm_output:
    st.subheader("✨ AI-Generated Audiobook Text")
    st.text_area("Output", st.session_state.llm_output, height=250)

    st.subheader("🔊 Convert to Audio (MP3)")
    
    if st.button("Generate MP3"):
        try:
            tts = gTTS(st.session_state.llm_output)
            audio_data = BytesIO()
            tts.write_to_fp(audio_data)
            audio_data.seek(0)

            st.audio(audio_data, format="audio/mp3")

            st.download_button(
                label="Download MP3",
                data=audio_data,
                file_name="audiobook.mp3",
                mime="audio/mp3",
            )
            st.success("MP3 generated successfully!")
        except Exception as e:
            st.error(f"Audio error: {e}")

else:
    st.info("Upload a file and rewrite text first.")
