from modules.supabase.db import db
from helper.error_handling import error_handler


@error_handler("db", "Error when getting web config")
def get_web_config(host: str) -> dict:
    query = ("key:key", "value:value", "web:web_id!inner(url:url)")
    res, _ = db.table("web_config").select(*query).eq("web.url", host).execute()

    result = res[1]
    web_config = {}
    for item in result:
        web_config[item["key"]] = item["value"]

    return web_config
