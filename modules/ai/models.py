from typing import List
from langchain.pydantic_v1 import BaseModel
from .tasks.create_outline.models import OutlineArticle
from .tasks.create_seo_data.models import SEOData
from .tasks.create_outline.models import CreateOutlineFromArticleArgs


class ArticleToArticleInput(CreateOutlineFromArticleArgs, BaseModel):
    pass


class ArticleToArticleOutput(BaseModel):
    outline: OutlineArticle
    seo_data: SEOData
    intro: str
    body: List[str]
