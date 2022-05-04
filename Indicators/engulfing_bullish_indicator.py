from .indicator import Indicator
from Domain.Entities import SignalModel
from Domain.Enum import IndicatorSignalChartType
from Domain.Enum import PositionType


class EngulfingBullishIndicator(Indicator):

    def __init__(self, args):
        super().__init__(args)

        self.type_of_indicator_signal = IndicatorSignalChartType.marker

        self.bullish_signal_three = None
        self.bullish_signal_two = None
        self.bullish_signal_one = None

    def next(self):

        if len(self.df) > 3:
            if "three" in self.args["candles"]:
                self.bullish_signal_three = (
                        self.df.Close[-4] < self.df.Open[-4]
                        and self.df.Close[-3] < self.df.Open[-3]
                        and self.df.Close[-2] < self.df.Open[-2] < self.df.Close[-1]
                )
            if "two" in self.args["candles"]:
                self.bullish_signal_two = (
                        self.df.Close[-3] < self.df.Open[-3]
                        and self.df.Close[-2] < self.df.Open[-2] < self.df.Close[-1]
                )
            if "one" in self.args["candles"]:
                self.bullish_signal_one = (
                        self.df.Close[-2] < self.df.Open[-2] < self.df.Close[-1]
                )

            if self.bullish_signal_three:
                self.add_signal(
                    SignalModel(
                        "bullish_signal_three",
                        self.df.index[-1],
                        float(self.df.Low[-1]) - 0.008,
                        'triangle-up',
                        'green'
                    )
                )
                self.add_signal(
                    SignalModel(
                        "bullish_signal_three",
                        self.df.index[-1],
                        float(self.df.Low[-1]) - 0.010,
                        'triangle-up',
                        'green'
                    )
                )
                self.indicator_event.fire(PositionType.LONG)
            elif self.bullish_signal_two:
                self.add_signal(
                    SignalModel(
                        "bullish_signal_two",
                        self.df.index[-1],
                        float(self.df.Low[-1]) - 0.008,
                        'triangle-up',
                        'green'
                    )
                )
                self.indicator_event.fire(PositionType.LONG)
            elif self.bullish_signal_one:
                self.add_signal(
                    SignalModel(
                        "bullish_signal_one",
                        self.df.index[-1],
                        float(self.df.Low[-1]) - 0.008,
                        'triangle-up',
                        'green'
                    )
                )
                self.indicator_event.fire(PositionType.LONG)





