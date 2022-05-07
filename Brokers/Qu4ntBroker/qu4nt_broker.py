from Brokers.broker import Broker
from .qu4nt_broker_pricing_info import Qu4ntBrokerPricingInfo
from .qu4nt_broker_account import Qu4ntBrokerAccount
from .qu4nt_broker_order import Qu4ntBrokerOrder
from .qu4nt_broker_trade import Qu4ntBrokerTrade
from Domain.Enum import OrderType
from Domain.Enum import PositionType
from Domain.Enum import Status
from Domain.Entities import OutcomeModel
from Services.Assistant import Assistant


class Qu4ntBroker(Broker):

    def __init__(self, args):
        super().__init__(args)

    def init_pricing_info(self):
        self.pricing = Qu4ntBrokerPricingInfo(self.args)

    def init_account(self):
        self.account = Qu4ntBrokerAccount(self.args)

    def init_order_manager(self):
        self.order_manager = Qu4ntBrokerOrder(self.args)

    def init_trade_manager(self):
        self.trade_manager = Qu4ntBrokerTrade(self.args)

    def check_trade_and_related_orders(self):
        open_trades = self.trade_manager.get_open_trade()
        for trade in open_trades:
            related_order = self.order_manager.get_related_orders_by_trade_id(trade.trade_id)

            data_stream = self.pricing.get_data_stream_to_check_order()
            if data_stream is False:
                return

            for index, row in data_stream.iterrows():
                # print(row)
                for order in related_order:
                    result = False
                    if order.order_type is OrderType.STOP_LOSS and order.state is Status.OPEN:
                        result = self.check_order_stop_loss(trade, order, row)
                        if result:
                            break
                    elif order.order_type is OrderType.TAKE_PROFIT and order.state is Status.OPEN:
                        result = self.check_order_take_profit(trade, order, row)
                        if result:
                            break

                    if result:
                        break
        pass

    def check_order_stop_loss(self, trade, order, row):
        if trade.position_type == PositionType.LONG and row.Bid <= order.price:
            '''
            se la posizione è long prendo stop loss quando il prezzo di data stream è minore del prezzo dell'ordine
            '''
            # print("sei in stop loss LONG bid: {} | order price: {}".format(row.Bid, order.price))
            return self.trade_manager.close_trade(trade, order, row)
        elif trade.position_type == PositionType.SHORT and row.Ask >= order.price:
            '''
            se la posizione è short prendo stop loss quando il prezzo di data stream è maggiore del prezzo dell'ordine
            '''
            # print("sei in stop loss SHORT ask: {} | order price: {}".format(row.Ask, order.price))
            return self.trade_manager.close_trade(trade, order, row)

    def check_order_take_profit(self, trade, order, row):
        if trade.position_type == PositionType.LONG and row.Bid >= order.price:
            '''
            se la posizione è long prendo take profit quando il prezzo di data stream è maggiore del prezzo dell'ordine
            '''
            # print("sei in take profit LONG bid: {} | order price: {}".format(row.Bid, order.price))
            return self.trade_manager.close_trade(trade, order, row)
        elif trade.position_type == PositionType.SHORT and row.Ask <= order.price:
            '''
            se la posizione è short prendo take profit quando il prezzo di data stream è minore del prezzo dell'ordine
            '''
            # print("sei in take profit SHORT ask: {} | order price: {}".format(row.Ask, order.price))
            return self.trade_manager.close_trade(trade, order, row)
        pass

