import inspect
from Base import BaseObject
from Domain.Enum import ProcessorType
from Services.DataFeed import DataFeed


class BrokerAccount(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args

