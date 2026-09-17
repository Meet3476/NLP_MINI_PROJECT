import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create output folder for figures
os.makedirs("report_figures", exist_ok=True)

def generate_figure1_system_architecture():
    """Generate System Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Colors
    c_blue = '#3b82f6'
    c_purple = '#8b5cf6'
    c_indigo = '#6366f1'
    c_green = '#10b981'
    c_amber = '#f59e0b'
    c_dark = '#1e293b'

    # Title
    ax.text(6, 7.5, "System Architecture: Automatic Text Summarization System", 
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')

    # Boxes
    # 1. Inputs
    box_inputs = patches.FancyBboxPatch((0.5, 4.5), 2.2, 2.2, boxstyle="round,pad=0.1", ec=c_blue, fc='#eff6ff', lw=2)
    ax.add_patch(box_inputs)
    ax.text(1.6, 6.3, "Document Inputs", ha='center', va='center', fontsize=11, fontweight='bold', color=c_blue)
    ax.text(1.6, 5.7, "• Direct Text\n• TXT Files\n• PDF Files (pypdf)\n• DOCX Files (python-docx)", ha='center', va='center', fontsize=9, color='#334155')

    # 2. File Parser & Preprocessor
    box_parser = patches.FancyBboxPatch((3.4, 4.5), 2.2, 2.2, boxstyle="round,pad=0.1", ec=c_indigo, fc='#eef2ff', lw=2)
    ax.add_patch(box_parser)
    ax.text(4.5, 6.3, "Text Preprocessor", ha='center', va='center', fontsize=11, fontweight='bold', color=c_indigo)
    ax.text(4.5, 5.4, "• Stream Extraction\n• Regex Cleaning\n• Chunking Engine\n  (Max 450 words/chunk)", ha='center', va='center', fontsize=9, color='#334155')

    # 3. NLP Summarization Engines
    box_engines = patches.FancyBboxPatch((6.3, 3.8), 2.6, 3.2, boxstyle="round,pad=0.1", ec=c_purple, fc='#f5f3ff', lw=2)
    ax.add_patch(box_engines)
    ax.text(7.6, 6.6, "NLP Core Engine", ha='center', va='center', fontsize=11, fontweight='bold', color=c_purple)
    
    # Sub box 1: DistilBART
    box_bart = patches.FancyBboxPatch((6.5, 5.2), 2.2, 1.1, boxstyle="round,pad=0.05", ec=c_purple, fc='#ffffff', lw=1.5)
    ax.add_patch(box_bart)
    ax.text(7.6, 5.9, "DistilBART Transformer", ha='center', va='center', fontsize=9, fontweight='bold', color=c_purple)
    ax.text(7.6, 5.5, "(Abstractive Seq2Seq)", ha='center', va='center', fontsize=8, color='#64748b')

    # Sub box 2: TF-IDF
    box_tfidf = patches.FancyBboxPatch((6.5, 4.0), 2.2, 0.9, boxstyle="round,pad=0.05", ec=c_amber, fc='#ffffff', lw=1.5)
    ax.add_patch(box_tfidf)
    ax.text(7.6, 4.5, "TF-IDF Ranker", ha='center', va='center', fontsize=9, fontweight='bold', color=c_amber)
    ax.text(7.6, 4.2, "(Extractive Baseline)", ha='center', va='center', fontsize=8, color='#64748b')

    # 4. Analytics & Metrics Engine
    box_metrics = patches.FancyBboxPatch((9.6, 4.5), 2.0, 2.2, boxstyle="round,pad=0.1", ec=c_green, fc='#ecfdf5', lw=2)
    ax.add_patch(box_metrics)
    ax.text(10.6, 6.3, "Evaluation Engine", ha='center', va='center', fontsize=11, fontweight='bold', color=c_green)
    ax.text(10.6, 5.4, "• ROUGE-1 / 2 / L\n• Compression Ratio %\n• Inference Speed (s)\n• Word/Sentence Stats", ha='center', va='center', fontsize=9, color='#334155')

    # 5. Flask API Layer
    box_flask = patches.FancyBboxPatch((3.4, 1.2), 5.5, 1.8, boxstyle="round,pad=0.1", ec='#475569', fc='#f8fafc', lw=2)
    ax.add_patch(box_flask)
    ax.text(6.15, 2.5, "Flask Web Application Framework (REST API Controller)", ha='center', va='center', fontsize=11, fontweight='bold', color='#1e293b')
    ax.text(6.15, 1.8, "GET /  |  POST /api/summarize  |  GET /api/model-info", ha='center', va='center', fontsize=10, family='monospace', color=c_indigo)

    # 6. User Interface
    box_ui = patches.FancyBboxPatch((9.6, 1.2), 2.0, 1.8, boxstyle="round,pad=0.1", ec=c_indigo, fc='#eef2ff', lw=2)
    ax.add_patch(box_ui)
    ax.text(10.6, 2.3, "Glassmorphism UI", ha='center', va='center', fontsize=11, fontweight='bold', color=c_indigo)
    ax.text(10.6, 1.6, "HTML5 / CSS3 / JS\nInteractive Dashboard", ha='center', va='center', fontsize=9, color='#334155')

    # Arrows
    arrow_props = dict(arrowstyle="->", lw=1.5, color='#475569')
    ax.annotate("", xy=(3.4, 5.6), xytext=(2.7, 5.6), arrowprops=arrow_props)
    ax.annotate("", xy=(6.3, 5.6), xytext=(5.6, 5.6), arrowprops=arrow_props)
    ax.annotate("", xy=(9.6, 5.6), xytext=(8.9, 5.6), arrowprops=arrow_props)
    
    # Downward connection to Flask API
    ax.annotate("", xy=(4.5, 3.0), xytext=(4.5, 4.5), arrowprops=arrow_props)
    ax.annotate("", xy=(7.6, 3.0), xytext=(7.6, 3.8), arrowprops=arrow_props)
    ax.annotate("", xy=(10.6, 3.0), xytext=(10.6, 4.5), arrowprops=arrow_props)
    
    # Flask to UI
    ax.annotate("", xy=(9.6, 2.1), xytext=(8.9, 2.1), arrowprops=arrow_props)

    plt.tight_layout()
    plt.savefig("report_figures/fig1_system_architecture.png", dpi=300)
    plt.close()
    print("[+] Saved fig1_system_architecture.png")

def generate_figure2_transformer_architecture():
    """Generate Transformer Model Architecture Diagram."""
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')

    ax.text(5, 7.5, "DistilBART Transformer Encoder-Decoder Architecture", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0f172a')

    # Encoder Block
    enc_box = patches.FancyBboxPatch((1.0, 1.5), 3.5, 5.2, boxstyle="round,pad=0.1", ec='#6366f1', fc='#eef2ff', lw=2)
    ax.add_patch(enc_box)
    ax.text(2.75, 6.3, "TRANSFORMER ENCODER", ha='center', va='center', fontsize=11, fontweight='bold', color='#4338ca')
    
    sub_e1 = patches.FancyBboxPatch((1.3, 4.8), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#6366f1', fc='#ffffff', lw=1.5)
    ax.add_patch(sub_e1)
    ax.text(2.75, 5.25, "Multi-Head Self-Attention", ha='center', va='center', fontsize=9, fontweight='bold')

    sub_e2 = patches.FancyBboxPatch((1.3, 3.5), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#6366f1', fc='#ffffff', lw=1.5)
    ax.add_patch(sub_e2)
    ax.text(2.75, 3.95, "Feed-Forward Neural Net", ha='center', va='center', fontsize=9, fontweight='bold')

    sub_e3 = patches.FancyBboxPatch((1.3, 2.0), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#6366f1', fc='#e0e7ff', lw=1.5)
    ax.add_patch(sub_e3)
    ax.text(2.75, 2.45, "Input Embeddings +\nPositional Encoding", ha='center', va='center', fontsize=8, fontweight='bold')

    # Decoder Block
    dec_box = patches.FancyBboxPatch((5.5, 1.5), 3.5, 5.2, boxstyle="round,pad=0.1", ec='#8b5cf6', fc='#f5f3ff', lw=2)
    ax.add_patch(dec_box)
    ax.text(7.25, 6.3, "TRANSFORMER DECODER", ha='center', va='center', fontsize=11, fontweight='bold', color='#6d28d9')

    sub_d1 = patches.FancyBboxPatch((5.8, 4.8), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#8b5cf6', fc='#ffffff', lw=1.5)
    ax.add_patch(sub_d1)
    ax.text(7.25, 5.25, "Masked Self-Attention", ha='center', va='center', fontsize=9, fontweight='bold')

    sub_d2 = patches.FancyBboxPatch((5.8, 3.5), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#8b5cf6', fc='#ffffff', lw=1.5)
    ax.add_patch(sub_d2)
    ax.text(7.25, 3.95, "Encoder-Decoder Cross Attention", ha='center', va='center', fontsize=9, fontweight='bold')

    sub_d3 = patches.FancyBboxPatch((5.8, 2.0), 2.9, 0.9, boxstyle="round,pad=0.05", ec='#8b5cf6', fc='#ede9fe', lw=1.5)
    ax.add_patch(sub_d3)
    ax.text(7.25, 2.45, "Output Linear &\nSoftmax Token Probabilities", ha='center', va='center', fontsize=8, fontweight='bold')

    # Connectors
    arrow_props = dict(arrowstyle="->", lw=2, color='#4338ca')
    ax.annotate("Context Representations", xy=(5.8, 4.0), xytext=(4.2, 4.0), arrowprops=arrow_props, fontsize=8, fontweight='bold', color='#4338ca')

    # Input & Output Labels
    ax.text(2.75, 0.8, "Original Input Text Tokens", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e293b')
    ax.annotate("", xy=(2.75, 1.5), xytext=(2.75, 1.1), arrowprops=dict(arrowstyle="->", lw=1.5, color='#475569'))

    ax.text(7.25, 0.8, "Generated Abstractive Summary", ha='center', va='center', fontsize=10, fontweight='bold', color='#1e293b')
    ax.annotate("", xy=(7.25, 1.1), xytext=(7.25, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='#475569'))

    plt.tight_layout()
    plt.savefig("report_figures/fig2_transformer_architecture.png", dpi=300)
    plt.close()
    print("[+] Saved fig2_transformer_architecture.png")

def generate_figure3_performance_chart():
    """Generate Performance Evaluation Chart."""
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)

    metrics = ['ROUGE-1\n(Unigram Overlap)', 'ROUGE-2\n(Bigram Overlap)', 'ROUGE-L\n(LCS Structure)', 'Compression\nRatio %']
    distilbart_scores = [56.63, 53.66, 56.63, 43.40]
    tfidf_scores = [100.00, 100.00, 100.00, 0.00]  # TF-IDF exact extraction vs non-compressed

    x = np.arange(len(metrics))
    width = 0.35

    rects1 = ax.bar(x - width/2, distilbart_scores, width, label='DistilBART Transformer (Abstractive)', color='#6366f1')
    rects2 = ax.bar(x + width/2, tfidf_scores, width, label='TF-IDF Ranker (Extractive Baseline)', color='#cbd5e1')

    ax.set_ylabel('Score / Percentage (%)', fontsize=10, fontweight='bold')
    ax.set_title('Comparative Quantitative Performance Evaluation', fontsize=12, fontweight='bold', pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9, fontweight='bold')
    ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1')
    ax.set_ylim(0, 115)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.savefig("report_figures/fig3_performance_evaluation.png", dpi=300)
    plt.close()
    print("[+] Saved fig3_performance_evaluation.png")

if __name__ == '__main__':
    generate_figure1_system_architecture()
    generate_figure2_transformer_architecture()
    generate_figure3_performance_chart()
    print("[*] All report diagrams successfully generated!")
