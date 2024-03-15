import requests
import random

from typing import List

from .models.articles import (
    ArticleData,
    ArticleMap,
    ArticleRewrited,
    ArticleDataFromSource,
    FeaturedMediaData,
    ImagesData,
    IframeData,
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
        self.__source_data: List[ArticleDataFromSource] = []
        self.__rewrited: List[ArticleRewrited] = []
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
        raw = {
            "source": {
                "host": v[0].item.source.endpoint.host,
                "path": v[0].item.source.endpoint.path,
            },
            "target": {
                "host": v[0].item.target.endpoint.host,
                "path": v[0].item.target.endpoint.path,
            },
        }

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
            "raw": raw,
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
        mapping = article.map
        article_map = self.__serialize_map(article.map)
        source = article_map["source"] + "/" + str(post_id)
        target = article_map["target"]
        language = article_map["language"]

        try:
            response = requests.get(source)
            response_data = response.json()
            data = ArticleDataFromSource(
                id=id,
                mapping=mapping,
                source=source,
                target=target,
                language=language,
                data=response_data,
            )
            self.__source_data.append(data)
            return data
        except Exception as e:
            raise e

    def __rewrite(self, mode, source_data: ArticleDataFromSource) -> ArticleRewrited:
        draft_id = source_data.id
        content = self.__content_cleaner(source_data.data["content"]["rendered"])
        lang_source = source_data.language["from"]
        lang_target = source_data.language["to"]
        try:
            new_article = ai.article_to_article(
                mode=mode,
                args=ArticleToArticleInput(
                    original_article=content,
                    lang_target=lang_target,
                    lang_source=lang_source,
                ),
            )

            rewrited = {
                "id": draft_id,
                "result": new_article,
            }
            self.__rewrited.append(rewrited)
            return rewrited

        except Exception as e:
            raise e

    def __article_formater(
        self,
        article: ArticleRewrited
    ):
        pass

    def __image_handler(self, source_data: ArticleDataFromSource):
        draft_id = source_data.id
        mapping = self.__serialize_map(source_data.mapping)["raw"]
        source = mapping["source"]["host"]
        path = mapping["source"]["path"]
        featured_media_id: int = source_data.data["featured_media"]
        featured_media_data: FeaturedMediaData = self.get_featured_image_link(
            featured_media_id, source, path=path
        )
        image_links = self.get_image_links(source_data.data["content"]["rendered"])

        return ImagesData(
            id=draft_id,
            source=source,
            featured_media=FeaturedMediaData(**featured_media_data),
            body_images=image_links,
        )

    def __iframe_handler(self, source_data: ArticleDataFromSource):
        draft_id = source_data.id
        mapping = self.__serialize_map(source_data.mapping)["raw"]
        source = mapping["source"]["host"]
        iframe = self.get_iframe(source_data.data["content"]["rendered"])

        return IframeData(
            id=draft_id,
            source=source,
            link=iframe,
        )

    def write(self, mode: str, count: int = 1):
        response = self.__get_articles_from_db(count)
        results = []
        for article in response:
            self.__get_source_data(article)
        for article in self.__source_data:
            rewrited = self.__rewrite(mode, article)
            images = self.__image_handler(article)
            results.append(
                {
                    "content": rewrited,
                    "featured_media": images.featured_media,
                }
            )
        return results
