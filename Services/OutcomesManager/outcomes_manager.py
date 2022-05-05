from Base import BaseObject
from Services.Communications import ServerAPI
from .html_printer import HTMLPrinter


class OutcomesManager(BaseObject):

    def __init__(self, args, data_main, data_stream, outcomes):
        super().__init__()
        self.args = args
        self.outcomes = outcomes
        self.data_main = data_main
        self.data_stream = data_stream
        self.check_url = None

        self.server_api = ServerAPI()
        self.html_printer = HTMLPrinter(self.data_main, self.data_stream, self.outcomes)

