import requests
from datetime import date, datetime
import json
from flask import Flask
from flask_cors import CORS

import google.generativeai as genai

# import server.config as config

app = Flask(__name__)

CORS(app, origins=["*"])

# socketio = SocketIO(app)

genai.configure(api_key="AIzaSyCIPjPfDJIf9Ueqz5mfWMUZ3LFXoGvyisg")

INITIAL_PROMPT = f"""
current date: {date.today()}

You are a flight booking assistant. You will receive two types of input, an initial input and then subsequent inputs. 

The user's initial input will describe a trip they want to take and your job is to output it in the following schema:
{{
    "response": "This will be your response. you can say whatever you want",

    "api_schema":{{
    "originLocationCode": "The place they want to travel from. Fill this with the IATA code for the city",
    "destinationLocationCode": "The place they want to go to. fill this with the IATA code for the city",
    "departureDate": "The day they'd like to travel on. calculate this using the current date provided. If no date is provided, assume it is the current date",
    "returnDate": "The day they'd like to come back. Only provide this property if the return date is specified",
    "adults": "assume all passengers are adults unless otherwise specified. Default this value to 1 unless otherwise specified",
    "children": "only include this parameter if the number of children specified is greater than 0",
    "travelClass": "only include this parameter if a class other than ECONOMY is specified. The options are PREMIUM_ECONOMY, BUSINESS, and FIRST",
    "includedAirlineCodes": "only include this if the user specifies an airline they specifically want to fly on. fill this with the IATA airline codes for the airline",
    "excludedAirlineCodes":  "only include this if the user specifies an airline they do not want to fly on. fill this with the IATA airline codes for the airline",
    "nonStop": "only include this parameter if the user specifies that they want a nonstop flight. if so put true in this property",
    "currencyCode": "this is a required field. Leave it as USD",
    "maxPrice": "only include this parameter if the user specifies a limit for the price"
    }}
    
}}

"If you are having a conversation with the user and dont have enough data to construct a schema, then leave it as an empty string and i will deal with accordingly.

For subsequent requests, you are to modify this schema and return with their changes made.
"""

CONVERT_PROMPT = """
your job is to convert the following schema into natural language that can be spoken in conversation.

You will recieve two kinds of inputs, one initial input where you will show the suggested flight itinerary, and then subsequent inputs that are variations of the original. 

I want you to deliver your response in a conversational manner. For the first output you can say things like "this is what your flight will look like" and then for subsequent ones you can say things like "how about a flight like this: "

Schema:
{
"itineraries": "an array of flights for the trip",
"price": "a breakdown of the price, including total cost",
"travelerPricings": "this array will include more details about the trip. the important thing to grab from here is the cabin level (economy, business, etc)"
}

Your response will be a summary of the trip using the data youre given from the schema.
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


conversationLog = [
    {"role": "user", "parts": [INITIAL_PROMPT]},
    {"role": "model", "parts": ["understood"]},
]

convertLog = [
    {"role": "user", "parts": [CONVERT_PROMPT]},
    {"role": "model", "parts": ["understood"]},
]


def addTurn(role, content):
    conversationLog.append({"role": role, "parts": [content]})


def generateChat():
    return model.generate_content(conversationLog).text


chat = model.start_chat(history=conversationLog)

jsonConvert = model.start_chat(history=convertLog)


@app.route("/convert_nlp/<prompt>")
def convert_from_nlp(prompt):
    response = chat.send_message(prompt)
    json_response = json.loads(response.text)
    return json_response


@app.route("/nlp_convert")
def convert_to_nlp(obj):  # this will take in an object
    # obje = {
    #     "itineraries": [
    #         {
    #             "duration": "PT14H15M",
    #             "segments": [
    #                 {
    #                     "departure": {
    #                         "iataCode": "SYD",
    #                         "terminal": "1",
    #                         "at": "2021-11-01T11:35:00",
    #                     },
    #                     "arrival": {
    #                         "iataCode": "MNL",
    #                         "terminal": "2",
    #                         "at": "2021-11-01T16:50:00",
    #                     },
    #                     "carrierCode": "PR",
    #                     "number": "212",
    #                     "aircraft": {"code": "333"},
    #                     "operating": {"carrierCode": "PR"},
    #                     "duration": "PT8H15M",
    #                     "id": "1",
    #                     "numberOfStops": 0,
    #                     "blacklistedInEU": False,
    #                 },
    #                 {
    #                     "departure": {
    #                         "iataCode": "MNL",
    #                         "terminal": "1",
    #                         "at": "2021-11-01T19:20:00",
    #                     },
    #                     "arrival": {"iataCode": "BKK", "at": "2021-11-01T21:50:00"},
    #                     "carrierCode": "PR",
    #                     "number": "732",
    #                     "aircraft": {"code": "320"},
    #                     "operating": {"carrierCode": "PR"},
    #                     "duration": "PT3H30M",
    #                     "id": "2",
    #                     "numberOfStops": 0,
    #                     "blacklistedInEU": False,
    #                 },
    #             ],
    #         }
    #     ],
    #     "price": {
    #         "currency": "EUR",
    #         "total": "355.34",
    #         "base": "255.00",
    #         "fees": [
    #             {"amount": "0.00", "type": "SUPPLIER"},
    #             {"amount": "0.00", "type": "TICKETING"},
    #         ],
    #         "grandTotal": "355.34",
    #     },
    #     "travelerPricings": [
    #         {
    #             "travelerId": "1",
    #             "fareOption": "STANDARD",
    #             "travelerType": "ADULT",
    #             "price": {"currency": "EUR", "total": "355.34", "base": "255.00"},
    #             "fareDetailsBySegment": [
    #                 {
    #                     "segmentId": "1",
    #                     "cabin": "ECONOMY",
    #                     "fareBasis": "EOBAU",
    #                     "class": "E",
    #                     "includedCheckedBags": {"weight": 25, "weightUnit": "KG"},
    #                 },
    #                 {
    #                     "segmentId": "2",
    #                     "cabin": "ECONOMY",
    #                     "fareBasis": "EOBAU",
    #                     "class": "E",
    #                     "includedCheckedBags": {"weight": 25, "weightUnit": "KG"},
    #                 },
    #             ],
    #         }
    #     ],
    # }
    response = jsonConvert.send_message(json.dumps(obj))
    return response.text


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
            # print("Access Token:", access_token)
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


@app.route("/get_flight/<prompt>")
def get_flight(prompt):

    if prompt["api_schema"] == "":
        return {"naturalResponse": prompt["response"], "flightData": {}}
    else:
        convertedJson = convert_from_nlp(prompt)

        flight_details = fetch_flight_details(convertedJson)

        naturalResponse = convert_to_nlp(flight_details)

        return {"naturalResponse": naturalResponse, "flightData": flight_details}


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
