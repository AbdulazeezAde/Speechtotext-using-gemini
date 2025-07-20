import streamlit as st
import librosa
import soundfile as sf
import tempfile
import os
from io import BytesIO
from google.generativeai import configure, GenerativeModel
from utils import convert_to_supported_format, transcribe_audio_with_gemini

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🎙️ Gemini Audio Transcriber", layout="centered")

st.title("🎙️ Gemini Audio Transcriber")
st.markdown("Record or upload audio to transcribe using **Gemini API**.")

gemini_key = st.text_input("🔑 Enter your Gemini API Key:", type="password")

#audio_data = st.audio(label="🎤 Record or Upload Your Audio", format="audio/wav")
audio_data = st.audio_input("🎙️ Record your answer")
audio_data = st.audio(audio_data, format='audio/wav')

if audio_data and gemini_key:
    with st.spinner("Transcribing..."):
        result = transcribe_audio_with_gemini(audio_data, gemini_key)
        st.success("Transcription complete!")
        st.markdown("### 📝 Transcribed Text")
        st.text_area("Output", value=result, height=200)

elif not audio_data:
    st.info("Please upload or record an audio file.")
