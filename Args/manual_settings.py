import datetime
from Domain.Entities import BrokerModel
from Domain.Entities import DataFeedModel
from Domain.Entities import StrategyModel
from Domain.Entities import IndicatorModel
from Domain.Entities import ParametersModel
from Domain.Enum import ProcessorType
from Domain.Enum import InstrumentType
from Domain.Enum import GranularityType

processor_type = ProcessorType.live

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

# strategy = StrategyModel(
#     strategy_name="RandomStrategy",
#     indicators=[
#         IndicatorModel(
#             "RandomIndicator",
#             {},
#         )
#     ],
#     stop_loss=20,
#     take_profit=60
# )

if processor_type is ProcessorType.backtest:
    data_feed = DataFeedModel(
        InstrumentType.eurusd,
        GranularityType.M15,
        start_date=datetime.datetime(2022, 2, 7, 0, 0, 0),
        end_date=datetime.datetime(2022, 2, 8, 0, 0, 0),
        stream_granularity=GranularityType.M1
    )
    args_qu4nt = {
        "currency": "EUR",
        "balance": 1000,
        "leverage": 30,
    }
    broker = BrokerModel(
        "Qu4ntBroker",
        args_qu4nt
    )
elif processor_type is ProcessorType.live:
    data_feed = DataFeedModel(
        InstrumentType.eurusd,
        GranularityType.S15,
        count=10,
    )
    broker = BrokerModel(
        "OandaBroker",
        {}
    )


class ManualSettings:
    def __init__(self):
        self.parameters = ParametersModel(processor_type, data_feed, strategy, broker)
