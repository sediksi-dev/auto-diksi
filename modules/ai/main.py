from .models import ArticleToArticleInput, ArticleToArticleOutput

from .flows.default_mode import default_rewriter
from .tasks.create_search_image_query import create_search_image_query


class AI:
    def __init__(self):
        pass

    def article_to_image_query(self, article: str) -> str:
        return create_search_image_query(article)

    def article_to_article(
        self, mode: str, args: ArticleToArticleInput
    ) -> ArticleToArticleOutput:
        if mode == "default":
            return default_rewriter(args)
        else:
            raise ValueError("Invalid mode")
