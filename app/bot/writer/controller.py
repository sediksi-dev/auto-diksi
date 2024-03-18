import requests

from typing import List

from .models import (
    ArticleDataFromSource,
    ArticleWriteOutputRaw,
    FeaturedMediaData,
    ArticleWriteOutput,
)

from modules.supabase.query.get_drafted_article import get_drafted_article
from modules.supabase.query.get_web_config_by_id import get_web_config_by_id
from modules.supabase.query.models.drafted_article import (
    ArticleMap,
    DraftedArticle,
)

from modules.preprocessor.config import PreProcess
from modules.ai.main import AI
from modules.ai.models import ArticleToArticleInput, ArticleToArticleOutput


ai = AI()


class BotRewriter(PreProcess):
    def __init__(self, id: int = None):
        super().__init__()
        self.__draft_id: int = id
        self.__draft: DraftedArticle = self.__get_drafted_posts(self.__draft_id)
        self.__draft_data: ArticleDataFromSource = self.__get_source_data(self.__draft)

    def __get_drafted_posts(self, id) -> DraftedArticle:
        article_db = get_drafted_article(id)
        if self.__draft_id is None:
            self.__draft_id = article_db.id
        return article_db

    def __get_source_data(self, article: DraftedArticle) -> ArticleDataFromSource:
        post_id = article.post_id
        mapping = article.map
        article_map = self.__serialize_map(mapping)
        source = article_map["source"] + "/" + str(post_id)
        target = article_map["target"]
        language = article_map["language"]

        response = requests.get(source)
        response.raise_for_status()
        response_data = response.json()
        data = ArticleDataFromSource(
            language=language,
            source=source,
            target=target,
            wp_data=response_data,
        )
        return data

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

    def __featured_media_handler(
        self, id: int, host: str, path: str
    ) -> FeaturedMediaData:
        results = self.get_featured_image_link(id, host, path)
        return FeaturedMediaData(**results)

    def __rewrite(
        self, mode, source_data: ArticleDataFromSource
    ) -> ArticleToArticleOutput:
        content = self.__content_cleaner(source_data.wp_data["content"]["rendered"])
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
            return new_article

        except Exception as e:
            return str(e)

    def write(self) -> ArticleWriteOutput:
        id = self.__draft_id
        mode = get_web_config_by_id(id, "mode")
        draft = self.__draft
        data = self.__draft_data
        featured_media = self.__featured_media_handler(
            data.wp_data["featured_media"],
            draft.map[0].item.source.endpoint.host,
            draft.map[0].item.source.endpoint.path,
        )

        result = self.__rewrite(mode, data)

        return ArticleWriteOutput(
            draft_id=id,
            raw=ArticleWriteOutputRaw(
                title=draft.title,
                post_id=draft.post_id,
                link=data.wp_data["link"],
                languange=data.language,
            ),
            result=result,
            featured_media=featured_media,
        )
