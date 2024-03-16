from pydantic import BaseModel
from typing import List, Dict


class WriterArticleMap(BaseModel):
    source: str
    target: str
    language: Dict[str, str]
    target_taxonomies: Dict[str, List[int]]


class PostToWpPayload(BaseModel):
    title: str
    content: str
    excerpt: str
    status: str


class PostToWpArgs(BaseModel):
    draft_id: int
    body: PostToWpPayload


class PostToWpResponse(BaseModel):
    message: str
    status: str
    url: str
