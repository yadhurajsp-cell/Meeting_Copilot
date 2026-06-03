from dotenv import load_dotenv

from core.extractor import extract_key_decisions, extract_questions
from core.rag import ask_question, build_rag
from core.summarise import generate_title, summarise
from core.transcriber import transcribe_all
from utils.audio import process_input


load_dotenv()


def run_pipeline(source):
    chunks = process_input(source)
    transcription = transcribe_all(chunks)
    print("Full Transcription:")
    print(transcription)

    summary = summarise(transcription)
    print("\nSummary:")
    print(summary)

    title = generate_title(transcription)
    print("\nGenerated Title:")
    print(title)

    decisions = extract_key_decisions(transcription)
    questions = extract_questions(transcription)
    print("\nKey Decisions:")
    print(decisions)
    print("\nOpen Questions:")
    print(questions)

    rag_chain = build_rag(transcription)

    return {
        "title": title,
        "summary": summary,
        "decisions": decisions,
        "questions": questions,
        "rag_chain": rag_chain,
    }


if __name__ == "__main__":
    source = input("Enter YouTube URL or local file path: ")
    result = run_pipeline(source)
    print("\nYou can now ask questions based on the video content.")

    print("\n" + "=" * 60)
    print(f"Title: {result['title']}")
    print(f"\nSummary:\n{result['summary']}")
    print(f"\nKey Decisions:\n{result['decisions']}")
    print(f"\nOpen Questions:\n{result['questions']}")
    print("=" * 60)

    print("\nChat with your meeting (type 'exit' to quit)\n")
    rag_chain = result["rag_chain"]
    while True:
        question = input("You: ").strip()
        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        if not question:
            continue
        answer = ask_question(rag_chain, question)
        print(f"\nAssistant: {answer}\n")
