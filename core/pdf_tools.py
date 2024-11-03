import fitz  # PyMuPDF
import os

def extract_text_from_pdfs(folder_path):
    """
    Extracts text from all PDF files in a given folder.
    
    Parameters:
    - folder_path (str): Path to the folder containing PDF files.
    
    Returns:
    - list: A list of strings, each containing the text of one PDF file.
    """
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            text = ""
            with fitz.open(file_path) as pdf:
                for page in pdf:
                    text += page.get_text()
            documents.append(text)
    return documents
