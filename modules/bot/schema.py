from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List


class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISH = "publish"
    PRIVATE = "private"


class PostOptions(BaseModel):
    status: PostStatus = PostStatus.DRAFT
    author_id: int


class Taxonomy(BaseModel):
    term_name: str = "category"
    id: int
    name: Optional[str]
    slug: Optional[str]


class TaxonomyMapping(BaseModel):
    source: Taxonomy
    target: Taxonomy


class Credentials(BaseModel):
    username: str
    password: str


class Info(BaseModel):
    source: str
    target: str
    taxonomies: List[TaxonomyMapping]
    post_options: PostOptions


class Config(Info, Credentials, BaseModel):
    username: str = Field(exclude=True)
    password: str = Field(exclude=True)


"""
if __name__ == "__main__":
    cuakz = Config(
        source="https://allthatsinteresting.com",
        target="https://cuakz.com",
        username="CUAKZ_USERNAME",
        password="CUAKZ_PASSWORD",
        taxonomies=[
            TaxonomyMapping(
                source=Taxonomy(id=1, name="news", slug="news"),
                target=Taxonomy(id=1, name="berita", slug="berita"),
            ),
            TaxonomyMapping(
                source=Taxonomy(id=2, name="entertainment", slug="entertainment"),
                target=Taxonomy(id=2, name="hiburan", slug="hiburan"),
            ),
        ],
        post_options=PostOptions(status="publish", author_id=1),
    )

    print(cuakz.model_dump())
"""
