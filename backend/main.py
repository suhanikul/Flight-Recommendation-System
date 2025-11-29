from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

from nlp.extract import extract_flight_details, get_iata_code
from backend.summary import summarize_basic
from backend.reason import generate_reasoning

load_dotenv()

app = FastAPI()

# CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SERP_API_KEY = os.getenv("SERP_API_KEY")


class FlightQuery(BaseModel):
    query: str


@app.post("/simple-summary")
def simple_summary(payload: FlightQuery):

    # Step 1 — NLP
    details = extract_flight_details(payload.query)
    origin_city = details["origin"]
    destination_city = details["destination"]
    date = details["date"]

    # Step 2 — IATA
    origin = get_iata_code(origin_city)
    destination = get_iata_code(destination_city)

    # Step 3 — SERP API
    params = {
        "engine": "google_flights",
        "departure_id": origin,
        "arrival_id": destination,
        "outbound_date": date,
        "type": 2,
        "api_key": SERP_API_KEY
    }

    serp_data = requests.get("https://serpapi.com/search", params=params).json()

    # Combine all flight results
    results = serp_data.get("best_flights", []) + serp_data.get("other_flights", [])

    # Step 4 — Summary calculations
    cheapest, fastest, best = summarize_basic(results)

    # Step 5 — AI Reasoning
    reasoning = generate_reasoning(
        origin_city, destination_city, date,
        cheapest, fastest, best
    )

    return {
        "query": payload.query,
        "structured": details,
        "iata": {"origin": origin, "destination": destination},
        "cheapest": cheapest,
        "fastest": fastest,
        "best_overall": best,
        "reasoning": reasoning,
        "results": results
    }
