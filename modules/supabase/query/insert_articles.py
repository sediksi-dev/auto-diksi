from pydantic import BaseModel
from modules.supabase.db import db
from modules.supabase.schema.articles import Article


class ArticleToInsert(BaseModel):
    title: str
    published_date: str
    post_id: int
    link: str


def insert_articles(article: ArticleToInsert):
    res, _ = (
        db.table("articles")
        .insert(
            {
                "post_title": article.title,
                "published_date": str(article.published_date),
                "original_id": article.post_id,
                "source_url": article.link,
            }
        )
        .execute()
    )
    return Article(**res[1][0])
