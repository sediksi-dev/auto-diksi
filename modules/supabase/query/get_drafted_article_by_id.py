from modules.supabase.db import db
from .models.drafted_article import DraftedArticle
from helper.error_handling import error_handler


@error_handler("db", "Error when get drafted article by id")
def get_drafted_article_by_id(id: int) -> DraftedArticle:
    target = "target_id(term:term_name, tax_id:taxonomy_id, endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
    source = "source_id(endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
    mapping = f"item:taxonomy_mapping(source:{source}, target:{target})"
    query = (
        "id: id",
        "title: post_title",
        "post_id: original_id",
        f"map: articles_mapping({mapping})",
    )
    res, _ = db.table("articles").select(*query).eq("id", id).single().execute()
    result = DraftedArticle(**res[1])
    return result
