from pydantic import BaseModel
from modules.supabase.db import db
from app.bot.crawler.models import WpPostData
from urllib.parse import urlparse
from helper.error_handling import error_handler


class TaxMappingSourceData(BaseModel):
    url: str
    term: str
    tax_id: int
    tax_name: str


class TaxMapping(BaseModel):
    id: int
    source: TaxMappingSourceData


@error_handler("db", "Error when mapping taxonomies")
def get_taxonomies_map(article: WpPostData) -> list[TaxMapping]:
    parsed_url = urlparse(article.link)
    host = parsed_url.netloc
    table_name = "taxonomy_mapping"
    query = (
        "id",
        "terms:source_id!inner(term_name)",
        "tax_name:source_id!inner(taxonomy_name)",
        "tax_id:source_id!inner(taxonomy_id)",
        "source:source_id!inner(web!inner(url))",
    )
    res, _ = db.table(table_name).select(*query).eq("source.web.url", host).execute()
    data = res[1]

    return [
        TaxMapping(
            id=tax["id"],
            source=TaxMappingSourceData(
                url=tax["source"]["web"]["url"],
                term=tax["terms"]["term_name"],
                tax_id=tax["tax_id"]["taxonomy_id"],
                tax_name=tax["tax_name"]["taxonomy_name"],
            ),
        )
        for tax in data
    ]
