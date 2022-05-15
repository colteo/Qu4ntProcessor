from Base import BaseObject
from Domain.Enum import OrderType
from Services.Assistant import Assistant
import uuid
import inspect


class Broker(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.instrument = self.args.parameters.data_feed.instrument

        self.id = str(uuid.uuid4())

        self.account = None
        self.init_account()

        self.pricing = None
        self.init_pricing_info()

        self.trade_manager = None
        self.init_trade_manager()

        self.order_manager = None
        self.init_order_manager()

    def market_order_request(self, units):
        return self.order_manager.market_order_request(self.instrument.value, units)

    def take_profit_order_request(self, trade_id, price):
        return self.order_manager.take_profit_order_request(trade_id, price)

    def stop_loss_order_request(self, trade_id, price):
        return self.order_manager.stop_loss_order_request(trade_id, price)


    # def create_order(self, data):
    #     if data.order_request_type is OrderType.MARKET:
    #         return self.order_manager.create_market_order(data)
    #     elif data.order_request_type is OrderType.TAKE_PROFIT:
    #         return self.order_manager.create_take_profit_order(data)
    #     elif data.order_request_type is OrderType.STOP_LOSS:
    #         return self.order_manager.create_stop_loss_order(data)
