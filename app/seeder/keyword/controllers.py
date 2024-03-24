from modules.ai.main import AI
from modules.ai.models import KeywordToArticleInput


class SeederKeyword:
    def __init__(self):
        pass

    def generate(self, keyword: str, lang_target: str, mode: str = "default"):
        ai = AI()
        return ai.keyword_to_article(
            mode=mode,
            args=KeywordToArticleInput(keyword=keyword, lang_target=lang_target),
        )
