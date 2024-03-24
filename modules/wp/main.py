import requests
from requests.auth import HTTPBasicAuth
import markdown as md
import os

import json
from datetime import datetime
from modules.supabase.query.get_article_data_by_id import get_article_data_by_id
from modules.supabase.query.get_credentials_by_host import (
    get_credentials_by_host,
    Credentials,
)
from modules.supabase.query.update_article import update_article

from .models import WpPostData, TargetData
from app.bot.schemas import PostToWpArgs, FeaturedMediaData

from helpers import error_handling as err


class WP:
    def __init__(self):
        self.__data = None
        pass

    def __get_target_data(self, draft_id: int):
        try:
            data = get_article_data_by_id(draft_id)
            data = data.model_dump()
            self.__data = data
            host = data["target"][0]["host"]
            endpoint = data["target"][0]["api_endpoint"]
            path = data["target"][0]["path"]
            credentials: Credentials = get_credentials_by_host(host)

            return TargetData.model_validate(
                {
                    "web": {
                        "host": host,
                        "api_endpoint": endpoint,
                        "path": path,
                    },
                    "credentials": credentials,
                }
            )
        except Exception as e:
            raise err.DatabaseException(f"Error drafted article data >>> {str(e)}")

    def __format_taxonomies(self):
        target_data = self.__data
        taxonomies = {}
        for key, value in target_data["target"][0]["taxonomies"].items():
            taxonomies[key] = ", ".join([str(tax["id"]) for tax in value])
        return taxonomies

    def __get_target_post_status(self):
        data = self.__data
        post_status = data["target"][0]["config"]["post_status"]
        return post_status

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
            raise err.WpException(f"Error downloading image >>> {str(e)}")

    def __remove_img_temp(self, filename: str):
        os.remove(filename)

    def __upload_media(self, target: TargetData, media: FeaturedMediaData):
        target_url = target.web.api_endpoint + "/media"
        credentials = target.credentials
        filename = self.__download_img_temp(media.url)
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
            print("Failed to upload image. Reason: ", str(e))
            return None

    def __update_draft_status(self, draft_id, status: str, **kwargs):
        if status == "error":
            data = update_article(draft_id, data={"status": "error"})
        else:
            data = update_article(draft_id, data={"status": status, **kwargs})
        return data

    def _post_to_wp(self, payload: PostToWpArgs):
        draft_id = payload.draft_id
        data = payload.body
        featured_media = payload.featured_media
        target = self.__get_target_data(draft_id)
        url = target.web.api_endpoint + "/" + target.web.path
        credentials = target.credentials

        try:
            body = WpPostData(
                title=data.title,
                content=md.markdown(data.content),
                excerpt=data.excerpt,
                status=self.__get_target_post_status(),
                taxonomies=self.__format_taxonomies(),
            )

            featured_media_id = self.__upload_media(target, featured_media)
            if featured_media_id is not None:
                body.featured_media = featured_media_id

            response = requests.post(
                url,
                auth=(credentials.user, credentials.pass_),
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                },
                data=json.dumps(body.model_dump()),
            )

            result_data = response.json()

            link = (
                result_data.get("link", "")
                if result_data.get("link") not in ["", None]
                else result_data.get("guid").get("rendered")
            )

            self.__update_draft_status(
                draft_id,
                "published",
                public_url=link,
                post_id=result_data["id"],
            )

            return result_data
        except Exception as e:
            raise err.WpException(f"Error posting to WordPress >>> {str(e)}")
