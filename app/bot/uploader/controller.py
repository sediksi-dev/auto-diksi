from modules.wp.main import WP

from app.bot.models import PostToWpArgs


class BotUploader(WP):
    def __init__(self):
        super().__init__()

    def get_tax(self, draft_id: int):
        return self._get_article_map(draft_id)

    def post(self, data: PostToWpArgs):
        return self._post_to_wp(data)
