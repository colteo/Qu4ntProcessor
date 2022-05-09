from Domain.Enum import PositionType
from Services.Assistant import Assistant
from Domain.Entities import TradeModel, OutcomeModel
from Singleton import Singleton
from .qu4nt_broker_account import Qu4ntBrokerAccount
from .qu4nt_broker_pricing_info import Qu4ntBrokerPricingInfo
from Domain.Enum import Status
from Domain.Enum import OrderType
from Domain.Entities import OrderModel


class Qu4ntBrokerTrade(metaclass=Singleton):

    def __init__(self, args):
        self.args = args
        self.account = Qu4ntBrokerAccount()
        self.pricing = Qu4ntBrokerPricingInfo()
        self.trades = []
        self.outcomes = []
        pass

    def create_trade(self, data):
        last_price = self.pricing.get_last_middle_price()

        if int(data["order"]["units"]) > 0:
            position_type = PositionType.LONG
            price = self.pricing.get_current_ask()
        elif int(data["order"]["units"]) < 0:
            position_type = PositionType.SHORT
            price = self.pricing.get_current_bid()

        result, response = self.order_can_be_opened(
            position_type,
            data["order"]["instrument"],
            data["order"]["units"],
        )

        if not result:
            return result, response

        margin_used = self.calc_margin_used_by_position(
            position_type,
            data["order"]["instrument"],
            data["order"]["units"],
        )

        trade = TradeModel(
            trade_id=len(self.trades),
            instrument=data["order"]["instrument"],
            units=data["order"]["units"],
            open_time=last_price.Time,
            price=price,
            margin_used=margin_used,
            state=Status.OPEN,
            stream_row=self.pricing.get_current_price()
        )
        self.trades.append(trade)
        return True, trade.trade_id

    def order_can_be_opened(self, position_type, instrument, units):
        if self.check_margin(position_type, instrument, units):
            return True, "OK"
        return False, "INSUFFICIENT_LIQUIDITY"

    def check_margin(self, position_type, instrument, units):
        margin_used_by_position = self.calc_margin_used_by_position(position_type, instrument, units)
        if self.account.get_margin_available() >= margin_used_by_position:
            return True
        return False

    def calc_margin_used_by_position(self, position_type, instrument, units):
        if position_type is PositionType.LONG:
            price = self.pricing.get_current_ask()
        elif position_type is PositionType.SHORT:
            price = self.pricing.get_current_ask()
        instrument_num = instrument.split("_")[0]
        if self.account.get_currency() == instrument_num:
            margin = units / self.account.get_leverage()
        else:
            margin = (units / self.account.get_leverage()) * price
        return abs(margin)

    def get_trade_by_id(self, trade_id):
        trade = [trade for trade in self.trades if trade.trade_id is trade_id]
        trade = trade[0]
        return trade

    def get_open_trade(self):
        return [trade for trade in self.trades if trade.state is Status.OPEN]

    def change_state_to_closed(self, trade):
        trade.state = Status.CLOSED

    def close_all_trade(self):
        _trades = self.get_open_trade()
        for trade in _trades:
            self.close_trade(
                trade=trade,
                order=OrderModel(
                    order_id=0,
                    trade_id=trade.trade_id,
                    price=None,
                    state=Status.OPEN,
                    order_type=OrderType.FORCED_CLOSURE
                ),
                row=self.pricing.get_current_price(),
            )

    def close_trade(self, trade, order, row):
        # questo metodo deve solo chiudere l'ordine e salvare l'outcome
        if trade.state is Status.OPEN:
            initial_balance = self.account.get_balance()
            trade_amount = self.calc_trade_produced_amount(trade, order, row)
            self.account.set_balance(initial_balance + trade_amount)

            self.account.set_margin_available(self.account.get_balance())

            self.change_state_to_closed(trade)

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

    def calc_trade_produced_amount(self, trade, order, row):
        pips = self.calc_pips_difference(trade, row)

        if order.order_type is OrderType.STOP_LOSS or order.order_type is OrderType.TAKE_PROFIT:
            price = order.price
        elif order.order_type is OrderType.FORCED_CLOSURE:
            price = trade.price

        if trade.position_type == PositionType.LONG and row.Bid <= price:
            return -self.calc_pips_value(trade, row, pips)
        elif trade.position_type == PositionType.SHORT and row.Ask >= price:
            return -self.calc_pips_value(trade, row, pips)
        elif trade.position_type == PositionType.LONG and row.Bid >= price:
            return self.calc_pips_value(trade, row, pips)
        elif trade.position_type == PositionType.SHORT and row.Ask <= price:
            return self.calc_pips_value(trade, row, pips)

    def calc_pips_value(self, trade, row, pips):
        # https://www.cashbackforex.com/tools/pip-calculator/EURUSD#:~:text=The%201%20pip%20size%20of,the%205%20represents%205%20pips.
        # the pip value price is calculated using the current exchange price (mid price)
        middle_price = (row.Ask + row.Bid) / 2
        one_pip_value = self.calc_pip_value(trade, middle_price)
        return pips * one_pip_value

    def calc_pip_value(self, trade, middle_price):
        multipler = 0.0001
        return abs((trade.units * multipler) / middle_price)


