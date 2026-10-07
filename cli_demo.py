"""
CLI Demo & Theoretical Explanation Script for NLP Text Summarization
Run this file directly via terminal: python cli_demo.py
"""

from summarizer import summarize_text, extractive_summarize, chunk_text

def print_ascii_box(title: str, content: str, width: int = 74):
    """Utility to print clean ASCII boxes in any terminal without unicode errors."""
    top_bot_border = "+" + "-" * (width - 2) + "+"
    print(top_bot_border)
    print("| " + title.center(width - 4) + " |")
    print("+" + "-" * (width - 2) + "+")
    
    for paragraph in content.split("\n"):
        if not paragraph.strip():
            print("| " + " " * (width - 4) + " |")
            continue
        words = paragraph.split(" ")
        line = ""
        for word in words:
            if len(line) + len(word) + 1 <= (width - 4):
                line = (line + " " + word).strip()
            else:
                print("| " + line.ljust(width - 4) + " |")
                line = word
        if line:
            print("| " + line.ljust(width - 4) + " |")
            
    print(top_bot_border)


def summarize_text_demo(text: str, model_type: str = "extractive"):
    """Summarize standard text passage."""
    res = summarize_text(text, model_type=model_type, length_setting="medium")
    return res["summary"]


def summarize_long_text(text: str, max_sentences: int = 4):
    """Summarize long text documents using chunking & TF-IDF sentence scoring."""
    chunks = chunk_text(text, max_words_per_chunk=350)
    summaries = []
    for c in chunks:
        summaries.append(extractive_summarize(c, max_sentences=2))
    
    combined = " ".join(summaries)
    final_summary = extractive_summarize(combined, max_sentences=max_sentences)
    return final_summary


def display_theory_qa():
    """Output answer to 'What is Text Summarization?' for presentations."""
    theory = (
        "Q: WHAT IS TEXT SUMMARIZATION IN NLP?\n"
        "------------------------------------------------------------------\n"
        "Text Summarization is an NLP task of automatically creating a condensed\n"
        "version of a long text document while retaining its key information and\n"
        "semantic meaning.\n\n"
        "TWO MAIN APPROACHES:\n"
        "1. EXTRACTIVE SUMMARIZATION (e.g., TF-IDF / TextRank):\n"
        "   - Selects & extracts key verbatim sentences directly from source text.\n"
        "   - Fast, non-paraphrased, preserves original wording 100%.\n\n"
        "2. ABSTRACTIVE SUMMARIZATION (e.g., DistilBART Transformer):\n"
        "   - Understands semantics using Encoder-Decoder attention neural nets.\n"
        "   - Writes NEW paraphrased sentences similar to human summarizers."
    )
    print_ascii_box("ACADEMIC NLP THEORY: WHAT IS TEXT SUMMARIZATION?", theory, width=74)


if __name__ == "__main__":
    sample_text = (
        "Artificial intelligence (AI) is transforming modern technology and computing. "
        "Natural Language Processing (NLP) is a specialized branch of AI focused on "
        "enabling computers to understand, interpret, and generate human language. "
        "Text summarization is one of the key NLP tasks that compresses long documents "
        "into short, contextually accurate summaries. Traditional extractive models use "
        "TF-IDF statistical scoring to rank sentence importance based on word frequencies. "
        "Modern abstractive models, such as Transformers (BART, T5, GPT), use multi-head "
        "self-attention mechanisms to generate new, human-like paraphrased summaries."
    )

    print("\n" + "=" * 74)
    print(" NLP TEXT SUMMARIZER - TERMINAL & CLI DEMO ".center(74, "="))
    print("=" * 74 + "\n")

    # 1. Standard Summarize Text Demo
    summary_ext = summarize_text_demo(sample_text, model_type="extractive")
    
    print("===== ORIGINAL TEXT =====")
    print(sample_text)
    print("\n===== GENERATED SUMMARY (TF-IDF EXTRACTIVE) =====")
    print(summary_ext)
    print("\n")

    # 2. ASCII Box Formatting Demo
    print_ascii_box("GENERATED SUMMARY (TF-IDF OUTPUT BOX)", summary_ext, width=74)
    print("\n")

    # 3. Long Text Summarize Demo
    long_sample = sample_text * 3
    summary_long = summarize_long_text(long_sample, max_sentences=3)

    print("===== LONG TEXT DEMO =====")
    print(f"Original Word Count: {len(long_sample.split())} words")
    print("\n===== GENERATED LONG TEXT SUMMARY =====")
    print(summary_long)
    print("\n")

    # 4. Display Theory Q&A
    display_theory_qa()
