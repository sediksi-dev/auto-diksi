from pydantic import BaseModel, Field
from typing import Any

from modules.ai.models import ArticleToArticleOutput


class ArticleDataFromSource(BaseModel):
    source: str
    target: str
    language: dict[str, str]
    wp_data: Any


class FeaturedMediaData(BaseModel):
    url: str
    title: str = ""
    caption: str = ""
    alt: str = ""


class ArticleWriteOutputLanguage(BaseModel):
    from_: str = Field(..., alias="from")
    to: str


class ArticleWriteOutputRaw(BaseModel):
    title: str
    post_id: int
    link: str
    languange: ArticleWriteOutputLanguage


class ArticleWriteOutput(BaseModel):
    draft_id: int
    raw: ArticleWriteOutputRaw
    result: ArticleToArticleOutput
    featured_media: FeaturedMediaData
