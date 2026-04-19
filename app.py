import os
from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("keys.env")

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


client = genai.Client()
code_snippet = [""]

@app.route("/")
def home_page():
    user_input = "Give me 30 lines of C++ code"
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
        system_instruction="Give code without comments and make the code have one bug somewhere"),
        contents=user_input
    )
    code_snippet[0] = response.text

    return render_template('index.html', text=response.text)

@app.route('/submit-bug', methods=['POST'])
def submit_bug():
    data = request.get_json()
    report = data.get('description')
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview",
        config=types.GenerateContentConfig(
        system_instruction="Explain the bug in the code in detail in about 20 lines and state if the bug as described by the following text is correct"),
        contents=code_snippet[0] + " " + report
    )
    return {"status": "Success", "output": response.text}

if __name__ == '__main__':
    app.run(debug=True)