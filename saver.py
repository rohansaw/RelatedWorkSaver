import os
import requests
import urllib.request
import uuid

import pdfplumber
from pdftitle.pdftitle import get_title_from_file

import gspread
from oauth2client.service_account import ServiceAccountCredentials

CHATGPT_PROXY_ADDRESS = "https://chatgpt-api.shn.hk/v1/" # https://github.com/ayaka14732/ChatGPTAPIFree
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)

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

def get_worksheet(sheet_id, worksheet_name):
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet

def save_to_worksheet(title, summary, link_to_pdf, category, worksheet):
    row = [category, title, summary, link_to_pdf]
    worksheet.append_rows([row])

def extract_save(link_to_pdf, category, summary, sheet_id, worksheet_name):
    try:
        file_path = download_pdf(link_to_pdf)
        title = get_title_from_file(file_path)
        if not summary:
            summary = get_summary(file_path)
        worksheet = get_worksheet(sheet_id, worksheet_name)
        save_to_worksheet(title, summary, link_to_pdf, category, worksheet)
        os.remove(file_path)
        return "SUCCESS: Summary saved!"
    except:
        return "ERROR: An unexpected error occured"
    
def get_worksheets(sheet_id):
    sheet = client.open_by_key(sheet_id)
    worksheets = sheet.worksheets()
    res = [{"id": worksheet.id, "title": worksheet.title} for worksheet in worksheets]
    return res



