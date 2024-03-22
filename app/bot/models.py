from pydantic import BaseModel
from typing import List, Literal, Optional

from .crawler.models import SubmittedArticles
from .writer.models import ArticleWriteOutput, FeaturedMediaData


class DefaultResponse(BaseModel):
    status: Literal["success", "error"]
    message: str = ""


class CrawlerResponse(DefaultResponse, BaseModel):
    data: List[SubmittedArticles] = []


class RewriterResponse(DefaultResponse, BaseModel):
    data: ArticleWriteOutput


class PostToWpPayload(BaseModel):
    title: str
    content: str
    excerpt: str
    status: str = "draft"


class PostToWpArgs(BaseModel):
    draft_id: int
    body: PostToWpPayload
    featured_media: Optional[FeaturedMediaData] = None


class PostToWpResponse(BaseModel):
    message: str
    status: str
    url: str
