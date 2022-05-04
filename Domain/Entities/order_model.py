from Domain.Enum import PositionType


class OrderModel:

    def __init__(self, order_id, trade_id, price, state, order_type):
        self.order_id = order_id
        self.trade_id = trade_id
        self.price = price
        self.state = state
        self.order_type = order_type
        self.stream_row = None

    def set_stream_row(self, row):
        self.stream_row = row
