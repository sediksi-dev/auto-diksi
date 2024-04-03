from pydantic import BaseModel
from modules.supabase.db import db


class KeywordWebTargetData(BaseModel):
    url: str
    api_endpoint: str
    post_type: str


class KeywordCredentialsData(BaseModel):
    username: str
    password: str


class KeywordTaxData(BaseModel):
    term: str
    tax_id: int
    name: str
    slug: str


class KeywordData(BaseModel):
    id: int
    keyword: str
    language: str
    rewrite_mode: str
    publish_date: str
    publish_status: str
    web: KeywordWebTargetData
    tax: KeywordTaxData
    credentials: KeywordCredentialsData


def get_artcile_seed_data(
    draft_id: int,
    status: str = None,
) -> KeywordData:
    web_query = (
        "url: url",
        "api_endpoint: api_endpoint",
        "post_type: post_type",
    )
    credentials_query = (
        "username: username",
        "password: password",
    )
    tax_query = (
        "term: term_name",
        "tax_id: taxonomy_id",
        "name: taxonomy_name",
        "slug: taxonomy_slug",
    )

    query = (
        "id: id",
        "keyword: keywords",
        "language: language",
        "rewrite_mode: rewrite_mode",
        "publish_date: rewrite_date",
        "publish_status: publish_status",
        "web: target_id({})".format(", ".join(web_query)),
        "tax: tax_id({})".format(", ".join(tax_query)),
        "credentials: target_id({})".format(", ".join(credentials_query)),
    )

    try:
        response = db.from_("seed_keywords").select(*query)
        if status:
            response = response.eq("status", status)
        response = response.eq("id", draft_id).maybe_single().execute()
        return KeywordData.model_validate(response.data)
    except Exception:
        return None
