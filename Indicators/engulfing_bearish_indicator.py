from .indicator import Indicator
from Domain.Entities import SignalModel
from Domain.Enum import IndicatorSignalChartType
from Domain.Enum import PositionType


class EngulfingBearishIndicator(Indicator):

    def __init__(self, args):
        super().__init__(args)

        self.type_of_indicator_signal = IndicatorSignalChartType.marker

        self.bearish_signal_three = None
        self.bearish_signal_two = None
        self.bearish_signal_one = None

    def next(self):

        if len(self.df) > 3:
            if self.check_arg('candles_three'):
                self.bearish_signal_three = (
                        self.df.Close[-4] > self.df.Open[-4]
                        and self.df.Close[-3] > self.df.Open[-3]
                        and self.df.Close[-2] > self.df.Open[-2] > self.df.Close[-1]
                )
            if self.check_arg('candles_two'):
                self.bearish_signal_two = (
                        self.df.Close[-3] > self.df.Open[-3]
                        and self.df.Close[-2] > self.df.Open[-2] > self.df.Close[-1]
                )
            if self.check_arg('candles_one'):
                self.bearish_signal_one = (
                        self.df.Close[-2] > self.df.Open[-2] > self.df.Close[-1]
                )

            if self.bearish_signal_three:
                self.add_signal(
                    SignalModel(
                        "bearish_signal_three",
                        self.df.index[-1],
                        float(self.df.High[-1]) + 0.008,
                        'triangle-down',
                        'red'
                    )
                )
                self.add_signal(
                    SignalModel(
                        "bearish_signal_three",
                        self.df.index[-1],
                        float(self.df.High[-1]) + 0.010,
                        'triangle-down',
                        'red'
                    )
                )
                self.indicator_event.fire(PositionType.SHORT)
            elif self.bearish_signal_two:
                self.add_signal(
                    SignalModel(
                        "bearish_signal_two",
                        self.df.index[-1],
                        float(self.df.High[-1]) + 0.008,
                        'triangle-down',
                        'red'
                    )
                )
                self.indicator_event.fire(PositionType.SHORT)
            elif self.bearish_signal_one:
                self.add_signal(
                    SignalModel(
                        "bearish_signal_one",
                        self.df.index[-1],
                        float(self.df.High[-1]) + 0.008,
                        'triangle-down',
                        'red'
                    )
                )
                self.indicator_event.fire(PositionType.SHORT)

    def check_arg(self, arg):
        return True if self.args.get(arg) == 'yes' else False

