from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import urllib.parse
import json


class BingImage:
    def __get_soup(self, url: str, header: dict):
        return BeautifulSoup(
            urllib.request.urlopen(urllib.request.Request(url, headers=header)),
            "html.parser",
        )

    def __bing_image_search(self, query: str):
        query = query.split()
        query = "+".join(query)
        url = f"http://www.bing.com/images/search?q={query}&qft=+filterui:imagesize-custom_900_400+filterui:aspect-wide"
        uagent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        # add the directory for your image here
        header = {
            "User-Agent": uagent,
        }
        soup = self.__get_soup(url, header)
        image_result_raw = soup.find_all("a", {"class": "iusc"})
        images = []
        for a in image_result_raw:
            m = json.loads(a["m"])
            murl = m["murl"]
            images.append(murl)
        return images

    def get_images(self, count=5, max_result=10, **keywords: str):
        images = []

        for key, value in keywords.items():
            try:
                results = self.__bing_image_search(
                    value.encode("ascii", "ignore").decode()
                )
                images += results[:count]
            except Exception as e:
                print(f"Error searching images for {key}: {value}: {e}")

        set_images = set(images)
        list_images = list(set_images)
        if len(list_images) > max_result:
            list_images = list_images[:max_result]
        return list_images
