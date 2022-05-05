from Base import BaseObject
from Singleton import Singleton
import inspect
import requests
import configparser


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
            config_parser.read('config.ini')
            self.token = config_parser["telegram"]["token"]
            self.chat_id = config_parser["telegram"]["chat_id"]

            self.link = "https://api.telegram.org/{}/sendMessage?chat_id={}"\
                .format(self.token, self.chat_id)
        except:
            self.logger.write_error("Configurazione telegram non trovata", self.__class__.__name__, inspect.stack()[0][3])

    def send(self, text):
        if self.link is None:
            return

        self.link += "&text=" + text
        r = requests.post(self.link)
