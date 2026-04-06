import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def speech_to_text(audio_file_path: str, language: str = "ar") -> str:
    if language not in ["ar", "en"]:
        raise ValueError("Unsupported language. Only 'ar' and 'en' are supported.")
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(audio_file_path, file.read()),
                model="whisper-large-v3-turbo",
                language=language,
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"
