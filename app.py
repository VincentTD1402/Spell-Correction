import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
import spell
from docx import Document

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("spell.html")

def process_word_file(file):
    doc = Document(file)
    paragraphs = [paragraph.text for paragraph in doc.paragraphs]
    return '\n'.join(paragraphs)

@app.route('/spell', methods=['GET', 'POST'])
def process():
    raw_text = ""
    results = ""

    if request.method == 'POST':
        uploaded_file = request.files.get('uploadedFile')

        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            file_ext = os.path.splitext(filename)[1]

            if file_ext == '.txt':
                # Read the content of the uploaded TXT file
                raw_text = uploaded_file.read().decode('utf-8')
                # Perform processing on the file
                results = spell.correct(raw_text)
            elif file_ext in ['.doc', '.docx']:
                # Read the content of the uploaded Word file
                raw_text = process_word_file(uploaded_file)
                # Perform processing on the file
                results = spell.correct(raw_text)
        else:
            raw_text = request.form.get('rawtext', '')
            if raw_text.strip() != '':
                results = spell.correct(raw_text)

    return render_template("spell.html", results=results, raw_text=raw_text)

if __name__ == '__main__':
    app.run(debug=True)
