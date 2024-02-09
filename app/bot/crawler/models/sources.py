from pydantic import BaseModel
from typing import Literal, Optional, List


class SourceTaxonomies(BaseModel):
    term_name: Literal["categories", "tags"]
    taxonomy_id: int
    taxonomy_name: Optional[str]


class SourceModel(BaseModel):
    """
    This is the source model for the bot.
    It will be used to get the source configuration from the database.
    """

    id: int
    url: str
    api_endpoint: str = "wp-json/wp/v2/"
    post_type: str = "posts"
    taxonomies: List[SourceTaxonomies]
