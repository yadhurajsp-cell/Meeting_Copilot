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

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Install FFmpeg and make sure it is available on PATH:

```powershell
winget install Gyan.FFmpeg
```

Restart the terminal after installing FFmpeg.

4. Create `.env` from `.env.example` and fill in your keys:

```powershell
copy .env.example .env
```

Required for summarization, extraction, and chat:

```text
MISTRAL_API_KEY=
```

Optional:

```text
WHISPER_MODEL=small
SARVAM_API_KEY=
SARVAM_STT_MODEL=saraas:v2.5
HUGGINGFACEHUB_API_TOKEN=
```

## Run the Streamlit App

```powershell
streamlit run app.py
```

## Run the CLI Pipeline

```powershell
python main.py
```

Then paste a YouTube URL or local file path when prompted.

## Notes

- The first Whisper run may download model weights and take longer.
- Large audio/video outputs are ignored by Git to keep the repository small.
- Never commit your `.env` file or API keys.
