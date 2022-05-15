from Base import BaseObject
from Singleton import Singleton
import inspect
import requests
import configparser
import os


class Telegram(BaseObject, metaclass=Singleton):

    def __init__(self):
        super().__init__()
        self.token = None
        self.chat_id = None
        self.link = None

        self.init_telegram()

    def init_telegram(self):
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read(self.get_config_path())
            self.token = config_parser["telegram"]["token"]
            self.chat_id = config_parser["telegram"]["chat_id"]

            self.link = "https://api.telegram.org/{}/sendMessage?chat_id={}"\
                .format(self.token, self.chat_id)
        except:
            self.logger.write_error("Configurazione telegram non trovata")

    def send(self, text):
        if self.link is None:
            return

        self.link += "&text=" + text
        r = requests.post(self.link)

    def get_config_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, os.pardir, "config.ini"))
