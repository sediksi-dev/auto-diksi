import requests
from modules.supabase.query.get_drafted_article import (
    get_drafted_article,
    get_credentials_by_host,
)
import markdown as md
from .models import WpPostData
from app.bot.models import PostToWpArgs


class WP:
    def __init__(self):
        pass

    def __get_target(self, draft_id: int):
        try:
            data = get_drafted_article(draft_id)
        except Exception as e:
            data = {"error": e}

        target = []

        for m in data.map:
            target.append(
                {
                    "url": f"https://{m.item.target.endpoint.host}/{m.item.target.endpoint.path}/{m.item.target.endpoint.type}",
                    "id": m.item.target.tax_id,
                    "term": m.item.target.term,
                }
            )

        host = data.map[0].item.target.endpoint.host
        credentials = get_credentials_by_host(host)

        result = {}
        for item in target:
            # Ambil nilai term dan id dari item saat ini
            term = item["term"]
            id = item["id"]
            # Jika term belum ada di dictionary result, tambahkan dengan list yang berisi id
            if term not in result:
                result[term] = f"{id}"
            else:
                # Jika term sudah ada, tambahkan id ke list yang ada
                result[term] = f"{result[term]},{id}"

        return {
            "target_url": target[0].get("url"),
            "taxonomies": result,
            "credentials": credentials,
        }

    def __upload_media(self, host: str, img_url: str):
        pass

    def post_to_wp(self, draft_id: int, data: PostToWpArgs = None):
        target = self.__get_target(draft_id)
        credentials = target.get("credentials")
        url = target.get("target_url")
        tax = target.get("taxonomies")
        body = WpPostData(
            title=data["title"],
            content=md.markdown(data["content"]),
            excerpt=data["excerpt"],
            status=data["status"],
            categories=tax.get("categories") if tax.get("categories") else "",
            tags=tax.get("tags") if tax.get("tags") else "",
        )
        try:
            response = requests.post(
                url,
                auth=(credentials["user"], credentials["pass"]),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                },
                data=body.model_dump_json(),
            )

            return {
                "target": target,
                "response": response.json(),
            }
        except Exception as e:
            return {"error": e}
