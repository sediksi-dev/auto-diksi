from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import List

from modules.supabase.schema.articles import Article

from .sources import SourceModel, SourceTaxonomies
from .mapping import ArticleToTaxMapping


class RenderedField(BaseModel):
    rendered: str = Field(..., alias="rendered")


class RawArticles(BaseModel):
    """
    This model is used to define the fetched articles from the source.
    Usually, the articles will be formatted as json from wordpress API.
    """

    id: int = Field(..., alias="id")
    date: datetime = Field(..., alias="date")
    guid: RenderedField = Field(..., alias="guid")
    title: RenderedField = Field(..., alias="title")
    slug: str = Field(..., alias="slug")
    link: str = Field(..., alias="link")

    @field_serializer("guid", "title", when_used="json")
    def render_guid(v: RenderedField):
        if isinstance(v, RenderedField):
            return v.rendered
        return v


class ProcessedArticles(BaseModel):
    """
    This model is used to define the fetched articles from the source.
    It adds the source and taxonomies to the articles for further processing.
    """

    source: SourceModel
    taxonomies: SourceTaxonomies
    articles: List[RawArticles]

    @field_serializer("source", when_used="json")
    def source_to_string(v: SourceModel):
        return v.url


class PreparedArticles(BaseModel):
    """
    This model is used to define the formated articles from the source.
    It will be prepared to be saved to the database.
    Main purpose of this model is to merge the taxonomies from the source. So, the articles will be unique.
    """

    published_date: datetime = Field(..., alias="published_date")
    title: str = Field(..., alias="title")
    link: str = Field(..., alias="link")
    post_id: int = Field(..., alias="post_id")
    source: str = Field(..., alias="source")
    taxonomies: List[SourceTaxonomies] = Field(..., alias="taxonomies")


class SubmittedArticles(BaseModel):
    """
    This model is used to define the articles that have been submitted to the database.
    """
    article: Article
    taxonomies: List[ArticleToTaxMapping]
