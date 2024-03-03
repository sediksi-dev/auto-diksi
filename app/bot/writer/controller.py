import requests
import random

from typing import List

from .models.articles import (
    ArticleData,
    ArticleMap,
    ArticleRewrited,
    ArticleDataFromSource,
)

from modules.supabase.db import db
from modules.preprocessor.config import PreProcess
from modules.ai.main import AI
from modules.ai.models import ArticleToArticleInput

ai = AI()


class BotRewriter(PreProcess):
    def __init__(self):
        super().__init__()
        self.__draft: List[ArticleData] = []
        self.__rewrited: List[ArticleRewrited] = []
        self.__source_data: List[ArticleDataFromSource] = []
        self.__images = []
        self.__video_links = []

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
        self.__draft = [ArticleData(**article) for article in response]

    def __get_articles_from_db(self, count=1) -> List[ArticleData]:
        data = self.__draft.copy()
        random.shuffle(data)
        results = data[:count]
        return results

    def __serialize_map(self, v: List[ArticleMap]):
        taxonomies = []
        source = "https://" + "/".join(
            [
                v[0].item.source.endpoint.host,
                v[0].item.source.endpoint.path,
                v[0].item.source.endpoint.type,
            ]
        )
        target = "https://" + "/".join(
            [
                v[0].item.target.endpoint.host,
                v[0].item.target.endpoint.path,
                v[0].item.target.endpoint.type,
            ]
        )
        language = {
            "from": v[0].item.source.endpoint.lang,
            "to": v[0].item.target.endpoint.lang,
        }
        for i in v:
            taxonomies.append(
                {"term": i.item.target.term, "tax_id": i.item.target.tax_id}
            )
        formated_tax = {}
        for i in taxonomies:
            if i["term"] in formated_tax:
                formated_tax[i["term"]].append(i["tax_id"])
            else:
                formated_tax[i["term"]] = [i["tax_id"]]

        results = {
            "source": source,
            "target": target,
            "language": language,
            "target_taxonomies": formated_tax,
        }
        return results

    def __content_cleaner(self, content: str) -> str:
        content = self.clean_html(content)
        return content

    def __get_source_data(self, article: ArticleData) -> ArticleDataFromSource:
        article
        id = article.id
        post_id = article.post_id
        article_map = self.__serialize_map(article.map)
        source = article_map["source"] + "/" + str(post_id)
        target = article_map["target"]
        language = article_map["language"]

        try:
            response = requests.get(source)
            response_data = response.json()
            data = ArticleDataFromSource(
                id=id,
                source=source,
                target=target,
                language=language,
                data=response_data,
            )
            self.__source_data.append(data)
            return data
        except Exception as e:
            raise e

    def __rewrite(self, article_data: ArticleDataFromSource) -> ArticleRewrited:
        draft_id = article_data.id
        content = self.__content_cleaner(article_data.data["content"]["rendered"])
        lang_source = article_data.language["from"]
        lang_target = article_data.language["to"]
        try:
            new_article = ai.article_to_article(
                ArticleToArticleInput(
                    original_article=content,
                    lang_target=lang_target,
                    lang_source=lang_source,
                )
            )

            return ArticleRewrited(
                id=draft_id,
                rewrited=new_article,
            )

        except Exception as e:
            raise e

    def write(self, count: int = 1):
        response = self.__get_articles_from_db(count)
        for article in response:
            self.__get_source_data(article)
        results = [self.__rewrite(article) for article in self.__source_data]
        return results
