from Base import BaseObject
from Singleton import Singleton
import json
import inspect
import requests
import configparser


class ServerAPI(BaseObject):

    def __init__(self):
        super().__init__()
        self.__is_on = False
        self.init()

    def init(self):
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read('config.ini')
            check_url = config_parser["server_api"]["check_url"]

            response = requests.get(check_url)
            content = response.content.decode("utf-8")

            if content == "OK":
                self.__is_on = True
        except:
            self.logger.write_error("Server API non configurato", self.__class__.__name__, inspect.stack()[0][3])

    def post_request(self, url, data, headers):
        response = requests.post(
            url,
            data=data,
            headers=headers
        )
        content = response.content
        return content
