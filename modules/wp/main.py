import requests
from requests.auth import HTTPBasicAuth
import markdown as md
import os

# import json
from datetime import datetime
from modules.supabase.query.get_drafted_article import get_drafted_article
from modules.supabase.query.get_web_by_host import get_web_by_host, Credentials, WebData
from modules.supabase.query.get_taxonomy_map_by_draft_id import (
    get_taxonomy_map_by_draft_id,
)
from modules.supabase.query.update_article import update_article

from .models import WpPostData
from app.bot.models import PostToWpArgs, FeaturedMediaData


class WP:
    def __init__(self):
        pass

    def __get_target(self, draft_id: int):
        try:
            data = get_drafted_article(draft_id)
            host = data.map[0].item.target.endpoint.host
            target = get_web_by_host(host)
            credentials = target.credentials
            web = target.web
            api_url = f"https://{web.host}/{web.path}/{web.type}"

            return {
                "web": web,
                "target_url": api_url,
                "credentials": credentials,
            }
        except Exception as e:
            raise e

    def __download_img_temp(self, url: str):
        try:
            img_data = requests.get(url).content
            filename = "modules/wp/temp/img-{}.png".format(
                datetime.now().strftime("%Y%m%d%H%M%S")
            )

            with open(filename, "wb") as handler:
                handler.write(img_data)
                handler.close()

            return filename
        except Exception as e:
            print("Failed to download image. Msg: ", str(e))
            return None

    def __remove_img_temp(self, filename: str):
        os.remove(filename)

    def __upload_media(
        self, web: WebData, credentials: Credentials, media: FeaturedMediaData
    ):
        target_url = f"https://{web.host}/{web.path}/media"
        filename = self.__download_img_temp(media.url)

        if filename is None:
            return None

        try:
            with open(filename, "rb") as img:
                response = requests.post(
                    target_url,
                    auth=HTTPBasicAuth(credentials.user, credentials.pass_),
                    files={"file": (filename, img)},
                    data={
                        "title": media.title,
                        "caption": media.caption,
                        "alt_text": media.alt,
                    },
                    headers={
                        "User-Agent": "Mozilla/5.0",
                    },
                )
            self.__remove_img_temp(filename)
            json_data = response.json()
            return json_data["id"]
        except Exception as e:
            print("Failed to upload image. Message: ", str(e))
            return None

    def __get_article_map(self, draft_id: int):
        return get_taxonomy_map_by_draft_id(draft_id)

    def __update_draft_status(self, draft_id, status: str, **kwargs):
        if status == "error":
            data = update_article(draft_id, data={"status": "error"})
        else:
            data = update_article(draft_id, data={"status": status, **kwargs})
        return data

    def _post_to_wp(self, payload: PostToWpArgs):
        draft_id = payload.draft_id
        data = payload.body

        target = self.__get_target(draft_id)
        tax = self.__get_article_map(draft_id)

        web: WebData = target.get("web")
        url = target.get("target_url")
        credentials: Credentials = target["credentials"]

        try:
            featured_media_id = self.__upload_media(
                web, credentials, payload.featured_media
            )
            body = WpPostData(
                title=data.title,
                content=md.markdown(data.content),
                excerpt=data.excerpt,
                status=data.status,
                taxonomies=tax,
                featured_media=featured_media_id,
            )

            response = requests.post(
                url,
                auth=(credentials.user, credentials.pass_),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                },
                data=body.model_dump_json(),
            )

            result_data = response.json()
            self.__update_draft_status(
                draft_id,
                "published",
                public_url=result_data["link"],
                post_id=result_data["id"],
            )
            return result_data
        except Exception as e:
            self.__update_draft_status(draft_id, "error")
            return {"error": str(e)}
