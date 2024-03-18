# from pydantic import BaseModel
from modules.supabase.db import db
from modules.supabase.schema.articles import Article


def update_article(draft_id: int, data: dict):
    res, _ = db.table("articles").update(data).eq("id", draft_id).execute()
    return [Article(**item) for item in res[1]]
