import os
from dotenv import load_dotenv
from modules.bot.schema import Config, Credentials
from modules.wp.config import WpConfig
from requests.auth import HTTPBasicAuth


load_dotenv()


class Bot:
    def __init__(self, data: Config):
        self.__credentials = Credentials(
            username=os.environ.get(data.username),
            password=os.environ.get(data.password),
        )
        self.__taxonomies = data.taxonomies
        self.__post_options = data.post_options
        self.__source = data.source
        self.__target = data.target

        self.__wp = WpConfig(source=data.source, target=data.target)

    @property
    def info(self) -> Config:
        return {
            "source": self.__source,
            "target": self.__target,
            "taxonomies": self.__taxonomies,
            "post_options": self.__post_options,
        }

    @property
    def credentials(self):
        return HTTPBasicAuth(self.__credentials.username, self.__credentials.password)

    @property
    def wp(self):
        return self.__wp
