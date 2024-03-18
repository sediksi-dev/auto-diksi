from pydantic import BaseModel, model_serializer
from typing import Literal, List
from modules.supabase.query.get_taxonomy_map_by_draft_id import TaxonomyMap


class WpPostData(BaseModel):
    title: str
    content: str
    excerpt: str
    status: Literal["publish", "draft"] = "draft"
    taxonomies: List[TaxonomyMap]
    featured_media: int = None

    @model_serializer()
    def serialize_model(self):
        taxonomies = {}
        for tax in self.taxonomies:
            if tax.term not in taxonomies:
                taxonomies[tax.term] = f"{tax.tax_id}"
            else:
                taxonomies[tax.term] += f",{tax.tax_id}"

        return {
            "title": self.title,
            "content": self.content,
            "excerpt": self.excerpt,
            "status": self.status,
            "featured_media": self.featured_media,
            **taxonomies,
        }
