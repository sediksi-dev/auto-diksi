from .models import ArticleToArticleInput, ArticleToArticleOutput

from .flows.default_mode import default_rewriter


class AI:
    def __init__(self):
        pass

    # def __modify_outline(self, outline: OutlineArticle) -> str:
    #     subheadings = "\n".join(
    #         [f"- {section.subheading}" for section in outline.sections]
    #     )
    #     return subheadings

    def article_to_article(
        self, mode: str, args: ArticleToArticleInput
    ) -> ArticleToArticleOutput:
        if mode == "default":
            return default_rewriter(args)
        else:
            raise ValueError(f"Invalid mode: {mode}")
