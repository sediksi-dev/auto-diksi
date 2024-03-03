from pydantic import BaseModel
from typing import List, Dict
from .crawler.models.articles import SubmittedArticles
from modules.ai.models import ArticleToArticleOutput


class CrawlerResponse(SubmittedArticles, BaseModel):
    pass


class WriterArticleMap(BaseModel):
    source: str
    target: str
    language: Dict[str, str]
    target_taxonomies: Dict[str, List[int]]


class WriterResponse(BaseModel):
    source: str
    target: str
    language: Dict[str, str]
    result: ArticleToArticleOutput
