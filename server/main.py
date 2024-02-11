import requests
from datetime import date
import json
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


INITIAL_PROMPT = f"""
current date: {date.today()}

You are a flight booking assistant. The user will make a request to you and your job is to output it in the following schema:
{{
    "originLocationCode": "The place they want to travel from. Fill this with the IATA code for the city",
    "destinationLocationCode": "The place they want to go to. fill this with the IATA code for the city",
    "departureDate": "The day they'd like to travel on. calculate this using the current date provided",
    "returnDate": "The day they'd like to come back. Only provide this property if the return date is specified",
    "adults": "assume all passengers are adults unless otherwise specified. Only include this property if the number of passengers is greater than 1",
    "children": "only include this parameter if the number of children specified is greater than 0",
    "travelClass": "only include this parameter if a class other than ECONOMY is specified. The options are PREMIUM_ECONOMY, BUSINESS, and FIRST",
    "includedAirlineCodes": "only include this if the user specifies an airline they specifically want to fly on. fill this with the IATA airline codes for the airline",
    "excludedAirlineCodes":  "only include this if the user specifies an airline they do not want to fly on. fill this with the IATA airline codes for the airline",
    "nonStop": "only include this parameter if the user specifies that they want a nonstop flight. if so put true in this property",
    "maxPrice": "only include this parameter if the user specifies a limit for the price"
}}
"""

CONVERT_PROMPT = """
your job is to convert the following schema into natural language that can be spoken in conversation.

Schema:
{
"itineraries": "an array of flights for the trip",
"price": "a breakdown of the price, including total cost",
"travelerPricings": "this array will include more details about the trip. the important thing to grab from here is the cabin level (economy, business, etc)"
}

Only respond with a few sentences that describe the trip using this data: departure, arrival, duration, price, and carry on information.
"""
genai.configure(api_key="AIzaSyCIPjPfDJIf9Ueqz5mfWMUZ3LFXoGvyisg")

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



chat = model.start_chat(
    history=[
        {"role": "user", "parts": [INITIAL_PROMPT]},
        {"role": "model", "parts": ["understood"]},
    ]
)

jsonConvert = model.start_chat(
    history=[
        {"role": "user", "parts": [CONVERT_PROMPT]},
        {"role": "model", "parts": ["understood"]},
    ]
)


app = FastAPI()
# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend's URL in production
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



# Our app

@app.get("/convert_nlp/{prompt}")
def convert_from_nlp(prompt: str):
    response = chat.send_message(prompt)
    json_response = json.loads(response.text)
    return json_response

@app.get("/nlp_convert")
def convert_to_nlp(obj):
    response = jsonConvert.send_message(json.dumps(obj))
    return response.text

@app.get("/get_flight/{prompt}")
def get_flight(prompt:str):
    convertedJson = convert_from_nlp(prompt)
    flight_details = fetch_flight_details(convertedJson)
    naturalResponse = convert_to_nlp(flight_details)
    return naturalResponse

def fetch_flight_details(obj):  # takes in the converted json
    # Define client ID and client secret
    CLIENT_ID = "nEJEFKF5JWhWT0Fj6NnGoqGR2duITg8L"
    CLIENT_SECRET = "G3AV2ekuaAvGEVRW"

    BASE_URL = "https://test.api.amadeus.com"

    # Construct the endpoint for obtaining access token
    endpoint = "/v1/security/oauth2/token"

    # Construct the URL
    url = BASE_URL + endpoint

    # Define payload with grant_type, client_id, and client_secret
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        # Make the POST request to obtain access token
        response = requests.post(url, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract access token from the response
            access_token = response.json()["access_token"]
            print("Access Token:", access_token)
        else:
            # Print error message if request was not successful
            print("Error:", response.status_code)
            print(response.text)
    except requests.exceptions.RequestException as e:
        # Print any exceptions that occur during the request
        print("Error:", e)

    # Construct the authentication header
    auth_header = {"Authorization": f"Bearer " + access_token}

    # Define the base URL for the Amadeus API
    BASE_URL = "https://test.api.amadeus.com/v2"

    # Construct the endpoint for the flight offer search
    endpoint = "/shopping/flight-offers"

    # Construct the URL
    url = BASE_URL + endpoint

    # Define parameters for the flight offer search

    # THESE PARAMETERS WILL NEED TO BE FILLED WITH DATA GIVEN FROM USER NLP
    # params = {
    #     'originLocationCode': 'IAH',
    #     'destinationLocationCode': 'DFW',
    #     'departureDate': '2024-02-11',
    #     'adults': 1,
    #     'nonStop': 'true',
    # }

    try:
        # Make the GET request to the Amadeus API
        response = requests.get(url, headers=auth_header, params=obj)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response data
            offers = response.json()["data"]

            itineraries = offers[0]["itineraries"]
            prices = offers[0]["price"]
            travelerPricings = offers[0]["travelerPricings"]

            toReturn = {
                "itineraries": itineraries,
                "prices": prices,
                "travelerPricings": travelerPricings,
            }
            return toReturn
        else:
            # Print error message if request was not successful
            print("Error:", response.status_code)
            print(response.text)
    except requests.exceptions.RequestException as e:
        # Print any exceptions that occur during the request
        print("Error:", e)