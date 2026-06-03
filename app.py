from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from core.rag import ask_question
from main import run_pipeline


load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent
DOWNLOAD_DIR = PROJECT_ROOT / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)


st.set_page_config(page_title="Video Agent", layout="wide")
st.title("Video Agent")

with st.sidebar:
    st.header("Input")
    input_mode = st.radio("Source", ["YouTube URL", "Local file"], horizontal=True)

    source = ""
    uploaded_file = None
    if input_mode == "YouTube URL":
        source = st.text_input(
            "YouTube URL",
            placeholder="https://youtu.be/X5gAG13OM5I?si=MJ7fB90B6GXP13bW",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload audio or video",
            type=["mp3", "mp4", "m4a", "wav", "webm", "mov"],
        )

    run_button = st.button("Process", type="primary", use_container_width=True)


def save_uploaded_file(uploaded):
    target = DOWNLOAD_DIR / uploaded.name
    with target.open("wb") as file:
        file.write(uploaded.getbuffer())
    return str(target)


if "result" not in st.session_state:
    st.session_state.result = None

if "messages" not in st.session_state:
    st.session_state.messages = []


if run_button:
    try:
        if input_mode == "YouTube URL":
            if not source.strip():
                st.warning("Paste a YouTube URL first.")
                st.stop()
            pipeline_source = source.strip()
        else:
            if uploaded_file is None:
                st.warning("Upload a file first.")
                st.stop()
            pipeline_source = save_uploaded_file(uploaded_file)

        with st.spinner("Processing video. This can take a few minutes..."):
            st.session_state.result = run_pipeline(pipeline_source)
            st.session_state.messages = []

        st.success("Processing complete.")
    except Exception as exc:
        st.error("The app hit an error while processing.")
        st.exception(exc)


result = st.session_state.result

if result is None:
    st.info("Choose a YouTube URL or upload a file, then click Process.")
else:
    st.subheader(result["title"])

    tab_summary, tab_decisions, tab_chat = st.tabs(
        ["Summary", "Decisions & Questions", "Chat"]
    )

    with tab_summary:
        st.markdown(result["summary"])

    with tab_decisions:
        left, right = st.columns(2)
        with left:
            st.markdown("### Key Decisions")
            st.markdown(result["decisions"])
        with right:
            st.markdown("### Open Questions")
            st.markdown(result["questions"])

    with tab_chat:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        question = st.chat_input("Ask about the video")
        if question:
            st.session_state.messages.append({"role": "user", "content": question})
            with st.chat_message("user"):
                st.markdown(question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = ask_question(result["rag_chain"], question)
                st.markdown(answer)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
