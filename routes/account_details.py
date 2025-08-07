from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models.account import AccountDetails

router = APIRouter()

class UpdateNicknameRequest(BaseModel):
    nickname: str

class UpdateCreationDateRequest(BaseModel):
    creation_date: str  # Format: YYYY-MM-DD

@router.get("/account-details/{account_number}")
async def get_account_details(account_number: str):
    account = await AccountDetails.get_or_none(account_number=account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/account-details/{account_number}/nickname")
async def update_nickname(account_number: str, data: UpdateNicknameRequest):
    account = await AccountDetails.get_or_none(account_number=account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.account_nickname = data.nickname
    await account.save()
    return {"message": "Nickname updated successfully"}

@router.put("/account-details/{account_number}/creation-date")
async def update_creation_date(account_number: str, data: UpdateCreationDateRequest):
    account = await AccountDetails.get_or_none(account_number=account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.account_creation_date = data.creation_date
    await account.save()
    return {"message": "Account creation date updated successfully"}
