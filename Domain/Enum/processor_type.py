from enum import Enum


class ProcessorType(Enum):
    backtest = 'backtest'
    live = 'live'

    def __str__(self):
        return self.value
