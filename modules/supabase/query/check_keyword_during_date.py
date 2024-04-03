import datetime
from pydantic import BaseModel
from modules.supabase.db import db


class KeywordsResponse(BaseModel):
    id: int
    keyword: str
    language: str
    rewrite_date: datetime.datetime
    rewrite_mode: str
    status: str


def get_artcile_seed_by_date() -> KeywordsResponse:
    query = (
        "id: id",
        "keyword: keywords",
        "language: language",
        "rewrite_date: rewrite_date",
        "rewrite_mode: rewrite_mode",
        "status: status",
    )
    now = datetime.datetime.now()

    try:
        response = db.from_("seed_keywords").select(*query, count="exact")
        response = response.lte("rewrite_date", now).eq("status", "draft")
        response = response.execute()

        if response.count == 0:
            return {
                "data": [],
                "count": 0,
            }

        return {
            "data": [KeywordsResponse.model_validate(row) for row in response.data],
            "count": response.count,
        }

    except Exception as e:
        print("Error getting seed keywords by date: ", e)
        return None


def update_keyword_status(id: int, status: str, **kwargs):
    try:
        response = (
            db.table("seed_keywords")
            .update({"status": status, **kwargs})
            .eq("id", id)
            .execute()
        )
        return response.data[0]
    except Exception as e:
        print("Error updating keyword status: ", e)
        return e


def bulk_update_status(data) -> bool:
    try:
        response = db.table("seed_keywords").upsert(data).execute()
        return response.data
    except Exception as e:
        print("Error updating keyword status: ", e)
        return e
