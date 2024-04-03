from pydantic import BaseModel
from typing import Literal
from modules.ai.models import KeywordToArticleOutput
from modules.wp.models import PostToWpResponse
from .keyword.models import FeaturedImage


# Schema for any response that will be sent by the API
class DefaultResponse(BaseModel):
    status: Literal["success", "error"]
    message: str = ""


class GeneratePayload(BaseModel):
    keyword: str
    lang_target: str
    mode: str = "default"


class GenerateResponse(DefaultResponse):
    data: KeywordToArticleOutput


class FindImagesPayload(BaseModel):
    original_articles: str


class FindImagesResponse(DefaultResponse):
    data: FeaturedImage


class UploadPayload(BaseModel):
    article: KeywordToArticleOutput
    image: FeaturedImage


class UploadResponse(DefaultResponse):
    data: PostToWpResponse
