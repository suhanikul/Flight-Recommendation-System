# backend/reason.py

from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reasoning(origin, destination, date, cheapest, fastest, best):
    prompt = f"""
You are an expert travel assistant.

Your job is NOT to summarize the flights. 
Your job is to provide:
1. A concrete RECOMMENDATION (1–2 lines)
2. A quick NOTE on which flights to avoid (if any)
3. 1–2 meaningful ALTERNATIVE SUGGESTIONS if the user could save money or reduce travel time

You MUST analyze:
- price differences
- duration differences
- stopovers
- relative advantages (price vs time)
- unusually expensive or slow options

You MUST give short, smart, helpful insights.
No long paragraphs. No repeated information from the UI.

Use exactly this structure:

⭐⭐ STRONG RECOMMENDATION:
<1 short line: choose X flight because Y>

⚠️ AVOID:
<1 line warning about overpriced or slow flights>

💡 BETTER OPTIONS:
<1–2 lines suggesting alternatives: earlier/later time, different day, different airline>

Rules:
- All prices are in USD → always use $.
- Never convert currency.
- Use only information present in the input flights.
- If alternatives cannot be inferred, give general travel tips instead.

Flights Provided:

Cheapest:
{cheapest}

Fastest:
{fastest}

Best Overall:
{best}

Return the text EXACTLY in this 3-section format.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()
