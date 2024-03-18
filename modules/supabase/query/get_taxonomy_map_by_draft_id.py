from pydantic import BaseModel
from modules.supabase.db import db


class TaxonomyMap(BaseModel):
    id: int
    term: str
    tax_name: str
    tax_id: int


def get_taxonomy_map_by_draft_id(draft_id: int):
    table_name = "articles_mapping"
    query = (
        "id",
        "tax:taxonomy_mapping_id!inner(target: target_id(term: term_name, id: taxonomy_id, name: taxonomy_name))",
    )

    res, _ = db.table(table_name).select(*query).eq("articles_id", draft_id).execute()
    response = res[1]
    return [
        TaxonomyMap(
            id=int(tax["id"]),
            term=tax["tax"]["target"]["term"],
            tax_name=tax["tax"]["target"]["name"],
            tax_id=tax["tax"]["target"]["id"],
        )
        for tax in response
    ]
