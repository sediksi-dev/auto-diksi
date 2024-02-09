from pydantic import BaseModel
from typing import List, Dict
from .crawler.models.articles import SubmittedArticles


class CrawlerResponse(SubmittedArticles, BaseModel):
    pass


class WriterArticleMap(BaseModel):
    source: str
    target: str
    language: Dict[str, str]
    target_taxonomies: Dict[str, List[int]]


class WriterResponse(BaseModel):
    id: int
    title: str
    post_id: int
    map: WriterArticleMap
