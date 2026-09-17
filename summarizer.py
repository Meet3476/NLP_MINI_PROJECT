import time
import re
import math
from collections import Counter

# Global cache for transformer model & tokenizer
_model = None
_tokenizer = None
_model_name = "sshleifer/distilbart-cnn-12-6"

def get_transformer_model():
    """Lazy load Hugging Face model & tokenizer for abstractive summarization."""
    global _model, _tokenizer
    if _model is None:
        try:
            from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
            print(f"[*] Loading Transformer Model '{_model_name}'...")
            _tokenizer = AutoTokenizer.from_pretrained(_model_name)
            _model = AutoModelForSeq2SeqLM.from_pretrained(_model_name)
        except Exception as e:
            print(f"[Warning] Failed to load Transformer model ({e}). Extractive mode will be used.")
            _model = False
            _tokenizer = False
    return (_model, _tokenizer) if _model is not False else (None, None)

def split_into_sentences(text: str) -> list[str]:
    """Split text into sentences using regex."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def extractive_summarize(text: str, max_sentences: int = 4) -> str:
    """
    Extractive Summarizer using TF-IDF / Frequency-based sentence scoring.
    Serves as an NLP baseline and offline fallback.
    """
    sentences = split_into_sentences(text)
    if len(sentences) <= max_sentences:
        return text

    # Compute word frequencies
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    stopwords = {
        'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'in', 'to', 'of',
        'for', 'with', 'by', 'as', 'that', 'it', 'this', 'be', 'are', 'was', 'were',
        'from', 'at', 'have', 'has', 'had', 'not', 'but', 'what', 'all', 'were', 'when',
        'we', 'there', 'can', 'an', 'your', 'which', 'their', 'if', 'will', 'each', 'about'
    }
    filtered_words = [w for w in words if w not in stopwords]
    freq = Counter(filtered_words)
    max_freq = max(freq.values()) if freq else 1

    for word in freq:
        freq[word] /= max_freq

    # Score sentences based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        score = 0
        sent_words = re.findall(r'\b[a-zA-Z0-9]+\b', sentence.lower())
        for word in sent_words:
            if word in freq:
                score += freq[word]
        # Normalize score by length to avoid bias toward long sentences
        sentence_scores[sentence] = score / (len(sent_words) + 1)

    # Pick top N sentences preserving original narrative order
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]
    ordered_summary = [s for s in sentences if s in ranked_sentences]
    
    return " ".join(ordered_summary)

def chunk_text(text: str, max_words_per_chunk: int = 450) -> list[str]:
    """Split large text into manageable chunks for Transformer model limit."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += 1
        if current_length >= max_words_per_chunk and word.endswith(('.', '!', '?')):
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks if chunks else [text]

def abstractive_transformer_summarize(text: str, length_setting: str = "medium") -> str:
    """
    Abstractive Summarization using Transformer model (BART/DistilBART).
    """
    model, tokenizer = get_transformer_model()
    if model is None or tokenizer is None:
        return extractive_summarize(text, max_sentences=4)

    # Determine token constraints based on length setting
    length_params = {
        "short": {"max_length": 60, "min_length": 25},
        "medium": {"max_length": 130, "min_length": 50},
        "long": {"max_length": 220, "min_length": 90}
    }
    params = length_params.get(length_setting.lower(), length_params["medium"])

    chunks = chunk_text(text, max_words_per_chunk=400)
    summaries = []

    for chunk in chunks:
        if len(chunk.split()) < 30:
            summaries.append(chunk)
            continue
        try:
            inputs = tokenizer(chunk, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=params["max_length"],
                min_length=params["min_length"],
                no_repeat_ngram_size=3,
                num_beams=4,
                early_stopping=True
            )
            summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary_text)
        except Exception as e:
            print(f"[Transformer Chunk Error] {e}")
            summaries.append(extractive_summarize(chunk, max_sentences=2))

    full_summary = " ".join(summaries)
    
    # If chunked text produced multiple summaries, consolidate if needed
    if len(chunks) > 1 and len(full_summary.split()) > params["max_length"] * 1.5:
        try:
            inputs = tokenizer(full_summary, return_tensors="pt", max_length=1024, truncation=True)
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=params["max_length"],
                min_length=params["min_length"],
                no_repeat_ngram_size=3,
                num_beams=4,
                early_stopping=True
            )
            full_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        except Exception:
            pass

    return full_summary

def calculate_n_gram_overlap(reference: str, hypothesis: str, n: int) -> float:
    """Calculate n-gram recall overlap (ROUGE approximation)."""
    ref_words = re.findall(r'\b\w+\b', reference.lower())
    hyp_words = re.findall(r'\b\w+\b', hypothesis.lower())
    
    if len(ref_words) < n or len(hyp_words) < n:
        return 0.0

    ref_ngrams = Counter([tuple(ref_words[i:i+n]) for i in range(len(ref_words)-n+1)])
    hyp_ngrams = Counter([tuple(hyp_words[i:i+n]) for i in range(len(hyp_words)-n+1)])

    overlap = 0
    for ngram, count in hyp_ngrams.items():
        if ngram in ref_ngrams:
            overlap += min(count, ref_ngrams[ngram])

    total_ref = sum(ref_ngrams.values())
    return (overlap / total_ref * 100) if total_ref > 0 else 0.0

def lcs_length(x: list[str], y: list[str]) -> int:
    """Compute Longest Common Subsequence length for ROUGE-L."""
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]

def calculate_rouge_metrics(original: str, summary: str) -> dict:
    """Calculate ROUGE-1, ROUGE-2, and ROUGE-L scores."""
    r1 = calculate_n_gram_overlap(original, summary, 1)
    r2 = calculate_n_gram_overlap(original, summary, 2)
    
    orig_words = re.findall(r'\b\w+\b', original.lower())
    summ_words = re.findall(r'\b\w+\b', summary.lower())
    
    lcs_val = lcs_length(orig_words[:200], summ_words[:100])
    rl = (lcs_val / len(orig_words[:200]) * 100) if orig_words else 0.0

    return {
        "rouge1": round(r1, 2),
        "rouge2": round(r2, 2),
        "rougeL": round(rl, 2)
    }

def summarize_text(text: str, model_type: str = "transformer", length_setting: str = "medium") -> dict:
    """
    Main summarization entry point. Returns summary text and execution metadata.
    """
    start_time = time.time()

    orig_words = len(re.findall(r'\b\w+\b', text))
    orig_sentences = len(split_into_sentences(text))

    if model_type.lower() == "extractive":
        max_sents = 2 if length_setting == "short" else (4 if length_setting == "medium" else 6)
        summary = extractive_summarize(text, max_sentences=max_sents)
        actual_model = "TF-IDF Extractive Baseline"
    else:
        summary = abstractive_transformer_summarize(text, length_setting=length_setting)
        actual_model = f"DistilBART Transformer ({_model_name})"

    elapsed_time = round(time.time() - start_time, 3)

    summary_words = len(re.findall(r'\b\w+\b', summary))
    summary_sentences = len(split_into_sentences(summary))

    compression_ratio = round(((orig_words - summary_words) / orig_words * 100), 1) if orig_words > 0 else 0.0
    compression_ratio = max(0.0, compression_ratio)

    rouge_scores = calculate_rouge_metrics(text, summary)

    return {
        "summary": summary,
        "model_used": actual_model,
        "metrics": {
            "original_words": orig_words,
            "original_sentences": orig_sentences,
            "summary_words": summary_words,
            "summary_sentences": summary_sentences,
            "compression_ratio_pct": compression_ratio,
            "inference_time_sec": elapsed_time,
            "rouge": rouge_scores
        }
    }
