from Domain.Enum import PositionType
from Services.Assistant import Assistant
from Domain.Entities import TradeModel
from Singleton import Singleton
from .qu4nt_broker_account import Qu4ntBrokerAccount
from .qu4nt_broker_pricing_info import Qu4ntBrokerPricingInfo
from Domain.Enum import Status


class Qu4ntBrokerTrade(metaclass=Singleton):

    def __init__(self, args):
        self.args = args
        self.account = Qu4ntBrokerAccount()
        self.pricing = Qu4ntBrokerPricingInfo()
        self.trades = []
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

    def close_all_trade(self):
        print("Metodo close_all_trade non implementato")

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

    def close_trade_by_id(self, trade_id):
        trade = self.get_trade_by_id(trade_id)
        trade.state = Status.CLOSED
