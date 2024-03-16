from pydantic import BaseModel
from typing import List


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


class DraftedArticle(BaseModel):
    id: int
    title: str
    post_id: int
    map: List[ArticleMap]
