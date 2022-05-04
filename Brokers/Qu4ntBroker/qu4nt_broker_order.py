from Brokers.broker_order import BrokerOrder
from Domain.Entities import OrderModel
from Services.Assistant import Assistant
from Domain.Enum import Status
from Singleton import Singleton
from .qu4nt_broker_account import Qu4ntBrokerAccount
from .qu4nt_broker_pricing_info import Qu4ntBrokerPricingInfo
from .qu4nt_broker_trade import Qu4ntBrokerTrade
from Domain.Enum import OrderType


class Qu4ntBrokerOrder(BrokerOrder, metaclass=Singleton):

    def __init__(self, args):
        super().__init__(args)
        self.account = Qu4ntBrokerAccount()
        self.pricing = Qu4ntBrokerPricingInfo()
        self.trade_manager = Qu4ntBrokerTrade()

    def market_order_request(self, instrument, units):
        data = {
            "order": {
                "type": "MARKET",
                "positionFill": "DEFAULT",
                "instrument": instrument,
                "timeInForce": "FOK",
                "units": units
            }
        }
        return self.trade_manager.create_trade(data)

    def take_profit_order_request(self, trade_id, pips):
        price = self.calc_take_profit_price(trade_id, pips)
        data = {
            "order": {
                "type": OrderType.TAKE_PROFIT,
                "tradeID": trade_id,
                "price": price,
                "timeInForce": "GTC",
            }
        }
        return self.create_order(data)

    def stop_loss_order_request(self, trade_id, pips):
        price = self.calc_stop_loss_price(trade_id, pips)
        data = {
            "order": {
                "type": OrderType.STOP_LOSS,
                "tradeID": trade_id,
                "price": price,
                "timeInForce": "GTC",
            }
        }
        return self.create_order(data)

    def create_order(self, data):
        order = OrderModel(
            order_id=len(self.orders),
            trade_id=data["order"]["tradeID"],
            price=data["order"]["price"],
            state=Status.OPEN,
            order_type=data["order"]["type"]
        )
        self.orders.append(order)
        return True, None

    def get_related_orders_by_trade_id(self, trade_id):
        return [order for order in self.orders if order.trade_id is trade_id]

    def close_related_orders_by_trade_id(self, trade_id):
        related_orders = self.get_related_orders_by_trade_id(trade_id)
        for order in related_orders:
            order.state = Status.CLOSED
