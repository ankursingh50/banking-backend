# routes/transactions.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel
from tortoise.expressions import Q
from models.transaction_history import TransactionHistory

router = APIRouter(tags=["Transactions"])

# ---------- Pydantic response schemas ----------
class TransactionOut(BaseModel):
    transaction_id: int
    account_number: int
    transaction_type: Optional[str]
    transaction_date: date
    transaction_amount: Decimal
    available_balance: Optional[Decimal] = None
    time_of_transaction: Optional[str] = None  # ISO "HH:MM:SS"
    merchant: Optional[str] = None
    reference_number: Optional[str] = None
    location_of_transaction: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True  # (Pydantic v2) allow ORM -> model

class TransactionListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[TransactionOut]

class DailySummaryOut(BaseModel):
    day: date
    txn_count: int
    total_amount: Decimal

# ---------- Endpoints ----------
@router.get("/transactions", response_model=TransactionListOut)
async def list_transactions(
    account_number: Optional[int] = Query(None, description="Filter by account_number"),
    from_date: Optional[date] = Query(None, description="Inclusive start date"),
    to_date: Optional[date] = Query(None, description="Inclusive end date"),
    merchant: Optional[str] = Query(None, description="Case-insensitive contains"),
    txn_type: Optional[str] = Query(None, description="Transaction type contains (ILIKE)"),
    reference_search: Optional[str] = Query(None, description="Search in reference number (ILIKE)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    # Build filters
    q = Q()
    if account_number is not None:
        q &= Q(account_number=account_number)
    if from_date is not None:
        q &= Q(transaction_date__gte=from_date)
    if to_date is not None:
        q &= Q(transaction_date__lte=to_date)
    if merchant:
        q &= Q(merchant__icontains=merchant)
    if txn_type:
        q &= Q(transaction_type__icontains=txn_type)
    if reference_search:
        q &= Q(reference_number__icontains=reference_search)

    total = await TransactionHistory.filter(q).count()
    rows = (
        await TransactionHistory
        .filter(q)
        .order_by("-transaction_date", "-time_of_transaction")
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert to Pydantic
    items = [TransactionOut.model_validate(r) for r in rows]
    return TransactionListOut(total=total, limit=limit, offset=offset, items=items)


@router.get("/transactions/{transaction_id}", response_model=TransactionOut)
async def get_transaction(transaction_id: int):
    row = await TransactionHistory.get_or_none(transaction_id=transaction_id)
    if not row:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionOut.model_validate(row)


@router.get("/accounts/{account_number}/transactions/daily-summary", response_model=List[DailySummaryOut])
async def account_daily_summary(
    account_number: int,
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
):
    q = Q(account_number=account_number)
    if from_date:
        q &= Q(transaction_date__gte=from_date)
    if to_date:
        q &= Q(transaction_date__lte=to_date)

    # Use ORM first; if perf becomes an issue, switch to raw SQL with GROUP BY
    rows = (
        await TransactionHistory
        .filter(q)
        .group_by("transaction_date")
        .annotate(
            txn_count=TransactionHistory.id.count(),  # fallback: we don't have ".id", so use any field's count
        )
        .order_by("-transaction_date")
        .values("transaction_date")
    )

    # When you need SUM(amount), Tortoise requires F-expressions; simpler path: raw SQL:
    # We’ll do a small raw query to include SUM(amount).
    sql = """
        SELECT "Transaction Date" AS day,
               COUNT(*) AS txn_count,
               SUM("Transaction amount") AS total_amount
        FROM transaction_history
        WHERE account_number = $1
          {from_clause}
          {to_clause}
        GROUP BY day
        ORDER BY day DESC
    """
    params = [account_number]
    from_clause = "AND \"Transaction Date\" >= $2" if from_date else ""
    to_clause = "AND \"Transaction Date\" <= $3" if to_date else ""
    # Adjust parameter ordering if from/to not provided
    if from_date and to_date:
        params = [account_number, from_date, to_date]
    elif from_date and not to_date:
        sql = sql.replace("{to_clause}", "")
        params = [account_number, from_date]
    elif to_date and not from_date:
        sql = sql.replace("{from_clause}", "")
        params = [account_number, to_date]
    else:
        sql = sql.replace("{from_clause}", "").replace("{to_clause}", "")

    # Execute raw SQL with Tortoise
    res = await TransactionHistory.raw(sql.format(from_clause=from_clause, to_clause=to_clause), *params)
    # .raw returns a list of model instances; easier: use execute_query_dict:
    from tortoise import Tortoise
    resdict = await Tortoise.get_connection("default").execute_query_dict(
        sql.format(from_clause=from_clause, to_clause=to_clause), params
    )
    return [DailySummaryOut(**r) for r in resdict]
