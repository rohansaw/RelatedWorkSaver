import os
from dotenv import load_dotenv

from flask import Flask, request
from flask_cors import CORS, cross_origin
from saver import extract_save, get_worksheets

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
sheet_id = os.getenv("SHEET_ID")

@app.route("/worksheets")
def worksheets():
    return get_worksheets(sheet_id)

@app.route("/save-pdf", methods=["POST"])
@cross_origin()
def save_pdf():
    link = request.form["link"]
    category = request.form["category"]
    worksheet = request.form["worksheet"]
    if "summary" in request.form:
        summary = request.form["summary"]
    else:
        summary = None
    return extract_save(link, category, summary, sheet_id, worksheet)
