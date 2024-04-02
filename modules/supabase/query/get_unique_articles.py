# from pydantic import BaseModel
from modules.supabase.db import db


def get_unique_articles_by_source_id(source_id, status: str = None):
    query = (
        "draft_id: id",
        "post_title",
        "status",
        "date: published_date",
        "map: articles_mapping!inner(tax: taxonomy_mapping_id!inner(source_id!inner(web_id))))",
    )

    response = db.table("articles").select(*query)
    if status:
        response = response.eq("status", status)
    try:
        response = response.eq("map.tax.source_id.web_id", source_id)
        response = response.order(column="published_date", desc=True)
        response = response.limit(1).maybe_single()
        response = response.execute()
        if not response.data:
            return None

        return response.data
    except Exception:
        return None
