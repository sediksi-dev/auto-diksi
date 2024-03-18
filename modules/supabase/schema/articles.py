from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from typing import Optional
from enum import Enum


class PostStatuses(str, Enum):
    draft = "draft"
    published = "published"
    pending = "pending"
    error = "error"
    # Tambahkan status lainnya sesuai dengan definisi enum `public.post_statuses` Anda


class Article(BaseModel):
    id: Optional[int] = Field(default=None, description="Primary key.")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Record creation time."
    )
    post_title: str = Field(..., description="Title of the post.")
    published_date: Optional[datetime] = Field(
        default=None, description="Date when the post was published."
    )
    original_id: int = Field(..., description="Original identifier for the post.")
    source_url: HttpUrl = Field(..., description="URL of the source.")
    public_url: Optional[HttpUrl] = Field(
        default=None, description="Public URL of the post."
    )
    post_id: Optional[int] = Field(
        default=None, description="Post id in target website."
    )
    status: PostStatuses = Field(
        default=PostStatuses.draft, description="Status of the post."
    )
