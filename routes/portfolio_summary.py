from fastapi import APIRouter, HTTPException
from models.portfolio import PortfolioSummary

router = APIRouter()

@router.get("/portfolio-summary/{iqama_id}")
async def get_portfolio_summary(iqama_id: int):
    record = await PortfolioSummary.get_or_none(iqama_id=iqama_id)
    if not record:
        raise HTTPException(status_code=404, detail="Portfolio summary not found")
    return record
