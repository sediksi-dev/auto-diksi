import requests
import random

from typing import List

from .models.articles import ArticleData

from modules.supabase.db import db
from modules.preprocessor.config import PreProcess
from modules.ai.main import AI
from modules.ai.models import ArticleToArticleInput

ai = AI()


class BotWriter(PreProcess):
    def __init__(self):
        super().__init__()
        self.draft = []
        self.__get_drafted_posts()

    def __get_drafted_posts(self) -> None:
        target = "target_id(term:term_name, tax_id:taxonomy_id, endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
        source = "source_id(endpoint:web_id(host:url, path:api_endpoint, type:post_type, lang: language))"
        query = (
            "id: id",
            "title: post_title",
            "post_id: original_id",
            f"map: articles_mapping(item:taxonomy_mapping(source:{source}, target:{target}))",
        )

        res, _ = db.table("articles").select(*query).eq("status", "draft").execute()
        response = res[1]
        self.draft = [ArticleData(**article) for article in response]

    def __format_responses(self, count=1) -> List[ArticleData]:
        data = self.draft.copy()
        random.shuffle(data)
        results = data[:count]
        return results

    def __content_cleaner(self, content: str) -> str:
        content = self.clean_html(content)
        return content

    def __rewrite(self, article: ArticleData) -> None:
        article_data = article.model_dump()
        post_id = article_data["post_id"]
        source = article_data["map"]["source"] + "/" + str(post_id)
        target = article_data["map"]["target"]
        language = article_data["map"]["language"]
        lang_target = language["to"]
        lang_source = language["from"]

        try:
            response = requests.get(source)
            data = response.json()
            content = data["content"]["rendered"]
            content = self.__content_cleaner(content)
            new_article = ai.article_to_article(
                ArticleToArticleInput(
                    original_article=content,
                    lang_target=lang_target,
                    lang_source=lang_source,
                )
            )

            return {
                "source": source,
                "target": target,
                "language": language,
                "results": new_article,
            }
        except Exception as e:
            raise e

    def write(self, count: int = 1):
        response = self.__format_responses(count)
        results = []
        for article in response:
            new_article = self.__rewrite(article)
            results.append(new_article)
        return results
