from gtts import gTTS

def text_to_speech(text: str, language: str = "ar", output_file: str = "output.mp3") -> str:
    """
    Converts text to speech.
    Only supports Arabic ('ar') and English ('en').
    Returns the path to the saved audio file.
    """
    if language not in ["ar", "en"]:
        raise ValueError("Unsupported language. Only 'ar' and 'en' are supported.")

    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(output_file)
    return output_file