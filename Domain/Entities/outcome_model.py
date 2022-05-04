from .trade_model import TradeModel
from .order_model import OrderModel


class OutcomeModel:

    def __init__(self, trade: TradeModel, order: OrderModel, initial_balance, final_balance):
        self.trade = trade
        self.order = order
        self.initial_balance = initial_balance
        self.final_balance = final_balance
        pass


