from Base import BaseObject
from Singleton import Singleton
import json
import inspect
import requests
import configparser
import os


class ServerAPI(BaseObject):

    def __init__(self):
        super().__init__()
        self.__is_on = False
        self.init()

    def init(self):
        try:
            config_parser = configparser.ConfigParser()
            config_parser.read(self.get_config_path())
            check_url = config_parser["server_api"]["check_url"]

            response = requests.get(check_url)
            content = response.content.decode("utf-8")

            if content == "OK":
                self.__is_on = True


        except:
            self.logger.write_error("Server API non configurato")

    def post_request(self, url, data, headers):
        if self.__is_on:
            response = requests.post(
                url,
                data=data,
                headers=headers
            )
            content = response.content
            return content
        return None

    def get_config_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, os.pardir, "config.ini"))
