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
    source: str
    target: str
    language: dict[str, str]
    data: Any


class ArticleRewrited(BaseModel):
    id: int
    rewrited: ArticleToArticleOutput
