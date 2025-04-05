import streamlit as st
import pdfplumber
import pytesseract
from PIL import Image
from transformers import pipeline

# Load the summarization model once globally
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF, using OCR for pages without selectable text."""
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
            else:
                # Perform OCR if no text is found
                image = page.to_image().convert("RGB")
                text += pytesseract.image_to_string(image) + "\n"
    return text.strip()

def chunk_text(text, chunk_size=1024):
    """Breaks long text into chunks to fit within model constraints."""
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text):
    """Summarizes long legal documents with a structured prompt."""
    prompt = (
        "You are a legal document summarization assistant. "
        "Extract key information such as the main purpose, rights and obligations, "
        "deadlines, penalties (if any), important clauses, and critical legal implications. "
        "Ensure the summary is concise yet comprehensive.\n\n"
    )
    
    chunks = chunk_text(text)
    summaries = []
    
    for chunk in chunks:
        input_text = f"{prompt}</s> {chunk}"
        summary = summarizer(input_text, max_length=300, min_length=100, do_sample=False)
        summaries.append(summary[0]["summary_text"])

    # If there are multiple chunks, summarize the combined summary too
    final_summary = " ".join(summaries)
    if len(summaries) > 1:
        final_summary = summarizer(final_summary, max_length=300, min_length=100, do_sample=False)[0]["summary_text"]

    return final_summary

# ✅ Main function to call in app.py
def document_summarizer_ui():
    st.title("📜 LexAI - Legal Document Summarizer")
    st.write("Upload a legal document (PDF), and we'll extract & summarize the key details for you.")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)

        if extracted_text:
            st.subheader("Extracted Text:")
            st.text_area("", extracted_text, height=300)

            if st.button("Summarize Document"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text(extracted_text)
                st.subheader("Summary:")
                st.write(summary)
        else:
            st.error("No readable text found in the document!")
