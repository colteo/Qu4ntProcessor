import sys
from Base import BaseObject
from Services.Assistant import Assistant
from Event import EventHook
from Sizer import Sizer
from Domain.Enum import OrderType

# ATTENZIONE: non eliminare la seguente riga
from Indicators import *


class Strategy(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.df = None

        self.strategy_event = EventHook()

        self.indicators = []
        self.set_indicators()

        self.sizer = None
        self.init_sizer()

    def next(self):
        for indicator in self.indicators:
            indicator.df = self.df  # invece di fare l'aggiunta di un valore faccio l'assegnazione completa
            indicator.next()
        pass

    def set_indicators(self):
        for indicator in self.args.parameters.strategy.indicators:
            class_ = getattr(sys.modules[__name__], indicator.indicator_name)
            indicator_to_append = class_(indicator.args)
            indicator_to_append.indicator_event += self.event_received
            self.indicators.append(indicator_to_append)

    def init_sizer(self):
        self.sizer = Sizer("aaa")

    def event_received(self, position_type):
        self.brain(position_type)

    def brain(self, position_type):
        '''
        il tipo di posizione è obbligatorio, l'ordine a mercato dev'essere aperto

        stop_loss, take_profit, trailing_profit posso o meno essere passati, dipende dal tipo di ordine che la straegia intede aprire
        '''
        self.strategy_event.fire(
            position_type,
            stop_loss=OrderType.STOP_LOSS,
            take_profit=OrderType.TAKE_PROFIT
        )




