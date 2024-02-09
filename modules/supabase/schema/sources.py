from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, Literal


class DbSourceModel(BaseModel):
    id: Optional[int]  # auto-generated, optional di model
    created_at: Optional[datetime] = datetime.now()  # nilai default sekarang
    source: str
    target: str
    original_id: int
    post_status: Literal["draft", "publish", "private", "error"] = "draft"
    original_url: HttpUrl
    public_url: Optional[HttpUrl]
