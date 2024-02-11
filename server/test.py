from flask import Flask
import google.generativeai as genai

from configure import GOOGLE_API_KEY

app = Flask(__name__)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemeni-pro")


@app.route("/request/<prompt>")
def index():
    return {}
