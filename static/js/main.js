// Application State
let activeInputTab = 'text';
let currentSelectedFile = null;
let currentSummaryResult = "";

// Initialize Event Listeners on DOM Load
document.addEventListener('DOMContentLoaded', () => {
    const rawInput = document.getElementById('raw-text-input');
    rawInput.addEventListener('input', updateWordCounter);

    // Setup Drag and Drop
    const dropzone = document.getElementById('dropzone');
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, () => dropzone.classList.remove('dragover'), false);
    });

    dropzone.addEventListener('drop', handleFileDrop, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Switch between Raw Text and File Upload Tabs
function switchInputTab(tabName) {
    activeInputTab = tabName;
    const textBtn = document.getElementById('tab-text-btn');
    const fileBtn = document.getElementById('tab-file-btn');
    const textPane = document.getElementById('pane-text');
    const filePane = document.getElementById('pane-file');

    if (tabName === 'text') {
        textBtn.classList.add('active');
        fileBtn.classList.remove('active');
        textPane.classList.add('active');
        filePane.classList.remove('active');
    } else {
        fileBtn.classList.add('active');
        textBtn.classList.remove('active');
        filePane.classList.add('active');
        textPane.classList.remove('active');
    }
}

// Live Word Counter
function updateWordCounter() {
    const text = document.getElementById('raw-text-input').value.trim();
    const words = text ? text.split(/\s+/).filter(w => w.length > 0).length : 0;
    document.getElementById('input-word-count').innerHTML = `<i class="fa-regular fa-file-lines"></i> ${words} words`;
}

// Sample Text Loader
function loadSampleText(sampleType) {
    switchInputTab('text');
    const textInput = document.getElementById('raw-text-input');
    
    if (sampleType === 'ai') {
        textInput.value = `Artificial Intelligence (AI) and Natural Language Processing (NLP) are rapidly transforming modern computing. Transformer models, introduced in the seminal paper "Attention Is All You Need", have revolutionized language modeling by replacing recurrent neural networks with self-attention mechanisms. This permits parallel computation across long text sequences and captures nuanced semantic context far better than traditional architectures. Models such as BERT, GPT, and BART leverage these attention layers to perform complex tasks including text classification, language translation, abstractive text summarization, and conversational query processing. Abstractive summarization goes beyond simple sentence extraction by understanding the core semantics of a document and generating new, coherent sentences that summarize the essential information cleanly.`;
    } else if (sampleType === 'science') {
        textInput.value = `Photosynthesis is a vital biological process by which green plants, algae, and certain bacteria convert light energy from the sun into chemical energy stored in glucose molecules. This process occurs primarily inside organelles called chloroplasts, which contain chlorophyll pigments that absorb blue and red light wavelengths. During photosynthesis, water absorbed by the roots and carbon dioxide absorbed from the atmosphere undergo light-dependent and light-independent reactions (the Calvin Cycle). The overall reaction produces oxygen as a essential byproduct alongside energy-rich carbohydrates. Photosynthesis sustains life on Earth by driving global carbon cycling and replenishing atmospheric oxygen levels required by aerobic organisms.`;
    }
    updateWordCounter();
}

function clearInput() {
    document.getElementById('raw-text-input').value = '';
    updateWordCounter();
}

// File Upload Handlers
function triggerFileInput() {
    document.getElementById('file-input').click();
}

function handleFileDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) {
        handleFileSelected(files);
    }
}

function handleFileSelected(files) {
    if (!files || files.length === 0) return;
    const file = files[0];
    const validExtensions = ['.txt', '.pdf', '.docx', '.doc'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(fileExt)) {
        showToast("Unsupported file format. Please upload .txt, .pdf, or .docx files.");
        return;
    }

    currentSelectedFile = file;

    // Display metadata
    document.getElementById('selected-file-name').innerText = file.name;
    document.getElementById('selected-file-size').innerText = formatBytes(file.size);

    document.getElementById('dropzone').classList.add('hidden');
    document.getElementById('file-details').classList.remove('hidden');

    // Read preview for TXT files
    if (fileExt === '.txt') {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('file-text-preview').innerText = e.target.result.slice(0, 400) + '...';
        };
        reader.readAsText(file);
    } else {
        document.getElementById('file-text-preview').innerText = `[${fileExt.toUpperCase()} Document ready for server extraction]`;
    }
}

function removeSelectedFile() {
    currentSelectedFile = null;
    document.getElementById('file-input').value = '';
    document.getElementById('file-details').classList.add('hidden');
    document.getElementById('dropzone').classList.remove('hidden');
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Execute Summarization Request
async function executeSummarization() {
    const modelType = document.getElementById('model-select').value;
    const lengthSetting = document.getElementById('length-select').value;
    const btn = document.getElementById('summarize-btn');
    const btnText = document.getElementById('btn-text');
    const btnSpinner = document.getElementById('btn-spinner');
    const outputStatus = document.getElementById('output-status');

    let formData = new FormData();
    formData.append('model_type', modelType);
    formData.append('length', lengthSetting);

    if (activeInputTab === 'text') {
        const textVal = document.getElementById('raw-text-input').value.trim();
        if (!textVal) {
            showToast("Please enter or paste text to summarize.");
            return;
        }
        formData.append('text', textVal);
    } else {
        if (!currentSelectedFile) {
            showToast("Please select a file to upload.");
            return;
        }
        formData.append('file', currentSelectedFile);
    }

    // Set Loading State
    btn.disabled = true;
    btnText.innerText = "Processing Summary...";
    btnSpinner.classList.remove('hidden');
    outputStatus.className = "status-badge";
    outputStatus.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Processing...`;

    try {
        const response = await fetch('/api/summarize', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Summarization failed.");
        }

        renderResults(data);
        showToast("Summary generated successfully!");

    } catch (err) {
        showToast(err.message);
        outputStatus.className = "status-badge";
        outputStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> Error`;
    } finally {
        btn.disabled = false;
        btnText.innerHTML = `<i class="fa-solid fa-wand-magic-sparkles"></i> Generate Summary`;
        btnSpinner.classList.add('hidden');
    }
}

// Render Results & Metrics on UI
function renderResults(data) {
    currentSummaryResult = data.summary;
    const metrics = data.metrics;

    // Update Status Badge
    const outputStatus = document.getElementById('output-status');
    outputStatus.className = "status-badge success";
    outputStatus.innerHTML = `<i class="fa-solid fa-check"></i> ${data.model_used}`;

    // Update Metric Cards
    document.getElementById('metric-compression').innerText = `${metrics.compression_ratio_pct}%`;
    document.getElementById('metric-speed').innerText = `${metrics.inference_time_sec}s`;
    document.getElementById('metric-orig-words').innerText = metrics.original_words;
    document.getElementById('metric-summ-words').innerText = metrics.summary_words;

    // Update Summary Box Text
    const summaryBox = document.getElementById('summary-output');
    summaryBox.innerHTML = `<p>${data.summary}</p>`;

    // Update Keywords Chips
    const kwContainer = document.getElementById('keywords-container');
    const kwChips = document.getElementById('keywords-chips');
    if (metrics.top_keywords && metrics.top_keywords.length > 0) {
        kwChips.innerHTML = metrics.top_keywords.map(kw => `<span class="kw-badge"># ${kw}</span>`).join(' ');
        kwContainer.classList.remove('hidden');
    } else {
        kwContainer.classList.add('hidden');
    }

    // Update ROUGE Metrics
    const rouge = metrics.rouge;
    document.getElementById('rouge1-val').innerText = `${rouge.rouge1}%`;
    document.getElementById('rouge2-val').innerText = `${rouge.rouge2}%`;
    document.getElementById('rougeL-val').innerText = `${rouge.rougeL}%`;

    document.getElementById('rouge1-bar').style.width = `${Math.min(rouge.rouge1, 100)}%`;
    document.getElementById('rouge2-bar').style.width = `${Math.min(rouge.rouge2, 100)}%`;
    document.getElementById('rougeL-bar').style.width = `${Math.min(rouge.rougeL, 100)}%`;
}

// Actions: Copy & Download
function copySummaryText() {
    if (!currentSummaryResult) {
        showToast("No summary available to copy.");
        return;
    }
    navigator.clipboard.writeText(currentSummaryResult);
    showToast("Summary copied to clipboard!");
}

function downloadSummaryTXT() {
    if (!currentSummaryResult) {
        showToast("No summary available to download.");
        return;
    }
    const blob = new Blob([currentSummaryResult], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'summary_report.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Modal Handlers
function openModelModal() {
    document.getElementById('model-modal').classList.remove('hidden');
}

function closeModelModal() {
    document.getElementById('model-modal').classList.add('hidden');
}

// Toast System
function showToast(message) {
    const toast = document.getElementById('toast');
    toast.innerText = message;
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3500);
}
