from flask import Flask, request
from saver import extract_save

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/save-pdf", methods=["POST"])
def save_pdf():
    link = request.form["link"]
    category = request.form["category"]
    return extract_save(link, category)
