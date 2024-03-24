from modules.wp.main import WP


class BotHelper:
    def __init__(self, path, **kwargs):
        self.__path = path
        self.__kwargs = kwargs

    def run(self):
        if self.__path == "target-data":
            draft_id = self.__kwargs.get("draft_id", None)
            if draft_id is None:
                raise ValueError("Draft ID is required.")
            return self.__get_wp_target(draft_id)

        raise ValueError("Path not found.")

    def __get_wp_target(self, draft_id: int):
        wp = WP()
        return wp.get_target(draft_id)
