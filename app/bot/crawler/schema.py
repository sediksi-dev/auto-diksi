from pydantic import BaseModel, field_serializer
from typing import List, Optional
from datetime import datetime


class Taxonomies(BaseModel):
    term_name: str
    taxonomy_id: int
    taxonomy_name: Optional[str]


class SourceModel(BaseModel):
    id: int
    url: str
    api_endpoint: str
    post_type: str
    taxonomies: List[Taxonomies]


class WpRendered(BaseModel):
    rendered: str


class Articles(BaseModel):
    id: int
    date: datetime
    guid: WpRendered | str
    title: WpRendered | str
    slug: str
    link: str

    @field_serializer("guid", "title", when_used="json")
    def render_guid(v: WpRendered):
        if isinstance(v, WpRendered):
            return v.rendered
        return v


class ArticlesObject(BaseModel):
    source: SourceModel
    taxonomies: Taxonomies
    articles: List[Articles]

    @field_serializer("source", when_used="json")
    def source_to_string(v: SourceModel):
        return v.url


class ArticleItem(BaseModel):
    published_date: datetime
    title: str
    link: str
    post_id: int
    source: str
    taxonomies: List[Taxonomies]


class ArticleCounter(BaseModel):
    source: str
    count: int
