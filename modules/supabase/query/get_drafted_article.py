from modules.supabase.db import db
from .models.drafted_article import DraftedArticle


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
    result = DraftedArticle(**res[1])
    return result


def get_article_by_id(id: int) -> DraftedArticle:
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


def get_credentials_by_host(host: str):
    query = (
        "user: auth_username",
        "pass: auth_token",
    )
    res, _ = db.table("web").select(*query).eq("url", host).single().execute()
    result = res[1]
    return result
