import os
import re
from pypdf import PdfReader
import docx

def extract_text_from_txt(file_bytes_or_path):
    """Extract text from TXT file bytes or filepath."""
    try:
        if isinstance(file_bytes_or_path, str):
            with open(file_bytes_or_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        else:
            return file_bytes_or_path.decode('utf-8', errors='ignore')
    except Exception as e:
        raise ValueError(f"Failed to read TXT file: {str(e)}")

def extract_text_from_pdf(file_stream_or_path):
    """Extract text from PDF using pypdf."""
    try:
        reader = PdfReader(file_stream_or_path)
        text_content = []
        for i, page in enumerate(reader.pages):
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)
        full_text = "\n".join(text_content)
        if not full_text.strip():
            raise ValueError("No extractable text found in PDF (file may be scanned/image-based).")
        return full_text
    except Exception as e:
        raise ValueError(f"Failed to read PDF file: {str(e)}")

def extract_text_from_docx(file_stream_or_path):
    """Extract text from DOCX using python-docx."""
    try:
        doc = docx.Document(file_stream_or_path)
        full_text = []
        for paragraph in doc.paragraphs:
            if paragraph.text:
                full_text.append(paragraph.text)
        text = "\n".join(full_text)
        if not text.strip():
            raise ValueError("DOCX document appears to be empty.")
        return text
    except Exception as e:
        raise ValueError(f"Failed to read DOCX file: {str(e)}")

def clean_extracted_text(text: str) -> str:
    """Clean and normalize raw extracted text."""
    if not text:
        return ""
    # Normalize multiple whitespace and carriage returns
    text = re.sub(r'\r\n|\r', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def parse_file(file_storage) -> tuple[str, str]:
    """
    Parse uploaded Werkzeug FileStorage object.
    Returns: (cleaned_text, filename)
    """
    filename = file_storage.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext == '.txt':
        raw_text = extract_text_from_txt(file_storage.read())
    elif ext == '.pdf':
        raw_text = extract_text_from_pdf(file_storage.stream)
    elif ext in ['.docx', '.doc']:
        raw_text = extract_text_from_docx(file_storage.stream)
    else:
        raise ValueError(f"Unsupported file format '{ext}'. Supported formats: .txt, .pdf, .docx")

    cleaned = clean_extracted_text(raw_text)
    if not cleaned:
        raise ValueError("The extracted text from the file is empty.")
    
    return cleaned, filename
