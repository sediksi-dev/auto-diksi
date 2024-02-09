from bs4 import BeautifulSoup
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
