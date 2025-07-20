# Speechtotext-using-gemini
This app:

Accepts microphone input

Converts the audio to a Gemini-compatible format

Transcribes it using Gemini API

✅ Requirements

Install dependencies in your environment:
```
pip install streamlit librosa soundfile google-generativeai
```

---

✅ To Run

```
streamlit run app.py
```

---

Notes

This app assumes your audio input is WAV format. Most browsers support .wav from mic.

If using MP3 or other formats, you might need FFmpeg or an extended conversion method.

google-generativeai is the SDK used for Gemini interaction. Make sure your key supports the model.
