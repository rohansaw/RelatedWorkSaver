import os
import requests
import urllib.request
import uuid

import pdfplumber
from pdftitle.pdftitle import get_title_from_file

CHATGPT_PROXY_ADDRESS = "https://chatgpt-api.shn.hk/v1/" # https://github.com/ayaka14732/ChatGPTAPIFree

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def get_summary(pdf_file):
    text = extract_text(pdf_file)
    req = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Give me a summary in four sentences for the following text: {text}"}]
    }
    res = requests.post(CHATGPT_PROXY_ADDRESS, req)
    return res.text


def download_pdf(link_to_pdf):
    file_name = f"{uuid.uuid1()}.pdf"
    file__save_path = os.path.join("pdfs", file_name)
    urllib.request.urlretrieve(link_to_pdf, file__save_path)
    return file__save_path

def save(title, summary, link_to_pdf, category):
    print(title, summary, link_to_pdf, category)
    pass

def extract_save(link_to_pdf, category):
    try:
        file_path = download_pdf(link_to_pdf)
        title = get_title_from_file(file_path)
        summary = get_summary(file_path)
        save(title, summary, link_to_pdf, category)
        os.remove(file_path)
        return "SUCCESS: Summary saved!"
    except:
        return "ERROR: An unexpected error occured"



