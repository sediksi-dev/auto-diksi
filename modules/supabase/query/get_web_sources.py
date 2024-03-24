from pydantic import BaseModel
from typing import Optional, List
from modules.supabase.db import db
from helpers.error_handling import error_handler


class WebSourceTaxonomies(BaseModel):
    term_name: str
    taxonomy_id: int
    taxonomy_name: Optional[str]


class WebSources(BaseModel):
    id: int
    url: str
    api_endpoint: str = "wp-json/wp/v2/"
    post_type: str = "posts"
    taxonomies: List[WebSourceTaxonomies]


@error_handler("db", "Error when getting web sources.")
def get_web_sources() -> List[WebSources]:
    query = (
        "id",
        "url",
        "api_endpoint",
        "post_type",
        "tax: taxonomies(term_name, taxonomy_id, taxonomy_name)",
    )
    res, _ = db.table("web").select(*query).eq("role_key", "source").execute()
    return [
        WebSources(
            id=data["id"],
            url=data["url"],
            api_endpoint=data["api_endpoint"],
            post_type=data["post_type"],
            taxonomies=[WebSourceTaxonomies(**tax) for tax in data["tax"]],
        )
        for data in res[1]
    ]
