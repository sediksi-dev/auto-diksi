from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional
import re


class DbSourceModel(BaseModel):
    id: Optional[int]  # auto-generated, optional di model
    created_at: Optional[datetime] = datetime.now()  # nilai default sekarang
    source: str
    target: str
    original_id: int
    post_status: str = "draft"  # nilai default 'draft'
    original_url: Optional[str]
    public_url: Optional[str]

    @validator("original_url", "public_url", pre=True, always=True, allow_reuse=True)
    def validate_url(cls, v):
        if v and not re.match(r"^(http|https)://[a-zA-Z0-9./?=_-]+$", v):
            raise ValueError("URL tidak valid")
        return v

    class Config:
        orm_mode = True
