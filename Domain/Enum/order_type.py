from enum import Enum


class OrderType(Enum):
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'
    FORCED_CLOSURE = 'FORCED_CLOSURE'

    def __str__(self):
        return self.value

