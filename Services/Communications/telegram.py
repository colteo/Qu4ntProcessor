from interface import implements
from .communication_interface import CommunicationInterface
import requests


class Telegram(implements(CommunicationInterface)):

    def __init__(self, config):
        self.config = config
        self.link = "https://api.telegram.org/{}/sendMessage?chat_id={}".format(self.config["token"], self.config["chat_id"])

    def send(self, text):
        self.link += "&text=" + text
        r = requests.post(self.link)
