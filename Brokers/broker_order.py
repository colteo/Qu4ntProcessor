import inspect
from Base import BaseObject
from Domain.Enum import ProcessorType
from Services.DataFeed import DataFeed
from Domain.Enum import PositionType


class BrokerOrder(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.orders = []
        self.activities = []

    def calc_take_profit_price(self, trade_id, pips):
        trade = self.trade_manager.get_trade_by_id(trade_id)
        if trade.position_type is PositionType.LONG:
            price = round(float(trade.price) + (pips / 10000), 4)
        elif trade.position_type is PositionType.SHORT:
            price = round(float(trade.price) - (pips / 10000), 4)
        return price

    def calc_stop_loss_price(self, trade_id, pips):
        trade = self.trade_manager.get_trade_by_id(trade_id)
        if trade.position_type is PositionType.LONG:
            price = round(float(trade.price) - (pips / 10000), 4)
        elif trade.position_type is PositionType.SHORT:
            price = round(float(trade.price) + (pips / 10000), 4)
        return price
