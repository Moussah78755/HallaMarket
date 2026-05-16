import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

PIDGIN_TRANSLATION_PROMPT = """
Role: You are the voice composition layer for HallaMarket. Convert the provided structured data into exactly one or two sentences of warm, natural, conversational Cameroon Pidgin English. Write it phonetically so an African-accented speech synthesis model reads it with perfect local rhythm and natural cadence. Do not include markdown formatting or alternative variations.

Example Input: {"market": "Mile 6", "status": "Safe & Open"}
Example Output: "Market for Mile 6 clear fine today o. Safe path dey, so make you feel free for bring your market come."
"""

async def _translate_data_to_pidgin(data: dict) -> str:
    """
    Translates structured data into natural Cameroon Pidgin English using Gemini 3 Flash.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        input_text = json.dumps(data)
        response = model.generate_content([
            PIDGIN_TRANSLATION_PROMPT,
            f"Input: {input_text}"
        ])
        
        return response.text.strip()
    except Exception as e:
        print(f"Error translating to Pidgin: {e}")
        return "System update for HallaMarket. Check your dashboard for more info."

async def orchestrate_outbound_voice(data: dict):
    """
    Main orchestration function for outbound voice note generation.
    1. Translates data to Pidgin.
    2. (Placeholder) Synthesizes to audio.
    3. (Placeholder) Prepares for WhatsApp delivery.
    """
    pidgin_text = await _translate_data_to_pidgin(data)
    print(f"Generated Pidgin Script: {pidgin_text}")
    
    # Placeholder for TTS Synthesis (e.g. using gTTS or a specialized African model)
    # audio_file = await synthesize_audio(pidgin_text)
    
    return {
        "script": pidgin_text,
        "audio_status": "synthesis_placeholder"
    }
