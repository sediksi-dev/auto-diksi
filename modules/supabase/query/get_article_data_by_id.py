from pydantic import (
    BaseModel,
    field_serializer,
    field_validator,
    # ConfigDict,
)
from datetime import datetime
from typing import (
    List,
    Dict,
    Any,
    Literal,
    # Union,
)
from enum import Enum
from modules.supabase.db import db
from helpers import error_handling as err


class WebConfigKeys(str, Enum):
    language = "language"
    status = "status"
    mode = "mode"
    post_status = "post_status"
    rewrite_mode = "rewrite_mode"


class Web(BaseModel):
    id: int
    host: str
    api_endpoint: str
    path: str
    config: Dict[WebConfigKeys, Any]


class Taxonomies(BaseModel):
    term_name: str
    tax_id: int
    tax_name: str
    web: Web


class TaxMapping(BaseModel):
    map_id: int
    taxonomies: Taxonomies


class ArticleDataModel(BaseModel):
    draft_id: int
    wp_post_id: int
    original_title: str
    original_url: str
    published_date: datetime
    source: List[TaxMapping] = []
    target: List[TaxMapping] = []

    @field_validator("source")
    @classmethod
    def source_url_must_be_single(cls, value: List[TaxMapping]) -> List[TaxMapping]:
        hosts = set(item.taxonomies.web.host for item in value)
        if len(hosts) == 0:
            raise ValueError("Multiple source urls found for article.")
        return value

    @field_validator("source", "target")
    @classmethod
    def cannot_be_blanks(cls, value: List[TaxMapping]) -> List[TaxMapping]:
        if len(value) == 0:
            raise ValueError("Multiple source urls")
        return value

    @field_serializer("source")
    def source_serializer(self, value: List[TaxMapping]):
        web = value[0].taxonomies.web
        taxonomies = {}
        for v in value:
            tax = v.taxonomies
            if tax.term_name not in taxonomies:
                taxonomies[tax.term_name] = []
            taxonomies[tax.term_name].append({"id": tax.tax_id, "name": tax.tax_name})

        return {
            "web_id": web.id,
            "host": web.host,
            "path": web.path,
            "api_endpoint": "https://{}/{}".format(web.host, web.api_endpoint),
            "config": web.config,
            "taxonomies": taxonomies,
        }

    @field_serializer("target")
    def target_serializer(self, value: List[TaxMapping]):
        web = []
        for v in value:
            taxonomies = {}
            web_id = v.taxonomies.web.id
            web_host = v.taxonomies.web.host
            web_path = v.taxonomies.web.path
            web_config = v.taxonomies.web.config

            endpoint = "https://{}/{}".format(
                v.taxonomies.web.host, v.taxonomies.web.api_endpoint
            )
            tax = v.taxonomies
            if tax.term_name not in taxonomies:
                taxonomies[tax.term_name] = []
            taxonomies[tax.term_name].append({"id": tax.tax_id, "name": tax.tax_name})

            web.append(
                {
                    "web_id": web_id,
                    "host": web_host,
                    "path": web_path,
                    "api_endpoint": endpoint,
                    "config": web_config,
                    "taxonomies": taxonomies,
                }
            )

        merged_data = []
        for item in web:
            id = item["web_id"]
            if id not in [i["web_id"] for i in merged_data]:
                merged_data.append(
                    {
                        "web_id": id,
                        "host": item["host"],
                        "api_endpoint": item["api_endpoint"],
                        "path": item["path"],
                        "config": item["config"],
                        "taxonomies": item["taxonomies"],
                    }
                )
            else:
                for i in merged_data:
                    if i["web_id"] == id:
                        for key, value in i["taxonomies"].items():
                            if key in item["taxonomies"]:
                                i["taxonomies"][key].extend(item["taxonomies"][key])
                            else:
                                i["taxonomies"][key] = item["taxonomies"][key]

        return merged_data


def res_validation(res):

    if res is None:
        raise err.DatabaseException(f"No data found for article with id {id}.")

    if len(res.data["source_tax"]) is None:
        raise err.DatabaseException(f"No source tax found for article with id {id}.")

    source_url = list(
        set([item["item"]["tax"]["web"]["url"] for item in res.data["source_url"]])
    )

    if len(source_url) > 1:
        raise err.DatabaseException(
            f"Multiple source urls found for article with id {id}."
        )

    if len(source_url) == 0:
        raise err.DatabaseException(f"No source url found for article with id {id}.")

    return source_url


def get_web_query(t: Literal["source", "target"]):
    web = "web_id(*, config: web_config(*))"
    tax_data = " {}_id(*, web: {})".format(t, web)
    tax_mapping = "taxonomy_mapping(*, tax:{})".format(tax_data)
    tax = "articles_mapping(*, item: {})".format(tax_mapping)
    return tax


def config_to_dict(config: list[dict], exclude: list[str] = []):
    exclude += ["auth_username", "auth_token"]
    cfg = {}

    for item in config:
        if item["key"] not in exclude:
            cfg[item["key"]] = item["value"]
    return cfg


def format_web_item(role_key: Literal["target", "source"], data: list[dict]):
    return (
        {
            "map_id": data["id"],
            "taxonomies": {
                "term_name": data["item"]["tax"]["term_name"],
                "tax_id": data["item"]["tax"]["taxonomy_id"],
                "tax_name": data["item"]["tax"]["taxonomy_name"],
                "web": {
                    "id": data["item"]["tax"]["web"]["id"],
                    "host": data["item"]["tax"]["web"]["url"],
                    "api_endpoint": data["item"]["tax"]["web"]["api_endpoint"],
                    "path": data["item"]["tax"]["web"]["post_type"],
                    "config": config_to_dict(data["item"]["tax"]["web"]["config"]),
                },
            },
        }
        for data in data[role_key]
    )


def format_data(data):
    formatted_data = {
        "draft_id": data["id"],
        "wp_post_id": data["original_id"],
        "original_title": data["post_title"],
        "original_url": data["source_url"],
        "published_date": data["published_date"],
        "source": format_web_item("source", data),
        "target": format_web_item("target", data),
    }
    return formatted_data


def get_article_data_by_id(id: int = None, status: str = None):
    source_tax = get_web_query("source")
    target_tax = get_web_query("target")
    query = (
        "*",
        "source: {}".format(source_tax),
        "target:{}".format(target_tax),
    )
    drafter = db.table("articles").select(*query)
    if status is not None:
        drafter = drafter.eq("status", status)

    if id is not None:
        drafter = drafter.eq("id", id)

    res = drafter.limit(1).maybe_single().execute()

    try:
        results = format_data(res.data)
        return ArticleDataModel.model_validate(results)
    except Exception as e:
        raise err.DatabaseException(f"Error validating article data >>> {str(e)}")
