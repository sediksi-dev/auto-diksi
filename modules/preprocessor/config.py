from bs4 import BeautifulSoup
from typing import List
import requests

# from markdownify import markdownify as md


class PreProcess:
    """
    PreProcess class is used to preprocess the content of the article.
    Content is the article formatted in HTML. The class will extract the
    images, headers and paragraphs count from the content. The original content
    will be stored in structured format.
    """

    def __init__(self):
        pass

    def clean_html(self, content: str) -> str:
        """
        This method will clean the HTML content and return the plain text.
        """
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text()

    def get_featured_image_link(
        self, id: int, source: str, path: str = "wp-json/wp/v2"
    ):

        url = f"https://{source}/{path}/media/{id}"
        print(url)
        response = requests.get(url)
        response_data = response.json()
        return {
            "url": response_data["guid"]["rendered"],
            "title": response_data["title"]["rendered"],
            "caption": self.clean_html(response_data["caption"]["rendered"]),
            "alt": response_data["alt_text"],
        }

    def get_featured_image_link_full(self, id: int, endpoint: str):

        url = f"{endpoint}/media/{id}"
        print(url)
        response = requests.get(url)
        response_data = response.json()
        return {
            "url": response_data["guid"]["rendered"],
            "title": response_data["title"]["rendered"],
            "caption": self.clean_html(response_data["caption"]["rendered"]),
            "alt": response_data["alt_text"],
        }

    def get_image_links(self, content: str) -> List[str]:
        """
        This method will extract the image links from the content.
        """
        soup = BeautifulSoup(content, "html.parser")
        images = soup.find_all("img")
        if len(images) > 0:
            try:
                return [image["src"] for image in images]
            except Exception as e:
                print(e)
                return []
        return []

    def get_iframe(self, content: str) -> List[str]:
        """
        This method will extract the youtube links from the content.
        """
        soup = BeautifulSoup(content, "html.parser")
        iframe = soup.find_all("iframe")
        if len(iframe) > 0:
            try:
                return [iframe["src"] for iframe in iframe]
            except Exception as e:
                print(e)
                return []
        return []
