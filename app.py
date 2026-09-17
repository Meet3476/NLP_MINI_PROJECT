import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from file_parser import parse_file, clean_extracted_text
from summarizer import summarize_text

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB Max Upload Size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Return model specifications and NLP concepts for presentation."""
    info = {
        "title": "Automatic Text Summarization Using Transformer Models",
        "primary_model": {
            "name": "DistilBART-CNN-12-6 (Hugging Face)",
            "architecture": "Transformer Encoder-Decoder Sequence-to-Sequence Model",
            "type": "Abstractive Summarization",
            "parameters": "306 Million Parameters",
            "pretraining_dataset": "CNN/DailyMail News Corpus",
            "key_features": [
                "Self-Attention mechanism (Multi-Head Attention)",
                "Generates new coherent sentences (Abstractive)",
                "Distilled version of BART Large for fast CPU inference",
                "Positional Encoding & Autoregressive Decoder"
            ]
        },
        "baseline_model": {
            "name": "TF-IDF / TextRank Algorithm",
            "type": "Extractive Summarization",
            "mechanism": "Selects existing key sentences based on word frequency & sentence vector weighting"
        },
        "evaluation_metrics": [
            {"metric": "ROUGE-1", "description": "Overlap of unigrams (single words) between original and summary."},
            {"metric": "ROUGE-2", "description": "Overlap of bigrams (two-word sequences)."},
            {"metric": "ROUGE-L", "description": "Longest Common Subsequence (LCS) score reflecting sentence structure similarity."},
            {"metric": "Compression Ratio", "description": "Percentage reduction in total word count."}
        ]
    }
    return jsonify(info)

@app.route('/api/summarize', methods=['POST'])
def handle_summarize():
    """Handle text paste or uploaded file for text summarization."""
    try:
        model_type = request.form.get('model_type', 'transformer')
        length_setting = request.form.get('length', 'medium')
        source_name = "Pasted Text"
        input_text = ""

        # Check if request has JSON payload instead of FormData
        if request.is_json:
            data = request.get_json()
            input_text = data.get('text', '')
            model_type = data.get('model_type', 'transformer')
            length_setting = data.get('length', 'medium')
            source_name = "Pasted Text"
        elif 'file' in request.files and request.files['file'].filename != '':
            uploaded_file = request.files['file']
            if not allowed_file(uploaded_file.filename):
                return jsonify({"error": "Unsupported file format. Please upload .txt, .pdf, or .docx files."}), 400
            
            input_text, filename = parse_file(uploaded_file)
            source_name = secure_filename(filename)
        else:
            input_text = request.form.get('text', '')

        cleaned_text = clean_extracted_text(input_text)
        if not cleaned_text:
            return jsonify({"error": "No valid text provided to summarize. Please enter text or upload a document."}), 400

        # Enforce minimum length requirement
        if len(cleaned_text.split()) < 15:
            return jsonify({"error": "Input text is too short to summarize. Please provide at least 15 words."}), 400

        # Perform summarization
        result = summarize_text(cleaned_text, model_type=model_type, length_setting=length_setting)
        result["source_name"] = source_name
        result["input_text_snippet"] = cleaned_text[:300] + ("..." if len(cleaned_text) > 300 else "")

        return jsonify(result), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"[Server Error] {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] Starting Automatic Text Summarization Server on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
