from langchain.pydantic_v1 import BaseModel
from typing import List, Any

from modules.ai.models import ArticleToArticleOutput


class Endpoint(BaseModel):
    host: str
    path: str
    type: str
    lang: str


class Source(BaseModel):
    endpoint: Endpoint


class Target(BaseModel):
    term: str
    tax_id: int
    endpoint: Endpoint


class Item(BaseModel):
    source: Source
    target: Target


class ArticleMap(BaseModel):
    item: Item


class ArticleData(BaseModel):
    id: int
    title: str
    post_id: int
    map: List[ArticleMap]


class ArticleDataFromSource(BaseModel):
    id: int
    mapping: List[ArticleMap]
    source: str
    target: str
    language: dict[str, str]
    data: Any


class ArticleRewrited(BaseModel):
    id: int
    rewrited: ArticleToArticleOutput


class FeaturedMediaData(BaseModel):
    url: str
    title: str = ""
    caption: str = ""
    alt: str = ""


class ImagesData(BaseModel):
    id: int
    source: str
    featured_media: FeaturedMediaData
    body_images: List[str]


class IframeData(BaseModel):
    id: int
    source: str
    link: List[str]


class ArticleWriteOutput(BaseModel):
    content: ArticleRewrited
    images: ImagesData
    iframe: IframeData
