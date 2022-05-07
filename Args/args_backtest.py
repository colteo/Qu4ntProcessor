import datetime
from argparse import ArgumentParser
from Domain.Entities import BrokerModel
from Domain.Entities import DataFeedModel
from Domain.Entities import StrategyModel
from Domain.Entities import IndicatorModel
from Domain.Enum import ProcessorType
from Domain.Enum import InstrumentType
from Domain.Enum import GranularityType

strategy = StrategyModel(
    strategy_name="EngulfingStrategy",
    indicators=[
        IndicatorModel(
            "EngulfingBullishIndicator",
            {
                "candles": ["three", "two", "one"]
            },
        ),
        IndicatorModel(
            "EngulfingBearishIndicator",
            {
                "candles": ["three", "two", "one"]
            },
        )
    ],
    stop_loss=20,
    take_profit=60
)

data_feed = DataFeedModel(
    InstrumentType.eurusd,
    GranularityType.D,
    start_date=datetime.datetime(2021, 1, 1, 0, 0, 0),
    end_date=datetime.datetime(2021, 1, 31, 0, 0, 0),
)

args_qu4nt = {
    "currency": "EUR",
    "balance": 1000,
    "leverage": 30,
    # "type_of_money_management": MoneyManagementType.ALL_IN
}
broker = BrokerModel(
    "Qu4ntBroker",
    args_qu4nt
)


class ArgsBacktest:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument('--processor_type', required=True, type=ProcessorType, choices=list(ProcessorType))

        try:
            self.parameters = parser.parse_args()
        except:
            class FakeParameters:
                def __init__(self):
                    self.processor_type = ProcessorType.backtest
                    self.data_feed = data_feed
                    self.strategy = strategy
                    self.broker = broker

            self.parameters = FakeParameters()

