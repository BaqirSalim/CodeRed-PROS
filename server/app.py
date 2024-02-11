from datetime import date
import json
from flask import Flask
import google.generativeai as genai

# import server.config as config

app = Flask(__name__)


genai.configure(api_key="AIzaSyCIPjPfDJIf9Ueqz5mfWMUZ3LFXoGvyisg")

INITIAL_PROMPT = f"""
current date: {date.today()}

You are a flight booking assistant. The user will make a request to you and your job is to output it in the following schema:
{{
    "originLocationCode": "The place they want to travel from. Fill this with the IATA code for the city",
    "destinationLocationCode": "The place they want to go to. fill this with the IATA code for the city",
    "departureDate": "The day they'd like to travel on. calculate this using the current date provided",
    "returnDate": "The day they'd like to come back",
    "adults": "assume all passengers are adults unless otherwise specified. Only include this property if the number of passengers is greater than 1",
    "children": "only include this parameter if the number of children specified is greater than 0",
    "travelClass": "only include this parameter if a class other than ECONOMY is specified. The options are PREMIUM_ECONOMY, BUSINESS, and FIRST",
    "includedAirlineCodes": "only include this if the user specifies an airline they specifically want to fly on. fill this with the IATA airline codes for the airline",
    "excludedAirlineCodes":  "only include this if the user specifies an airline they do not want to fly on. fill this with the IATA airline codes for the airline",
    "nonStop": "only include this parameter if the user specifies that they want a nonstop flight. if so put true in this property",
    "maxPrice": "only include this parameter if the user specifies a limit for the price"
}}
"""

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)

chat = model.start_chat(
    history=[
        {"role": "user", "parts": [INITIAL_PROMPT]},
        {"role": "model", "parts": ["understood"]},
    ]
)


@app.route("/convert_nlp/<prompt>")
def convert_nlp(prompt):
    response = chat.send_message(prompt)
    json_response = json.loads(response.text)
    # json_object = json.dumps(json_response, indent=4)
    return json_response

def fetch_flight_details(obj):



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
