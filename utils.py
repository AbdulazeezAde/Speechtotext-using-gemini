# -------------------------------
# Audio Conversion Function
# -------------------------------
def convert_to_supported_format(audio_data):
    """Convert audio to a format supported by Gemini using librosa"""
    try:
        # Save raw audio data to a temporary WAV file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_input:
            tmp_input.write(audio_data.getvalue())
            tmp_input_path = tmp_input.name
        
        # Load and convert to 16kHz mono
        audio, sr = librosa.load(tmp_input_path, sr=16000, mono=True)

        if len(audio) == 0:
            os.unlink(tmp_input_path)
            return None

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_output:
            sf.write(tmp_output.name, audio, 16000)
            tmp_output_path = tmp_output.name

        os.unlink(tmp_input_path)
        return tmp_output_path

    except Exception as e:
        st.error(f"Audio conversion error: {str(e)}")
        return None

# -------------------------------
# Transcription Function
# -------------------------------
def transcribe_audio_with_gemini(audio_data, gemini_key):
    """Transcribe audio using Gemini API"""
    try:
        if not gemini_key:
            return "Please provide Gemini API key for speech transcription."

        # Initialize Gemini client once
        if "gemini_client" not in st.session_state:
            try:
                configure(api_key=gemini_key)
                st.session_state.gemini_client = GenerativeModel("models/gemini-1.5-pro-latest")
            except Exception as init_error:
                return f"Failed to initialize Gemini client: {str(init_error)}"

        # Convert audio
        audio_file_path = convert_to_supported_format(audio_data)
        if not audio_file_path:
            return "Failed to convert audio to supported format."

        with open(audio_file_path, 'rb') as f:
            audio_bytes = f.read()

        prompt = """
        Please transcribe this audio recording accurately. 
        Return only the transcribed text without any additional commentary or formatting.
        If no speech is detected, return "No speech detected in recording."
        """

        response = st.session_state.gemini_client.generate_content([
            prompt,
            {"mime_type": "audio/wav", "data": audio_bytes}
        ])

        os.unlink(audio_file_path)

        transcribed_text = response.text.strip()
        return transcribed_text if transcribed_text else "No speech detected in recording."

    except Exception as e:
        return f"Transcription error: {str(e)}"
