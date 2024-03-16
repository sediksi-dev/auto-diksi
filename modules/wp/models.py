from pydantic import BaseModel
from typing import Literal


class WpPostData(BaseModel):
    title: str
    content: str
    excerpt: str
    status: Literal["publish", "draft"] = "draft"
    categories: str = ""
    tags: str = ""
