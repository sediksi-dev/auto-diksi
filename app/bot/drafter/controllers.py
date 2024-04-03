from typing import List
from .models import DraftedArticles
from modules.supabase.query.get_web_sources import get_web_sources
from modules.supabase.query.get_unique_articles import get_unique_articles_by_source_id


class BotDrafter:
    def __init__(self):
        pass

    def get_all_source_id(self):
        return get_web_sources()

    def get_articles_by_source_id(self) -> List[DraftedArticles]:
        sources = self.get_all_source_id()
        results = [
            {
                "source": source.url,
                "data": get_unique_articles_by_source_id(source.id, "draft"),
            }
            for source in sources
        ]
        results = [
            DraftedArticles.model_validate(
                {
                    "id": result["data"]["draft_id"],
                    "source": result["source"],
                    "title": result["data"]["post_title"],
                    "status": result["data"]["status"],
                    "date": result["data"]["date"],
                }
            )
            for result in results
            if result["data"]
        ]

        return results
