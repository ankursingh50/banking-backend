from fastapi import APIRouter, HTTPException
from models.account import AccountDetails

router = APIRouter()

@router.get("/account-details/{iqama_id}")
async def get_account_details(iqama_id: str):
    record = await AccountDetails.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Account details not found")
    return record
