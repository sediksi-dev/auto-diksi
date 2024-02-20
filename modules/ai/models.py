from langchain.pydantic_v1 import BaseModel

from .tasks.create_outline.models import CreateOutlineFromArticleArgs


class ArticleToArticleInput(CreateOutlineFromArticleArgs, BaseModel):
    pass


class ArticleToArticleOutput(BaseModel):
    pass
