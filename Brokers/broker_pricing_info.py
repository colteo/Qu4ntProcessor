import inspect
from Base import BaseObject
from Domain.Enum import ProcessorType
from Services.DataFeed import DataFeed


class BrokerPricingInfo(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.data_main = None
        self.data_feed = None
        self.data_stream = None

        self.args = args
        self.init_data_feed()

