from fastapi import APIRouter, HTTPException
from models.customer import OnboardedCustomer

router = APIRouter()

# 1. Get successfully onboarded customers
@router.get("/customers/completed")
async def get_completed_customers():
    return await CustomerRecord.filter(status="completed").all()

# 2. Get partially onboarded customers
@router.get("/customers/partial")
async def get_partial_customers():
    return await CustomerRecord.exclude(status="completed").all()

# 3. Delete partially onboarded customer by Iqama ID
@router.delete("/customers/partial/{iqama_id}")
async def delete_partial_customer(iqama_id: str):
    record = await CustomerRecord.get_or_none(iqama_id=iqama_id)
    if not record or record.status == "completed":
        raise HTTPException(status_code=404, detail="Partial customer not found or already completed")
    await record.delete()
    return {"message": "Partial customer deleted"}

# 4. Remove device bindings for a customer
@router.put("/customers/unbind-device/{iqama_id}")
async def unbind_device(iqama_id: str):
    record = await CustomerRecord.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Customer not found")
    record.device_id = None
    record.device_type = None
    await record.save()
    return {"message": "Device unbound from customer"}
