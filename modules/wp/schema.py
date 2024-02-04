from enum import Enum
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union, Literal
from datetime import datetime


class WpBaseUrl(BaseModel):
    source: HttpUrl
    target: HttpUrl


class WpConfig(BaseModel):
    source: HttpUrl
    target: HttpUrl
    auth: tuple = None


class WpEndpoint(str, Enum):
    SOURCE = "source"
    TARGET = "target"


class WpPostStatuses(str, Enum):
    PUBLISH = "publish"
    FUTURE = "future"
    DRAFT = "draft"
    PENDING = "pending"
    PRIVATE = "private"
    TRASH = "trash"
    AUTO_DRAFT = "auto-draft"
    INHERIT = "inherit"


class WpChangeEndpoint(BaseModel):
    endpoint: Literal["source", "target"]
    val: str


class WpQueryParams(BaseModel):
    per_page: Optional[int]
    page: Optional[int]
    search: Optional[str]
    order: Optional[str]
    orderby: Optional[str]
    slug: Optional[str]
    offset: Optional[int]


class WpRequestsError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

        if status_code == 404:
            self.message = "Not found, please check your url"
        elif status_code == 401:
            self.message = "Unauthorized, please check your credentials"
        elif status_code == 403:
            self.message = "Forbidden, please check your credentials"
        else:
            self.message = message


class WpRendered(BaseModel):
    rendered: str
    protected: Optional[bool] = None

    # This is because the API does not return protected key if it is False
    def __init__(self, **data):
        super().__init__(**data)
        if self.protected is None:
            self.protected = False


class WpPostResponse(BaseModel):
    id: int
    date: datetime
    date_gmt: datetime
    guid: WpRendered
    modified: datetime
    modified_gmt: datetime
    slug: str
    status: Union[WpPostStatuses, str]
    type: str
    link: str
    title: WpRendered
    content: WpRendered
    excerpt: WpRendered
    author: int
    featured_media: int
    categories: list[int]
    tags: list[int]


"""
if __name__ == "__main__":
    base_from = "source"
    test_url = WpBaseUrl(
        source="https://allthatsinteresting.com",
        target="https://cuakz.com",
    )

    val = getattr(test_url, base_from)
    print(val)
"""
