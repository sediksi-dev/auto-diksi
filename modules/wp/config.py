from pydantic import HttpUrl
from modules.wp.schema import (
    WpBaseUrl,
    WpEndpoint,
    WpChangeEndpoint,
    WpPostResponse,
    WpRequestsError,
)
from modules.preprocessor.config import PreProcess
import requests
from typing import List


class WpConfig:
    def __init__(self, **data):
        self.__base_url: WpBaseUrl = WpBaseUrl(
            source=data.get("source"), target=data.get("target")
        )
        self._endpoint: WpChangeEndpoint = {
            "source": "wp-json/wp/v2",
            "target": "wp-json/wp/v2",
        }

    @property
    def endpoint(self) -> WpChangeEndpoint:
        return self._endpoint

    def __cleaning(self, content: str):
        preprocess = PreProcess(content)
        markdown = preprocess.processed_content["markdown"]
        return markdown

    def _url(self, get_base_from: WpEndpoint, post_type: str = "posts") -> HttpUrl:
        base_url = getattr(self.__base_url, get_base_from)
        endpoint = self._endpoint[get_base_from]

        url = f"{base_url}/{endpoint}/{post_type}"
        return url

    def change_endpoint(self, endpoint_type: WpEndpoint, val: str):
        self._endpoint[endpoint_type] = val

    def get_posts(
        self, _from: WpEndpoint, post_type: str = "posts", **kwargs
    ) -> List[WpPostResponse]:
        url = self._url(_from, post_type)
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
        except Exception as e:
            raise WpRequestsError(str(e), response.status_code)

        # clean the content
        posts = response.json()
        for post in posts:
            post["content"]["rendered"] = self.__cleaning(post["content"]["rendered"])
            post["excerpt"]["rendered"] = self.__cleaning(post["excerpt"]["rendered"])
            post["title"]["rendered"] = self.__cleaning(post["title"]["rendered"])
        return posts
