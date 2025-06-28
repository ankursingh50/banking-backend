from fastapi import APIRouter, HTTPException
from models.absher import AbsherRecord
from models.iqama import IqamaRecord
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AbsherCreateRequest(BaseModel):
    iqama_id: str
    pep_flag: str
    tax_employer_flag: str
    disability_flag: str
    high_risk_flag: str

@router.post("/absher")
async def create_absher_record(data: AbsherCreateRequest):
    iqama = await IqamaRecord.get_or_none(iqama_id=data.iqama_id)
    if not iqama:
        raise HTTPException(status_code=404, detail="Iqama not found")

    record = await AbsherRecord.create(
        iqama=iqama,
        pep_flag=data.pep_flag,
        tax_employer_flag=data.tax_employer_flag,
        disability_flag=data.disability_flag,
        high_risk_flag=data.high_risk_flag,
    )
    return {"message": "Absher record created", "id": record.id}

@router.get("/{iqama_id}")
async def get_absher_record(iqama_id: str):
    record = await AbsherRecord.get_or_none(iqama__iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Absher record not found")
    return {
        "pep_flag": record.pep_flag,
        "tax_employer_flag": record.tax_employer_flag,
        "disability_flag": record.disability_flag,
        "high_risk_flag": record.high_risk_flag,
    }

@router.put("/absher/{iqama_id}")
async def update_absher_record(iqama_id: str, data: AbsherCreateRequest):
    record = await AbsherRecord.get_or_none(iqama__iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Absher record not found")

    record.pep_flag = data.pep_flag
    record.tax_employer_flag = data.tax_employer_flag
    record.disability_flag = data.disability_flag
    record.high_risk_flag = data.high_risk_flag

    await record.save()
    return {"message": "Absher record updated"}

