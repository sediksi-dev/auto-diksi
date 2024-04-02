from pydantic import BaseModel, model_serializer
from typing import Literal, Dict, Optional
from modules.supabase.query.get_credentials_by_host import Credentials


class WebTargetData(BaseModel):
    host: str
    api_endpoint: str
    path: str


class TargetData(BaseModel):
    web: WebTargetData
    credentials: Credentials


class WpPostData(BaseModel):
    title: str
    content: str
    excerpt: str
    status: Literal["publish", "draft"] = "draft"
    taxonomies: Dict[str, str] = {}
    featured_media: Optional[int] = None

    @model_serializer()
    def serialize_model(self):
        return {
            "title": self.title,
            "content": self.content,
            "excerpt": self.excerpt,
            "status": self.status,
            "featured_media": self.featured_media,
            **self.taxonomies,
        }


class WpRendered(BaseModel):
    rendered: str


class PostToWpResponse(BaseModel):
    id: int
    date: str
    date_gmt: str
    guid: WpRendered
    modified: str
    modified_gmt: str
    slug: str
    status: str
    type: str
    link: str
    title: WpRendered
    content: WpRendered
    excerpt: WpRendered
    author: int
    featured_media: int
