# routes/mpin.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.customer import OnboardedCustomer
from utils.security import verify_pin

router = APIRouter()

class MpinVerificationRequest(BaseModel):
    iqama_id: str
    mpin: str

@router.post("/verify-mpin")
async def verify_mpin(data: MpinVerificationRequest):
    customer = await OnboardedCustomer.get_or_none(iqama_id=data.iqama_id)
    if not customer or not customer.mpin:
        raise HTTPException(status_code=404, detail="Customer or MPIN not found")

    if not verify_pin(data.mpin, customer.mpin):
        raise HTTPException(status_code=401, detail="Invalid MPIN")

    return {"message": "MPIN verified successfully"}
