# Meeting Copilot

Turn hours of meetings into minutes of insights. Transcribe, summarize, chat, and uncover key decisions with AI.

Meeting Copilot is a Streamlit app that downloads or accepts an audio/video file, transcribes it with Whisper, summarizes the transcript with Mistral, extracts decisions and open questions, and lets you chat with the transcript through a Chroma-backed RAG pipeline.

## Features

- Process a YouTube URL or uploaded local media file
- Convert audio to 16 kHz mono WAV
- Transcribe audio chunks with Whisper
- Generate summary and title
- Extract key decisions and open questions
- Chat with the transcript using LangChain and Chroma

## Project Structure

```text
Meeting_Copilot/
├── app.py                 # Streamlit UI
├── main.py                # CLI pipeline
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── core/
│   ├── extractor.py       # Decisions/questions extraction
│   ├── rag.py             # RAG chain
│   ├── summarise.py       # Summary/title generation
│   ├── transcriber.py     # Whisper transcription
│   └── vectordb.py        # Chroma vector store
└── utils/
    └── audio.py           # Download, conversion, and chunking
```

Generated files are intentionally ignored:

- `downloads/`
- `vector_db/`
- `.venv/`
- `.env`
- Python cache folders









```

Then paste a YouTube URL or local file path when prompted.

## Notes

- The first Whisper run may download model weights and take longer.
- Large audio/video outputs are ignored by Git to keep the repository small.
- Never commit your `.env` file or API keys.
