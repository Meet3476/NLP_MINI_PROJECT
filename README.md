# Automatic Text Summarization Using Transformer Models (NLP Mini Project)

A fully functional, web-based Natural Language Processing (NLP) mini-project built with **Flask**, **Hugging Face Transformers (DistilBART)**, and a **TF-IDF Extractive Baseline**. 

Designed specifically for academic project presentations, demonstration, and evaluation.

---

## 🌟 Key Features

1. **Transformer Abstractive Summarization**:
   - Uses Hugging Face sequence-to-sequence model (`sshleifer/distilbart-cnn-12-6`).
   - Leverages **Multi-Head Self-Attention** and **Autoregressive Decoding** to paraphrase complex articles into fluent, human-like summaries.
   - Built-in text chunking engine to handle long articles and documents without token overflow.

2. **Extractive NLP Baseline**:
   - Includes a **TF-IDF & TextRank** sentence-ranking algorithm for benchmark comparison between Abstractive and Extractive summarization techniques.

3. **Multi-Format Document Upload**:
   - Accepts raw text copy & paste.
   - Accepts document uploads: `.txt`, `.pdf` (via `pypdf`), and `.docx` (via `python-docx`).

4. **Live Performance Analytics & Metrics**:
   - Compression Ratio % calculation.
   - Real-time CPU Inference Speed (seconds).
   - Word count & sentence count comparative statistics.
   - **ROUGE Metrics Evaluation**: ROUGE-1 (Unigram overlap), ROUGE-2 (Bigram overlap), and ROUGE-L (Longest Common Subsequence).

5. **Presentation-Ready Web UI**:
   - Sleek Glassmorphism Dark Theme dashboard built with modern HTML5, CSS3, and JavaScript.
   - Built-in **"Model Architecture & Present Project"** modal detailing system workflow, transformer parameters, and NLP concepts.
   - Copy to clipboard & download `.txt` summary functionality.

---

## 📁 Project Directory Structure

```
nlp_text_summarizer/
├── app.py                      # Main Flask web application & REST routes
├── summarizer.py               # NLP Engine (DistilBART Transformer + Extractive TF-IDF)
├── file_parser.py             # File text extractor (.txt, .pdf, .docx)
├── requirements.txt            # Python package dependencies
├── run.bat                     # Double-click automated Windows launcher
├── README.md                   # Academic project documentation
├── static/
│   ├── css/
│   │   └── style.css           # Glassmorphism presentation styling
│   └── js/
│       └── main.js             # Interactive client-side application logic
└── templates/
    └── index.html              # Frontend dashboard web interface
```

---

## 🚀 How to Run the Project

### Option A: Automated One-Click Launch (Windows)
Double-click `run.bat` in the project folder. It will automatically set up the Python virtual environment, install required libraries, and start the web server at `http://127.0.0.1:5000`.

### Option B: Manual Terminal Launch

1. Open your terminal in the project directory:
   ```bash
   cd C:\Users\jddar\.gemini\antigravity\scratch\nlp_text_summarizer
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Flask application:
   ```bash
   python app.py
   ```

5. Open your browser and go to `http://127.0.0.1:5000`.

---

## 🎓 Academic Presentation Overview & Key Concepts

When presenting this project to your professor or evaluator, highlight these core NLP concepts:

1. **Difference between Extractive vs Abstractive Summarization**:
   - *Extractive*: Selects exact high-scoring sentences from the original document without changing words.
   - *Abstractive*: Understands the underlying semantic meaning using neural networks and generates *new* sentences, similar to human summarizing.

2. **Why Transformers?**:
   - Transformers replace traditional Recurrent Neural Networks (RNNs/LSTMs).
   - They process entire sequences in parallel using **Self-Attention Mechanisms**, effectively eliminating vanishing gradient problems over long text distances.

3. **Evaluation via ROUGE**:
   - **ROUGE-1**: Measures single-word overlap between generated summary and original text.
   - **ROUGE-2**: Measures two-word phrase overlap.
   - **ROUGE-L**: Measures the longest common subsequence structure.

---

## 🛠️ Built With

- **Backend**: Python 3, Flask, Werkzeug
- **NLP / ML**: Hugging Face Transformers, PyTorch, NLTK, TF-IDF
- **Document Extractors**: PyPDF, Python-Docx
- **Frontend**: Modern HTML5, Custom CSS3 (Glassmorphism), Vanilla JavaScript, FontAwesome
