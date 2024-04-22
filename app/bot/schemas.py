from pydantic import BaseModel
from typing import List, Literal, Optional

from .crawl.models import SubmittedArticles
from .rewrite.models import ArticleWriteOutput, FeaturedMediaData
from .drafter.models import DraftedArticles
from modules.wp.models import PostToWpResponse


# Schema for any response that will be sent by the API
class DefaultResponse(BaseModel):
    status: Literal["success", "error"]
    message: str = ""


# Schema for the response of the crawl endpoint
class CrawlerResponse(DefaultResponse):
    data: List[SubmittedArticles] = []


class DrafterResponse(DefaultResponse):
    data: List[DraftedArticles] = []


class RewriterResponse(DefaultResponse):
    data: ArticleWriteOutput


class UploaderResponse(DefaultResponse):
    data: PostToWpResponse


# Schema for the payload of the post endpoint
class UploaderBody(BaseModel):
    title: str
    content: str
    excerpt: str
    date: Optional[str] = None


class UploaderPayload(BaseModel):
    draft_id: int
    body: UploaderBody
    featured_media: Optional[FeaturedMediaData] = None
