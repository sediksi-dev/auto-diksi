from pydantic import BaseModel
from typing import List, Literal, Optional, Any

from .crawl.models import SubmittedArticles
from .rewrite.models import ArticleWriteOutput, FeaturedMediaData


# Schema for any response that will be sent by the API
class DefaultResponse(BaseModel):
    status: Literal["success", "error"]
    message: str = ""


# Schema for the response of the crawl endpoint
class CrawlerResponse(DefaultResponse):
    data: List[SubmittedArticles] = []


class RewriterResponse(DefaultResponse):
    data: ArticleWriteOutput


class UploaderResponse(DefaultResponse):
    data: Any


# Schema for the payload of the post endpoint
class UploaderBody(BaseModel):
    title: str
    content: str
    excerpt: str


class UploaderPayload(BaseModel):
    draft_id: int
    body: UploaderBody
    featured_media: Optional[FeaturedMediaData] = None
