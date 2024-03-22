import requests

from .models import (
    ArticleDataFromSource,
    FeaturedMediaData,
    ArticleWriteOutput,
)

from helper import error_handling as err

from modules.supabase.query.get_article_data_by_id import get_article_data_by_id

from modules.preprocessor.config import PreProcess
from modules.ai.main import AI
from modules.ai.models import ArticleToArticleOutput, ArticleToArticleInput


ai = AI()


class BotRewriter(PreProcess):
    def __init__(self, draft_id: int = None):
        self.__draft_id = draft_id
        self.__data = self.__get_data()

    def __get_data(self):
        return get_article_data_by_id(self.__draft_id)

    @property
    def db_data(self):
        return self.__data

    def __fetch_wp_data(self):
        data = self.__data.model_dump()
        source_url = f"{data['source']['api_endpoint']}/{data['source']['path']}/{data['wp_post_id']}"
        target_url = f'{data["target"][0]["api_endpoint"]}/{data["target"][0]["path"]}'
        language = {
            "from": data["source"]["config"]["language"],
            "to": data["target"][0]["config"]["language"],
        }

        wp_response = requests.get(source_url)
        # wp_response.raise_for_status()
        results = wp_response.json()

        return ArticleDataFromSource(
            language=language,
            source=source_url,
            target=target_url,
            wp_data=results,
        )

    def _featured_media_handler(self, id: int, endpoint: str) -> FeaturedMediaData:
        results = self.get_featured_image_link_full(id, endpoint)
        return FeaturedMediaData(**results)

    def __writing(
        self, mode: str, source_data: ArticleDataFromSource
    ) -> ArticleToArticleOutput:
        content = self.clean_html(source_data.wp_data["content"]["rendered"])
        try:
            new_article: ArticleToArticleOutput = ai.article_to_article(
                mode=mode,
                args=ArticleToArticleInput(
                    original_article=content,
                    lang_target=source_data.language["to"],
                    lang_source=source_data.language["from"],
                ),
            )
            return new_article
        except Exception as e:
            raise err.AiResponseException(f"Gagal menulis artikel. {str(e)}")

    def rewrite(self):
        data = self.__data.model_dump()
        draft_id = data["draft_id"]
        fetched = self.__fetch_wp_data()

        featured_media = self._featured_media_handler(
            id=fetched.wp_data["featured_media"],
            endpoint=data["source"]["api_endpoint"],
        )

        mode = data["target"][0]["config"]["mode"]
        rewrited = self.__writing(mode, fetched)

        output = {
            "draft_id": draft_id,
            "raw": {
                "title": data["original_title"],
                "post_id": data["wp_post_id"],
                "link": fetched.wp_data["link"],
                "language": fetched.language,
            },
            "result": rewrited,
            "featured_media": featured_media,
        }

        try:
            results = ArticleWriteOutput.model_validate(output)
            return results
        except Exception as e:
            raise Exception(f"Gagal memvalidasi output. {str(e)}")
