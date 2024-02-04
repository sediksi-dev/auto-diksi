from modules.bot.config import Bot
from modules.bot.schema import Config

config = Config(
    target="https://cuakz.com",
    source="https://allthatsinteresting.com",
    username="CUAKZ_USERNAME",
    password="CUAKZ_PASSWORD",
    taxonomies=[
        {
            "source": {
                "term_name": "category",
                "id": 1,
                "name": "news",
                "slug": "news",
            },
            "target": {
                "term_name": "category",
                "id": 1,
                "name": "berita",
                "slug": "berita",
            },
        },
        {
            "source": {
                "term_name": "category",
                "id": 2,
                "name": "entertainment",
                "slug": "entertainment",
            },
            "target": {
                "term_name": "category",
                "id": 2,
                "name": "hiburan",
                "slug": "hiburan",
            },
        },
    ],
    post_options={"status": "publish", "author_id": 1},
)


cuakz = Bot(config)
