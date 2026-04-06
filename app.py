import streamlit as st
from model.LLM_groq import GroqModel
from model.tts import text_to_speech
from model.stt import speech_to_text
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

st.set_page_config(page_title="Uni-Assistant", page_icon="🎓")
st.title("🎓 University Student Assistant")
st.caption("I answer questions based on official university rules.")

if "bot" not in st.session_state:
    st.session_state.bot = GroqModel()

with st.sidebar:
    st.header("Settings")
    st.subheader("🌐 Language")
    language_label = st.radio("Select Language", options=["Arabic", "English"], index=0)
    language_code = "ar" if language_label == "Arabic" else "en"
    st.subheader("🔊 Text-to-Speech")
    tts_enabled = st.toggle("Enable Voice Responses", value=False)
    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.bot.clear_history()
        st.rerun()

for message in st.session_state.bot.conversation_history[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.subheader("🎙️ Voice Input")
audio_input = st.audio_input("Record your question")

if audio_input:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_audio:
        tmp_audio.write(audio_input.read())
        tmp_audio_path = tmp_audio.name
    with st.spinner("Transcribing your voice..."):
        transcribed_text = speech_to_text(tmp_audio_path, language=language_code)
    os.unlink(tmp_audio_path)
    st.success(f"📝 Transcribed: *{transcribed_text}*")
    with st.chat_message("user"):
        st.markdown(transcribed_text)
    with st.chat_message("assistant"):
        with st.spinner("Checking university rules..."):
            try:
                response = st.session_state.bot.chat(transcribed_text)
            except Exception as e:
                response = f"An error occurred: {str(e)}"
            st.markdown(response)
            if tts_enabled:
                with st.spinner("Generating voice response..."):
                    try:
                        audio_path = text_to_speech(response, language=language_code)
                        st.audio(audio_path, autoplay=True)
                    except Exception as e:
                        st.error(f"Error generating audio: {str(e)}")

st.subheader("⌨️ Text Input")
if prompt := st.chat_input("How can I help you today?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Checking university rules..."):
            try:
                response = st.session_state.bot.chat(prompt)
            except Exception as e:
                response = f"An error occurred: {str(e)}"
            st.markdown(response)
            if tts_enabled:
                with st.spinner("Generating voice response..."):
                    try:
                        audio_path = text_to_speech(response, language=language_code)
                        st.audio(audio_path, autoplay=True)
                    except Exception as e:
                        st.error(f"Error generating audio: {str(e)}")
