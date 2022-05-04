from enum import Enum


class InstrumentType(Enum):
    eurusd = 'EUR_USD'
    eurchf = 'EUR_CHF'

    def __str__(self):
        return self.value

