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
        self.outcomes = []

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
            print("sei in stop loss LONG bid: {} | order price: {}".format(row.Bid, order.price))
            return self.close_trade(trade, order, row)
        elif trade.position_type == PositionType.SHORT and row.Ask >= order.price:
            '''
            se la posizione è short prendo stop loss quando il prezzo di data stream è maggiore del prezzo dell'ordine
            '''
            print("sei in stop loss SHORT ask: {} | order price: {}".format(row.Ask, order.price))
            return self.close_trade(trade, order, row)

    def check_order_take_profit(self, trade, order, row):
        if trade.position_type == PositionType.LONG and row.Bid >= order.price:
            '''
            se la posizione è long prendo take profit quando il prezzo di data stream è maggiore del prezzo dell'ordine
            '''
            print("sei in take profit LONG bid: {} | order price: {}".format(row.Bid, order.price))
            return self.close_trade(trade, order, row)
        elif trade.position_type == PositionType.SHORT and row.Ask <= order.price:
            '''
            se la posizione è short prendo take profit quando il prezzo di data stream è minore del prezzo dell'ordine
            '''
            print("sei in take profit SHORT ask: {} | order price: {}".format(row.Ask, order.price))
            return self.close_trade(trade, order, row)
        pass

    def close_trade(self, trade, order, row):
        initial_balance = self.account.get_balance()

        pips = self.calc_pips_difference(trade, row)
        # print(pips)
        pips_value = self.calc_pips_value(trade, row, pips)
        # print(pips_value)
        if order.order_type is OrderType.TAKE_PROFIT:
            self.account.set_balance(self.account.get_balance() + pips_value)
        elif order.order_type is OrderType.STOP_LOSS:
            self.account.set_balance(self.account.get_balance() - pips_value)
        self.account.set_margin_available(self.account.get_balance())

        self.trade_manager.close_trade_by_id(trade.trade_id)
        self.order_manager.close_related_orders_by_trade_id(trade.trade_id)

        order.set_stream_row(row)
        outcome = OutcomeModel(
            trade=trade,
            order=order,
            initial_balance=initial_balance,
            final_balance=self.account.get_balance()
        )
        self.outcomes.append(outcome)

        return True

    def calc_pips_difference(self, trade, row):
        # TODO : multipler will change based on currency cross
        multipler = 10000
        if trade.position_type == PositionType.SHORT:
            diff = row.Ask - trade.price
        elif trade.position_type == PositionType.LONG:
            diff = row.Bid - trade.price
        return abs(diff * multipler)

    def calc_pips_value(self, trade, row, pips):
        # https://www.cashbackforex.com/tools/pip-calculator/EURUSD#:~:text=The%201%20pip%20size%20of,the%205%20represents%205%20pips.
        # the pip value price is calculated using the current exchange price (mid price)
        middle_price = (row.Ask + row.Bid) / 2
        one_pip_value = self.calc_pip_value(trade, middle_price)
        return pips * one_pip_value

    def calc_pip_value(self, trade, middle_price):
        multipler = 0.0001
        return abs((trade.units * multipler) / middle_price)


