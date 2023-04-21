import os
import openai
from flask import Flask, render_template, request, jsonify
from PyPDF2 import PdfFileReader
from io import BytesIO

app = Flask(__name__)
openai.api_key = "AAa"

def extract_text_from_pdf(file):
    try:
        pdf_reader = PdfFileReader(file)
        text = " ".join([pdf_reader.getPage(i).extract_text() for i in range(pdf_reader.getNumPages())])
        return text
    except:
        return None

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]
    print(f"Received question: {question}")  # Add this line to check if the function is called

    pdf_file = request.files.get("pdf", None)

    prompt = f"User question: {question}"
    
    if pdf_file:
        print("Received PDF")  # Add this line to check if a PDF is received
        pdf_file = BytesIO(pdf_file.read())
        text = extract_text_from_pdf(pdf_file)
        if text:
            print(f"Extracted text from PDF:\n{text}")  # Add this line to check if text is extracted from the PDF
            prompt += f"\n\nDocument content:\n{text}"
        else: 
            prompt = f"User question: {question}"
    else:
        prompt = f"User question: {question}"

    print(prompt)

    prompt += "\n\nAnswer:"
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.3,
    )
    answer = response.choices[0].text.strip()
    return jsonify({"answer": answer})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
