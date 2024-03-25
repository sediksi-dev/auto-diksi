from modules.supabase.db import db
from pydantic import BaseModel, Field
from helpers.error_handling import error_handler


class Credentials(BaseModel):
    user: str
    pass_: str = Field(..., alias="pass")


def get_web_config(host: str) -> dict:
    query = ("key:key", "value:value", "web:web_id!inner(url:url)")
    res, _ = db.table("web_config").select(*query).eq("web.url", host).execute()

    result = res[1]
    web_config = {}
    for item in result:
        web_config[item["key"]] = item["value"]

    return web_config


@error_handler("db", "Error when getting credentials")
def get_credentials_by_host(host: str) -> Credentials:
    config = get_web_config(host)
    auth_username = config["auth_username"]
    auth_token = config["auth_token"]
    credentials = {
        "user": auth_username,
        "pass": auth_token,
    }

    return Credentials(**credentials)
