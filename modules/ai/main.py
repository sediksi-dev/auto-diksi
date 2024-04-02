from .models import (
    ArticleToArticleInput,
    ArticleToArticleOutput,
    KeywordToArticleInput,
    KeywordToArticleOutput,
)

from .flows.bot_default_mode import bot_default_rewriter
from .flows.seeder_default_mode import seeder_default_rewriter
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
            return bot_default_rewriter(args)
        else:
            raise ValueError("Invalid mode")

    def keyword_to_article(
        self, mode: str, args: KeywordToArticleInput
    ) -> KeywordToArticleOutput:
        if mode == "default":
            return seeder_default_rewriter(args)
        else:
            raise ValueError("Invalid mode")
