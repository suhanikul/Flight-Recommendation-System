# nlp/extract.py
from google import genai
from datetime import datetime
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# -----------------------------
# Extract origin, destination, date (strict JSON)
# -----------------------------
def extract_flight_details(user_query: str):
    today = datetime.now().strftime("%d %B %Y (%A)")  # Example: 30 November 2025 (Sunday)

    prompt = f"""
You are a flight search extraction system.
Extract ONLY the following fields:
- origin city
- destination city
- date of travel in ISO format (YYYY-MM-DD)

Today is: {today}
Use this for relative dates like:
"next Friday", "this Sunday", "tomorrow", "day after tomorrow".

User query: "{user_query}"

Return ONLY pure JSON. No explanation. No text.
Format:
{{
  "origin": "...",
  "destination": "...",
  "date": "YYYY-MM-DD"
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()
    text = re.sub(r"```json|```", "", text).strip()  # Remove markdown fences

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # fallback: try extracting with regex
        print("JSON decode failed, raw output:", text)
        raise


# -----------------------------
# Convert city name → IATA code
# -----------------------------
def get_iata_code(city: str):
    prompt = f"""
Return ONLY the 3-letter IATA airport code for this city.
City: {city}

Output example:
BOM
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    code = response.text.strip().upper()

    # Clean hallucinated characters
    code = code.replace("`", "").replace('"', "").replace("'", "").strip()

    # Keep exactly 3 letters
    if len(code) > 3:
        code = code[:3]

    return code
