# routes/international_transactions.py
from fastapi import APIRouter, HTTPException, Query, Response
from typing import Optional, List
from datetime import date, time
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from tortoise.expressions import Q
from tortoise import Tortoise
from models.international_transaction_history import InternationalTransactionHistory

router = APIRouter(tags=["International Transactions"])

# ---------- Schemas ----------
class IntlTxnOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    international_transaction_id: int
    account_number: int
    transaction_type: Optional[str]
    transaction_date: date
    transaction_amount: Decimal
    available_balance: Optional[Decimal] = None
    time_of_transaction: Optional[time] = None
    merchant: Optional[str] = None
    reference_number: Optional[str] = None
    location_of_transaction: Optional[str] = None
    address: Optional[str] = None
    conversion_rate: Optional[Decimal] = None
    currency: Optional[str] = None
    currency_amount: Optional[Decimal] = None

class IntlTxnListOut(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[IntlTxnOut]

# ---------- Endpoints ----------
@router.get("/international-transactions", response_model=IntlTxnListOut)
async def list_international_transactions(
    account_number: Optional[int] = Query(None, description="Filter by account_number"),
    from_date: Optional[date] = Query(None, description="Inclusive start date"),
    to_date: Optional[date] = Query(None, description="Inclusive end date"),
    currency: Optional[str] = Query(None, description="Exact currency code, e.g., USD"),
    merchant: Optional[str] = Query(None, description="Case-insensitive contains"),
    txn_type: Optional[str] = Query(None, description="Transaction type contains (ILIKE)"),
    reference_search: Optional[str] = Query(None, description="Search ref number (ILIKE)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    q = Q()
    if account_number is not None:
        q &= Q(account_number=account_number)
    if from_date is not None:
        q &= Q(transaction_date__gte=from_date)
    if to_date is not None:
        q &= Q(transaction_date__lte=to_date)
    if currency:
        q &= Q(currency=currency)
    if merchant:
        q &= Q(merchant__icontains=merchant)
    if txn_type:
        q &= Q(transaction_type__icontains=txn_type)
    if reference_search:
        q &= Q(reference_number__icontains=reference_search)

    total = await InternationalTransactionHistory.filter(q).count()
    rows = (
        await InternationalTransactionHistory
        .filter(q)
        .order_by("-transaction_date", "-time_of_transaction")
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = [IntlTxnOut.model_validate(r) for r in rows]
    return IntlTxnListOut(total=total, limit=limit, offset=offset, items=items)


@router.get("/international-transactions/{international_transaction_id}",
            response_model=IntlTxnOut)
async def get_international_transaction(international_transaction_id: int):
    row = await InternationalTransactionHistory.get_or_none(
        international_transaction_id=international_transaction_id
    )
    if not row:
        raise HTTPException(status_code=404, detail="International transaction not found")
    return IntlTxnOut.model_validate(row)


@router.get("/accounts/{account_number}/international-transactions/export")
async def export_international_transactions_csv(
    account_number: int,
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    currency: Optional[str] = Query(None),
):
    # Server-side CSV generation using a concise SQL (quotes for spaced columns)
    sql = f"""
        SELECT
            international_transaction_id,
            account_number,
            "Transaction type"           AS transaction_type,
            "Transaction Date"           AS transaction_date,
            "Transaction amount"         AS transaction_amount,
            "available balance"          AS available_balance,
            "Time of transaction"        AS time_of_transaction,
            "Merchant"                   AS merchant,
            "Reference Number"           AS reference_number,
            "Location of transaction"    AS location_of_transaction,
            "Address"                    AS address,
            "Conversion Rate"            AS conversion_rate,
            "Currency"                   AS currency,
            "Currency Amount"            AS currency_amount
        FROM international_transaction_history
        WHERE account_number = $1
          {{from_clause}}
          {{to_clause}}
          {{currency_clause}}
        ORDER BY "Transaction Date" DESC, "Time of transaction" DESC
    """

    params: List = [account_number]
    from_clause = to_clause = currency_clause = ""

    if from_date:
        from_clause = "AND \"Transaction Date\" >= $" + str(len(params) + 1)
        params.append(from_date)
    if to_date:
        to_clause = "AND \"Transaction Date\" <= $" + str(len(params) + 1)
        params.append(to_date)
    if currency:
        currency_clause = "AND \"Currency\" = $" + str(len(params) + 1)
        params.append(currency)

    sql = sql.format(from_clause=from_clause, to_clause=to_clause, currency_clause=currency_clause)

    rows = await Tortoise.get_connection("default").execute_query_dict(sql, params)

    # Build CSV in-memory
    import io, csv
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()) if rows else [
        "international_transaction_id","account_number","transaction_type","transaction_date",
        "transaction_amount","available_balance","time_of_transaction","merchant","reference_number",
        "location_of_transaction","address","conversion_rate","currency","currency_amount"
    ])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    csv_bytes = buf.getvalue().encode("utf-8")
    headers = {
        "Content-Disposition": f'attachment; filename="international_transactions_{account_number}.csv"'
    }
    return Response(content=csv_bytes, media_type="text/csv; charset=utf-8", headers=headers)
