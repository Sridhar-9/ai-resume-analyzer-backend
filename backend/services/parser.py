import magic
import pdfplumber
from fastapi import UploadFile, File
import os

UPLOAD_FOLDER = "uploaded_files"

async def file_type(file: UploadFile = File(...)):
    header_bytes = await file.read(2048)
    await file.seek(0)
    detected_mime = magic.from_buffer(header_bytes, mime=True)
    return detected_mime


def save_local(filename, file_content):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(f"{UPLOAD_FOLDER}/{filename}", "wb") as f:
        f.write(file_content)


def extract_text(filename):
    full_text = ""
    with pdfplumber.open(f"{UPLOAD_FOLDER}/{filename}") as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    return full_text
