from fastapi import APIRouter, HTTPException, Request
from models.customer import OnboardedCustomer
from models.iqama import IqamaRecord
from pydantic import BaseModel
from typing import Optional
from utils import generate_dep_reference_number
from datetime import datetime, date
from tortoise import timezone

router = APIRouter()

# Helper to strip timezone info safely
def strip_tz(dt):
    if isinstance(dt, datetime):
        return dt.replace(tzinfo=None)
    return dt

# Request schema for onboarding start
class StartOnboardingRequest(BaseModel):
    iqama_id: str
    device_id: Optional[str]
    device_type: Optional[str]
    location: Optional[str]
    current_step: Optional[str] = None

# Request schema for update
class UpdateCustomerRequest(BaseModel):
    building_number: Optional[str]
    street: Optional[str]
    neighbourhood: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    device_id: Optional[str]
    device_type: Optional[str]
    location: Optional[str]
    status: Optional[str]
    pep_flag: Optional[str]
    tax_employer_flag: Optional[str]
    disability_flag: Optional[str]
    high_risk_flag: Optional[str]
    account_purpose: Optional[str]
    estimated_withdrawal: Optional[float]
    mpin: Optional[str]
    password: Optional[str]
    current_step: Optional[str]
    additional_mobile_number: Optional[str]
    employment_status: Optional[str]
    source_of_income: Optional[str]
    employment_sector: Optional[str]
    industry: Optional[str]
    salary_income: Optional[str]
    business_income: Optional[str]
    investment_income: Optional[str]
    rental_income: Optional[str]
    personal_allowance: Optional[str]
    pension_income: Optional[str]
    other_income: Optional[str]

# ⬇️ POST /customers/start
@router.post("/start")
async def start_customer_onboarding(data: StartOnboardingRequest):
    existing = await OnboardedCustomer.get_or_none(iqama_id=data.iqama_id)
    if existing:
        return existing

    iqama = await IqamaRecord.get_or_none(iqama_id=data.iqama_id)
    if not iqama:
        raise HTTPException(status_code=404, detail="Iqama ID not found in records")

    #if iqama.expiry_date and iqama.expiry_date < date.today():
    #    raise HTTPException(status_code=400, detail="Iqama ID is expired")

    dep_ref = await generate_dep_reference_number()

    record = await OnboardedCustomer.create(
        iqama_id=iqama.iqama_id,
        full_name=iqama.full_name,
        arabic_name=iqama.arabic_name,  
        mobile_number=iqama.mobile_number,
        date_of_birth=strip_tz(iqama.date_of_birth),
        date_of_birth_hijri=str(iqama.dob_hijri) if iqama.dob_hijri else None,
        expiry_date=strip_tz(iqama.expiry_date),
        expiry_date_hijri=iqama.expiry_date_hijri,
        issue_date=strip_tz(iqama.issue_date),
        age=(date.today().year - iqama.date_of_birth.year - ((date.today().month, date.today().day) < (iqama.date_of_birth.month, iqama.date_of_birth.day))) if iqama.date_of_birth else None,
        gender=iqama.gender,
        nationality=iqama.nationality,
        building_number=iqama.building_number,
        street=iqama.street,
        neighbourhood=iqama.neighbourhood,
        city=iqama.city,
        postal_code=iqama.postal_code,
        country=iqama.country,
        dep_reference_number=dep_ref,
        device_id=data.device_id,
        device_type=data.device_type,
        location=data.location,
        status="in_progress",
        current_step=data.current_step or "nafath"
    )
    return record

# ⬇️ GET /customers/onboarded
@router.get("/onboarded")
async def get_onboarded_customers():
    return await OnboardedCustomer.all().order_by("-created_at").values(
        "full_name",
        "iqama_id",
        "mobile_number",
        "device_id",
        "dep_reference_number",
        "created_at",
        "status",
        "current_step"
    )

# ⬇️ GET /customers/device/{device_id}
@router.get("/device/{device_id}")
async def get_customer_by_device(device_id: str):
    customer = await OnboardedCustomer.filter(
        device_id=device_id,
        status="in_progress"
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="No resumable onboarding found")

    return {
        "iqama_id": customer.iqama_id,
        "current_step": customer.current_step
    }

# ⬇️ GET /customers/{iqama_id}
@router.get("/{iqama_id}")
async def get_customer(iqama_id: str):
    record = await OnboardedCustomer.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Customer record not found")

    return {
        "iqama_id": record.iqama_id,
        "full_name": record.full_name,
        "arabic_name": record.arabic_name,
        "mobile_number": record.mobile_number,
        "dep_reference_number": record.dep_reference_number,
        "status": record.status,
        "created_at": record.created_at,
        "date_of_birth": record.date_of_birth,
        "date_of_birth_hijri": record.date_of_birth_hijri,
        "expiry_date": record.expiry_date,
        "expiry_date_hijri": record.expiry_date_hijri,
        "issue_date": record.issue_date,
        "age": record.age,
        "gender": record.gender,
        "nationality": record.nationality,
        "building_number": record.building_number,
        "street": record.street,
        "neighbourhood": record.neighbourhood,
        "city": record.city,
        "postal_code": record.postal_code,
        "country": record.country,
        "device_id": record.device_id,
        "device_type": record.device_type,
        "location": record.location,
        "account_purpose": record.account_purpose,
        "estimated_withdrawal": record.estimated_withdrawal,
        "pep_flag": record.pep_flag,
        "disability_flag": record.disability_flag,
        "tax_residency_outside_ksa": record.tax_residency_outside_ksa,
        "employment_status": record.employment_status,
        "source_of_income": record.source_of_income,
        "employment_sector": record.employment_sector,
        "industry": record.industry,
        "salary_income": record.salary_income,
        "business_income": record.business_income,
        "investment_income": record.investment_income,
        "rental_income": record.rental_income,
        "personal_allowance": record.personal_allowance,
        "pension_income": record.pension_income,
        "other_income": record.other_income,
    }

# ⬇️ PUT /customers/{iqama_id}
@router.put("/{iqama_id}")
async def update_customer(iqama_id: str, request: Request):
    record = await OnboardedCustomer.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Customer not found")

    device_id_header = request.headers.get('device_id')
    if record.device_id and device_id_header and record.device_id != device_id_header:
        pass

    update_data = await request.json()
    updated_fields_list = []

    from re import sub

    def clean_amount(val):
        try:
            return float(sub(r'[^\d.]', '', val)) if val else None
        except:
            return None

    for field, value in update_data.items():
        if hasattr(record, field):
            if field in [
                "salary_income", "business_income", "investment_income",
                "rental_income", "personal_allowance", "pension_income", "other_income"
            ]:
                setattr(record, field, clean_amount(value))
            else:
                setattr(record, field, value)
            updated_fields_list.append(field)  # ✅ Add this

    if not updated_fields_list:
        raise HTTPException(status_code=400, detail="No valid fields provided for update.")

    record.updated_at = timezone.now()
    await record.save()

    return {"message": "Customer record updated", "updated_fields": updated_fields_list}

# ⬇️ DELETE /customers/{iqama_id}
@router.delete("/{iqama_id}")
async def delete_customer(iqama_id: str):
    record = await OnboardedCustomer.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Customer not found")

    await record.delete()
    return {"message": "Customer and associated device binding removed"}
