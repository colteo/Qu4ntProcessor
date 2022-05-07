from enum import Enum


class InstrumentType(Enum):
    eurusd = 'EUR_USD'
    eurchf = 'EUR_CHF'
    eurgbp = 'EUR_GBP'
    euraud = 'EUR_AUD'
    eurcad = 'EUR_CAD'
    eurnzd = 'EUR_NZD'

    def __str__(self):
        return self.value

