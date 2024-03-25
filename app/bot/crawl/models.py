from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List

from modules.supabase.schema.articles import Article


class WpRenderedField(BaseModel):
    rendered: str = ""


class WpPostData(BaseModel):
    model_config = ConfigDict(extra="allow")
    id: int = Field(..., alias="id")
    date: datetime = Field(..., alias="date")
    guid: WpRenderedField = Field(..., alias="guid")
    title: WpRenderedField = Field(..., alias="title")
    slug: str = Field(..., alias="slug")
    link: str = Field(..., alias="link")


class WpPreparedArticle(BaseModel):
    post_id: int
    title: str
    link: str
    published_date: datetime


class ArticleToTaxMapping(BaseModel):
    id: Optional[int]
    articles_id: int
    taxonomy_mapping_id: int


class SubmittedArticles(BaseModel):
    article: Article
    tax_mapping: List[ArticleToTaxMapping]
