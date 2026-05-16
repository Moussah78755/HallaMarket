import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure the Gemini API
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
Role: You are the parsing core for HallaMarket in Bamenda, Cameroon. Process the provided local audio recording (Cameroon Pidgin English, localized English, or blended dialects) from market women or farmers, and extract data into a strict JSON object. Do not include markdown backticks or extra prose.

Fields to Extract:
- "crop": Standardized English name (e.g., "potato" -> "Irish Potatoes", "pepa" -> "Habanero Peppers"). Return null if absent.
- "quantity": Numeric value paired with the unit used (e.g., "5 bags", "2 rubbers"). Return null if absent.
- "location": Specific local hub mentioned (e.g., "Santa", "Mile 6 Market", "Food Market", "Bambili"). Return null if absent.
- "intent": Must classify strictly into one of: "supply_declaration", "demand_request", "safety_query", or null.

Expected Output Schema:
{"crop": string|null, "quantity": string|null, "location": string|null, "intent": string|null}
"""

async def process_audio_with_gemini(audio_content: bytes, mime_type: str = "audio/ogg"):
    """
    Processes audio content using Gemini 3 Flash and extracts supply chain data.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash") # Note: Using 1.5 flash as 3-flash might be internal name or latest alias
        
        # In a real scenario, we'd upload the file if it's large, 
        # but for small streams we can pass it directly if supported or use the File API.
        # For this hackathon simulation, we'll use the content-based generation.
        
        response = model.generate_content([
            SYSTEM_PROMPT,
            {
                "mime_type": mime_type,
                "data": audio_content
            }
        ])
        
        # Clean the response to ensure it's valid JSON
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text_response)
    except Exception as e:
        print(f"Error processing audio with Gemini: {e}")
        return {"crop": None, "quantity": None, "location": None, "intent": None}
