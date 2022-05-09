from .indicator import Indicator
from Domain.Entities import SignalModel
from Domain.Enum import IndicatorSignalChartType
from Domain.Enum import PositionType
import random


class RandomIndicator(Indicator):

    def __init__(self, args):
        super().__init__(args)
        self.hello = ['LONG', 'SHORT']
        self.type_of_indicator_signal = IndicatorSignalChartType.marker

    def next(self):
        if len(self.df) % 2 == 0:
            # print(len(self.df))
            # print("ok è divisibile")
            selected = random.choice(self.hello)
            if selected == "LONG":
                self.indicator_event.fire(PositionType.LONG)
            elif selected == "SHORT":
                self.indicator_event.fire(PositionType.SHORT)

        pass

