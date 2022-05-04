from enum import Enum


class OrderType(Enum):
    TAKE_PROFIT = 'TAKE_PROFIT'
    STOP_LOSS = 'STOP_LOSS'

    def __str__(self):
        return self.value

