import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

SAFETY_ANALYSIS_PROMPT = """
Role: You are the Crisis Intelligence Agent for MarketMinder AI in Bamenda. 
Analyze the provided community reports, news snippets, and traffic data to predict the safety status of a specific market hub.
Provide a "Go/No-Go" signal and a brief reason in natural Pidgin English.

Expected JSON Output:
{"status": "Safe" | "Caution" | "Danger", "signal": "Go" | "No-Go", "reason_pidgin": string}
"""

async def predict_market_safety(location: str, reports: list):
    """
    Predicts market safety status using Gemini by analyzing community reports.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        context = f"Location: {location}\nReports: {reports}"
        response = model.generate_content([
            SAFETY_ANALYSIS_PROMPT,
            context
        ])
        
        import json
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
            
        return json.loads(text_response)
    except Exception as e:
        print(f"Error predicting safety: {e}")
        return {
            "status": "Caution",
            "signal": "No-Go",
            "reason_pidgin": "System still de check path, make you wait small."
        }
