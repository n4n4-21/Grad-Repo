import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def speech_to_text(audio_file_path: str, language: str = "ar") -> str:
    """
    Transcribes an audio file to text using Groq's Whisper model.
    Only supports Arabic ('ar') and English ('en').
    Returns the transcribed text.
    """
    if language not in ["ar", "en"]:
        raise ValueError("Unsupported language. Only 'ar' and 'en' are supported.")

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    with open(audio_file_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(audio_file_path, file.read()),
            model="whisper-large-v3-turbo",
            language=language,  # ← explicitly set the language
            response_format="text"
        )

    return transcription