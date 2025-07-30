from fastapi import APIRouter, HTTPException
from models.iqama import IqamaRecord
from models.customer import OnboardedCustomer
from datetime import date
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/validate-iqama")
async def validate_iqama(payload: dict):
    iqama_id = payload.get("iqama_id")
    mobile_number = payload.get("mobile_number")

    iqama = await IqamaRecord.get_or_none(iqama_id=iqama_id)
    if not iqama:
        raise HTTPException(status_code=404, detail="Iqama ID not found")

    if iqama.mobile_number != mobile_number:
        raise HTTPException(status_code=400, detail="Mobile number does not match")

    existing = await OnboardedCustomer.get_or_none(iqama_id=iqama_id)
    if existing and existing.status == "Account Successfully Created":
    raise HTTPException(status_code=400, detail="Iqama already onboarded")

    today = date.today()
    dob = iqama.date_of_birth
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    logger.info(f"IQAMA VALIDATION: id={iqama_id}, expiry={iqama.expiry_date}, issue={iqama.issue_date}, age={age}")
    print(f"[DEBUG] Expiry Date: {iqama.expiry_date}, Today: {today}, Age: {age}")

    return {
        "full_name": iqama.full_name,
        "arabic_name": iqama.arabic_name,
        "gender": iqama.gender,
        "city": iqama.city,
        "age": age,
        "date_of_birth": str(iqama.date_of_birth),
        "dob_hijri": str(iqama.dob_hijri) if iqama.dob_hijri else "",
        "issue_date": str(iqama.issue_date) if iqama.issue_date else None,
        "expiry_date": str(iqama.expiry_date) if iqama.expiry_date else None,
        "expiry_date_hijri": str(iqama.expiry_date_hijri) if iqama.expiry_date_hijri else ""
    }
