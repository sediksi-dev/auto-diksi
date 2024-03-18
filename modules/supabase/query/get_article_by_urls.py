from typing import List
from modules.supabase.db import db


def get_articles_by_urls(urls: List[str]) -> List[str]:
    res, _ = db.table("articles").select("source_url").in_("source_url", urls).execute()
    return res[1]
