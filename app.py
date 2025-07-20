import streamlit as st
import librosa
import soundfile as sf
import tempfile
import os
from io import BytesIO
from google.generativeai import configure, GenerativeModel
from utils import convert_to_supported_format, transcribe_audio_with_gemini
from dotenv import load_dotenv

# Load from .env file into environment
load_dotenv()

# Fetch the key
gemini_key = os.getenv("GEMINI_API_KEY")

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🎙️ Gemini Audio Transcriber", layout="centered")

st.title("🎙️ Gemini Audio Transcriber")
st.markdown("Record or upload audio to transcribe using **Gemini API**.")

#audio_data = st.audio(label="🎤 Record or Upload Your Audio", format="audio/wav")

# 🎙️ Record from microphone or upload
audio_data = st.audio_input("🎙️ Record your answer")

# Optional playback
if audio_data:
    st.audio(audio_data, format='audio/wav')

if audio_data and gemini_key:
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            result = transcribe_audio_with_gemini(audio_data, gemini_key)

        st.success("Transcription complete!")
        st.markdown("### 📝 Transcribed Text")
        st.text_area("Output", value=result, height=200)

elif not audio_data:
    st.info("Please record or upload an audio file.")
