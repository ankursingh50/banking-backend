from fastapi import APIRouter, HTTPException
from models.card import CardDetails

router = APIRouter()

@router.get("/card-details/{account_number}")
async def get_card_details(account_number: int):
    record = await CardDetails.get_or_none(account_number=account_number)
    if not record:
        raise HTTPException(status_code=404, detail="Card details not found")
    return record
