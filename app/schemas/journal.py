from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models import EntryStatus


class JournalLineIn(BaseModel):
    account_id: int
    debit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    credit: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    memo: str | None = None


class JournalEntryCreate(BaseModel):
    entry_date: date
    description: str = Field(min_length=1, max_length=500)
    reference: str | None = None
    lines: list[JournalLineIn] = Field(min_length=1)


class JournalLineRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    account_id: int
    debit: Decimal
    credit: Decimal
    memo: str | None


class JournalEntryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    entry_date: date
    description: str
    reference: str | None
    status: EntryStatus
    created_at: datetime
    lines: list[JournalLineRead]
