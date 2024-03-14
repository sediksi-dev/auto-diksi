from langchain.pydantic_v1 import BaseModel, Field


class ArticleToArticleInput(BaseModel):
    original_article: str = Field(
        ...,
        title="The original article",
        description="The original article to be rewritten",
    )
    lang_target: str = Field(
        "indonesia",
        title="The target language",
        description="The language to translate the article to",
    )
    lang_source: str = Field(
        "english",
        title="The source language",
        description="The language of the original article",
    )


class ArticleToArticleOutput(BaseModel):
    title: str = Field(
        ...,
        description="SEO Title of the rewritten article",
    )
    description: str = Field(
        ...,
        description="Meta Description of the rewritten article",
    )
    keyword: str = Field(
        ...,
        description="Main keyword of the rewritten article",
    )
    article: str = Field(
        ...,
        description="The rewritten article in markdown format",
    )
