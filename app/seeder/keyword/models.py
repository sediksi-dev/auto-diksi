from pydantic import BaseModel


class FeaturedImage(BaseModel):
    url: str
    title: str = ""
    caption: str = ""
    alt: str = ""
