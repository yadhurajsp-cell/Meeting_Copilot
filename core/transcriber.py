import whisper
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL" , "small") 

_model = None

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL" , "saraas:v2.5")

def load_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {_model}")
        _model = whisper.load_model(WHISPER_MODEL)
    return _model

def transcribe_chunk(chunk_path: str) -> str:
    model = load_model()

   

    result = model.transcribe(
        chunk_path
    )

    return result["text"]

def transcribe_all(chunks: list ) -> str:
    full_transcription = ""
    for i , chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}")          
        transcription = transcribe_chunk(chunk)
        full_transcription += transcription + " "
    return full_transcription