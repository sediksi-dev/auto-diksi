from modules.supabase.db import db
from helper.error_handling import error_handler
from .get_web_config import get_web_config


@error_handler("db", "Error when getting web config by id and key")
def get_web_config_by_id(draft_id: int, key: str) -> dict:
    query = (
        "draft_id: articles_id",
        "tax_mapping: taxonomy_mapping(target: target_id(web: web_id(host:url)))",
    )

    res, _ = (
        db.table("articles_mapping")
        .select(*query)
        .eq("articles_id", draft_id)
        .execute()
    )
    result = res[1][0]
    host = result["tax_mapping"]["target"]["web"]["host"]
    web_config = get_web_config(host)
    value = web_config[key]

    if value:
        return value
    else:
        raise ValueError(f"Key {key} not found in web config")
