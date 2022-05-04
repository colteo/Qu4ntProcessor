from Domain.Enum import PositionType


class TradeModel:

    def __init__(self, trade_id, instrument, units, open_time, price, margin_used, state, stream_row):
        self.trade_id = trade_id
        self.instrument = instrument
        self.open_time = open_time
        self.price = price
        self.margin_used = margin_used
        self.state = state
        self.stream_row = stream_row
        self.position_type = None
        self.units = None
        self.set_units(units)

    def set_units(self, units):
        self.units = int(units)
        if self.units < 0:
            self.position_type = PositionType.SHORT
        elif self.units > 0:
            self.position_type = PositionType.LONG
