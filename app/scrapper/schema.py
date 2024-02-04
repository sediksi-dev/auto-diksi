from pydantic import BaseModel
from typing import ClassVar, List
from modules.bot.schema import Info as BotInfo
from modules.wp.schema import WpPostResponse, WpPostStatuses


class GetAllPosts(WpPostResponse, BaseModel):
    """Response model for the /{module_name}/all endpoint. Exclude the some fields from the WpPostResponse model"""

    link: ClassVar[str]
    date: ClassVar[str]
    date_gmt: ClassVar[str]
    modified: ClassVar[str]
    modified_gmt: ClassVar[str]
    categories: ClassVar[List[int]]
    tags: ClassVar[List[int]]
    author: ClassVar[int]
    featured_media: ClassVar[int]
    type: ClassVar[str]
    status: ClassVar[WpPostStatuses]


class GetInfoResponse(BotInfo, BaseModel):
    """Response model for the /{module_name}/info endpoint"""
    pass
