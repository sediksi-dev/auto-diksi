from bs4 import BeautifulSoup
from markdownify import markdownify as md


class PreProcess:
    """
    PreProcess class is used to preprocess the content of the article.
    Content is the article formatted in HTML. The class will extract the
    images, headers and paragraphs count from the content. The original content
    will be stored in structured format.
    """

    def __init__(self, content: str):
        self.__content = content
        self.__cleaned_html = ""
        self.__images = []
        self.__headers = []
        self.__markdown = ""
        self.__paragraphs_count: int = 0
        self.__preprocess()

    @property
    def processed_content(self):
        return {
            "content": self.__cleaned_html,
            "images": self.__images,
            "headers": self.__headers,
            "paragraphs_count": self.__paragraphs_count,
            "markdown": self.__markdown,
        }

    def __preprocess(self):
        self.__clean_html()
        self.__extract_images()
        self.__extract_headers()
        self.__extract_markdown()
        self.__extract_paragraphs_count()

    def __clean_html(self):
        content = self.__content
        soup = BeautifulSoup(content, "html.parser")
        self.__cleaned_html = soup.prettify()

    def __extract_images(self):
        content = self.__content
        soup = BeautifulSoup(content, "html.parser")
        images = soup.find_all("img")
        for index, image in enumerate(images):
            self.__images.append(
                {
                    "src": image["src"],
                    "alt": image["alt"],
                    "position": index,
                }
            )

    def __extract_headers(self):
        content = self.__content
        soup = BeautifulSoup(content, "html.parser")
        headers = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        for index, header in enumerate(headers):
            self.__headers.append(
                {
                    "text": header.text,
                    "level": header.name,
                    "position": index,
                }
            )

    def __extract_markdown(self):
        content = self.__content
        soup = BeautifulSoup(content, "html.parser")
        # remove attributes from the tags
        for tag in soup.find_all(True):
            tag.attrs = None

        md_format = md(soup.renderContents().decode())
        # replace more one new line with one new line
        md_format = (
            md_format.replace("\n-", "-")
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("--", "")
            .replace("[]", "")
            .replace("()", "")
            .replace(r"/\s\s+/g", " ")
        )

        self.__markdown = md_format

    def __extract_paragraphs_count(self):
        content = self.__content
        self.__paragraphs_count = len(content.split("\n"))
