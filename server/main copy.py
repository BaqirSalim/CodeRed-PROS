import requests
from datetime import date
import json
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import server.config as config

systemPrompt = f"""
You are FlightChat, an flight booking assistant. Your job is to communicate with the user in order to get them the best possible flights.
Your responses should always follow this format:
{{
    "response": "Put your response to the user here",
    "api_query": {{
        
    }}
}}
"""

# {{
#     "originLocationCode": "The place they want to travel from. Fill this with the IATA code for the city",
#     "destinationLocationCode": "The place they want to go to. fill this with the IATA code for the city",
#     "departureDate": "The day they'd like to travel on. calculate this using the current date provided",
#     "returnDate": "The day they'd like to come back. Only provide this property if the return date is specified",
#     "adults": "assume all passengers are adults unless otherwise specified. Only include this property if the number of passengers is greater than 1",
#     "children": "only include this parameter if the number of children specified is greater than 0",
#     "travelClass": "only include this parameter if a class other than ECONOMY is specified. The options are PREMIUM_ECONOMY, BUSINESS, and FIRST",
#     "includedAirlineCodes": "only include this if the user specifies an airline they specifically want to fly on. fill this with the IATA airline codes for the airline",
#     "excludedAirlineCodes":  "only include this if the user specifies an airline they do not want to fly on. fill this with the IATA airline codes for the airline",
#     "nonStop": "only include this parameter if the user specifies that they want a nonstop flight. if so put true in this property",
#     "maxPrice": "only include this parameter if the user specifies a limit for the price"
# }}

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
)



conversation = \
    [
        {"role": "user", "parts": [systemPrompt]},
        {"role": "model", "parts": ["understood"]},
    ]

chat = model.start_chat(
    history=conversation
)

app = FastAPI()
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust to your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}
