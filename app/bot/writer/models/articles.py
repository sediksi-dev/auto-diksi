from pydantic import BaseModel, field_serializer
from typing import List


class Endpoint(BaseModel):
    host: str
    path: str
    type: str
    lang: str


class Source(BaseModel):
    endpoint: Endpoint


class Target(BaseModel):
    term: str
    tax_id: int
    endpoint: Endpoint


class Item(BaseModel):
    source: Source
    target: Target


class ArticleMap(BaseModel):
    item: Item


class ArticleData(BaseModel):
    id: int
    title: str
    post_id: int
    map: List[ArticleMap]

    @field_serializer("map", when_used="always")
    def serialize_map(v: List[ArticleMap]):
        taxonomies = []
        source = "https://" + "/".join(
            [
                v[0].item.source.endpoint.host,
                v[0].item.source.endpoint.path,
                v[0].item.source.endpoint.type,
            ]
        )
        target = "https://" + "/".join(
            [
                v[0].item.target.endpoint.host,
                v[0].item.target.endpoint.path,
                v[0].item.target.endpoint.type,
            ]
        )
        language = {
            "from": v[0].item.source.endpoint.lang,
            "to": v[0].item.target.endpoint.lang,
        }
        for i in v:
            taxonomies.append(
                {"term": i.item.target.term, "tax_id": i.item.target.tax_id}
            )
        formated_tax = {}
        for i in taxonomies:
            if i["term"] in formated_tax:
                formated_tax[i["term"]].append(i["tax_id"])
            else:
                formated_tax[i["term"]] = [i["tax_id"]]

        results = {
            "source": source,
            "target": target,
            "language": language,
            "target_taxonomies": formated_tax,
        }
        return results
