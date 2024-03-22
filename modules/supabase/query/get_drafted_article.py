from modules.supabase.db import db
from .models.drafted_article import DraftedArticle
from helper.error_handling import error_handler


@error_handler("db", "Error when getting articles")
def get_drafted_article(id: int = None) -> DraftedArticle:
    target = "target_id(term:term_name, tax_id:taxonomy_id, endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
    source = "source_id(endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
    mapping = f"item:taxonomy_mapping(source:{source}, target:{target})"
    query = (
        "id: id",
        "title: post_title",
        "post_id: original_id",
        f"map: articles_mapping({mapping})",
    )
    if id:
        res, _ = (
            db.table("articles")
            .select(*query)
            .eq("status", "draft")
            .eq("id", id)
            .single()
            .execute()
        )
    else:
        res, _ = (
            db.table("articles")
            .select(*query)
            .eq("status", "draft")
            .limit(1)
            .single()
            .execute()
        )

    results = res[1]

    if results is None:
        return []

    if len(results) == 0:
        return []

    try:
        result = DraftedArticle(**results)
        return result
    except Exception as e:
        raise e
