from fastapi import APIRouter, HTTPException
from models.transaction import TransactionSummary

router = APIRouter()

@router.get("/transaction-summary/{account_number}")
async def get_transaction_summary(account_number: int):
    record = await TransactionSummary.get_or_none(account_number=account_number)
    if not record:
        raise HTTPException(status_code=404, detail="Transaction summary not found")
    return record
