from gtts import gTTS
import tempfile

def text_to_speech(text: str, language: str = "ar") -> str:
    if language not in ["ar", "en"]:
        raise ValueError("Unsupported language. Only 'ar' and 'en' are supported.")
    tts = gTTS(text=text, lang=language, slow=False)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name
