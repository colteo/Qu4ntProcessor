from argparse import ArgumentParser
from Domain.Entities import BrokerModel
from Domain.Entities import DataFeedModel
from Domain.Entities import StrategyModel
from Domain.Entities import IndicatorModel
from Domain.Enum import ProcessorType
from Domain.Enum import InstrumentType
from Domain.Enum import GranularityType

strategy = StrategyModel(
    "EngulfingStrategy",
    [
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
    ]
)

data_feed = DataFeedModel(
    InstrumentType.eurusd,
    GranularityType.S5,
    count=10,
)

broker = BrokerModel(
    "OandaBroker",
    {}
)


class ArgsLive:
    def __init__(self):
        parser = ArgumentParser()
        parser.add_argument('--processor_type', required=True, type=ProcessorType, choices=list(ProcessorType))

        try:
            self.parameters = parser.parse_args()
        except:
            class FakeParameters:
                def __init__(self):
                    self.processor_type = ProcessorType.live
                    self.data_feed = data_feed
                    self.strategy = strategy
                    self.broker = broker

            self.parameters = FakeParameters()
