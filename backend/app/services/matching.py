from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import AgriculturalLog

async def find_intelligent_matches(db: AsyncSession):
    """
    Intelligently matches supply declarations with demand requests.
    """
    # Fetch all supply logs
    supply_query = await db.execute(
        select(AgriculturalLog).where(AgriculturalLog.intent == "supply_declaration")
    )
    supplies = supply_query.scalars().all()
    
    # Fetch all demand logs
    demand_query = await db.execute(
        select(AgriculturalLog).where(AgriculturalLog.intent == "demand_request")
    )
    demands = demand_query.scalars().all()
    
    matches = []
    for s in supplies:
        for d in demands:
            # Simple matching logic: same crop and potentially nearby location
            if s.crop and d.crop and s.crop.lower() == d.crop.lower():
                matches.append({
                    "supply_id": s.id,
                    "demand_id": d.id,
                    "crop": s.crop,
                    "supply_loc": s.location,
                    "demand_loc": d.location,
                    "match_score": 0.9 if s.location == d.location else 0.6
                })
                
    return matches
