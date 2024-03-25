# from pydantic import BaseModel
from modules.supabase.db import db
from modules.supabase.schema.articles import Article
from helpers.error_handling import error_handler


@error_handler("db", "Error updating draft article")
def update_article(draft_id: int, data: dict):
    res, _ = db.table("articles").update(data).eq("id", draft_id).execute()
    return [Article(**item) for item in res[1]]
