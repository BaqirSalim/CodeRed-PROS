from flask import Flask
import google.generativeai as genai

from configure import GOOGLE_API_KEY

app = Flask(__name__)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemeni-pro")

INITIAL_PROMPT = """
current date: 2024-02-10

You are a flight booking assistant. The user will make a request to you and your job is to output it in the following schema:

You are a flight booking assistant. The user will make a request to you and your job is to output it in the following schema:
{
origin: "The place they want to travel from",
destination: "The place they want to go to",
start_date: "The day they'd like to travel on. calculate this 
using the current date provided",
return_date: "The day they'd like to come back"
}
"""


@app.route("/request/<prompt>")
def index():
    return {}
