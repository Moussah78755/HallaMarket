from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import io

from .database import engine, Base, get_db
from .models import AgriculturalLog
from .gemini_client import process_audio_with_gemini

app = FastAPI(title="HallaMarket Backend")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed initial data if empty
    async with AsyncSessionLocal() as db:
        from sqlalchemy import select
        result = await db.execute(select(AgriculturalLog))
        if not result.scalars().first():
            seed_data = [
                AgriculturalLog(crop="Irish Potatoes", quantity="50 bags", location="Santa", intent="supply_declaration", source="whatsapp"),
                AgriculturalLog(crop="Habanero Peppers", quantity="15 rubbers", location="Food Market", intent="supply_declaration", source="whatsapp"),
                AgriculturalLog(crop="Maize", quantity="20 bags", location="Mile 6", intent="supply_declaration", source="ussd"),
                AgriculturalLog(crop="Carrots", quantity="10 crates", location="Santa", intent="demand_request", source="ussd"),
            ]
            db.add_all(seed_data)
            await db.commit()
            print("Database seeded with mock data.")

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Simulates incoming WhatsApp payload with a media URL.
    """
    payload = await request.json()
    media_url = payload.get("media_url")
    
    if not media_url:
        raise HTTPException(status_code=400, detail="Missing media_url")
    
    # Simulate fetching the audio file from the URL
    try:
        # In a real scenario, this would be an async request to WhatsApp/Twilio
        response = requests.get(media_url)
        response.raise_for_status()
        audio_content = response.content
        
        # Determine mime type based on extension or URL
        mime_type = "audio/ogg"
        if media_url.endswith(".mp3"):
            mime_type = "audio/mpeg"
        elif media_url.endswith(".wav"):
            mime_type = "audio/wav"
            
        # Process with Gemini
        extracted_data = await process_audio_with_gemini(audio_content, mime_type)
        
        # Save to database
        new_log = AgriculturalLog(
            crop=extracted_data.get("crop"),
            quantity=extracted_data.get("quantity"),
            location=extracted_data.get("location"),
            intent=extracted_data.get("intent"),
            source="whatsapp"
        )
        db.add(new_log)
        await db.commit()
        
        return {"status": "success", "data": extracted_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/webhook/ussd", response_class=PlainTextResponse)
async def ussd_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Handles Africa's Talking USSD protocol.
    Params: sessionId, phoneNumber, networkCode, serviceCode, text
    """
    form_data = await request.form()
    text = form_data.get("text", "")
    
    # Structural branching for USSD
    if text == "":
        # Main Menu
        response = "CON Welcome to HallaMarket Bamenda\n"
        response += "1. Check Market Safety\n"
        response += "2. Log Crop Supply\n"
        response += "3. Check Local Prices"
    elif text == "1":
        # Market Safety
        response = "END Market Safety: Santa - Safe, Mile 6 - Caution, Food Market - Safe."
    elif text == "2":
        # Log Supply Start
        response = "CON Enter Crop Name (e.g. Potato, Pepa):"
    elif text.startswith("2*"):
        parts = text.split("*")
        if len(parts) == 2:
            response = f"CON How many bags/rubbers of {parts[1]}?"
        elif len(parts) == 3:
            response = f"CON Where is the location? (Santa, Mile 6, etc.)"
        elif len(parts) == 4:
            # Finalize Log
            crop, qty, loc = parts[1], parts[2], parts[3]
            new_log = AgriculturalLog(
                crop=crop,
                quantity=qty,
                location=loc,
                intent="supply_declaration",
                source="ussd"
            )
            db.add(new_log)
            await db.commit()
            response = f"END Thank you! Logged {qty} of {crop} at {loc}."
    elif text == "3":
        # Local Prices
        response = "END Current Prices: Potato (Bag) - 15k CFA, Pepa (Rubber) - 2k CFA."
    else:
        response = "END Invalid option. Please try again."
        
    return response

@app.get("/api/records")
async def get_records(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(AgriculturalLog).order_by(AgriculturalLog.timestamp.desc()))
    return result.scalars().all()

@app.get("/logs")
async def get_logs(db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select
    result = await db.execute(select(AgriculturalLog).order_by(AgriculturalLog.timestamp.desc()))
    return result.scalars().all()
