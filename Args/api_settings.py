import requests
import configparser
import inspect
from datetime import datetime
from Base.base_object import BaseObject
from Domain.Entities import ParametersModel
from Domain.Entities import BrokerModel
from Domain.Entities import DataFeedModel
from Domain.Entities import StrategyModel
from Domain.Entities import IndicatorModel
from Domain.Enum import ProcessorType
from Domain.Enum import InstrumentType
from Domain.Enum import GranularityType


class ApiSettings(BaseObject):
    def __init__(self, settings_id):
        super().__init__()
        self.parameters = self.get_parameters(settings_id)

    def get_config_file(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        return config_parser['processor_api']

    def get_settings_from_api(self, settings_id):
        processor_api_config = self.get_config_file()
        try:
            url = "{}/{}".format(processor_api_config['url_get_settings'], settings_id)
            return requests.get(url).json()
        except Exception as e:
            self.logger.write_error("Processor API non configurato. Exception: {}".format(e),
                                    self.__class__.__name__, inspect.stack()[0][3])
            exit(e)

    def get_parameters(self, settings_id):
        settings = self.get_settings_from_api(settings_id)
        processor_type, data_feed, strategy, broker = ApiSettings.map_parameters(settings)
        return ParametersModel(processor_type, data_feed, strategy, broker)

    def map_parameters(self, settings):
        processor_type = ProcessorType(settings["TypeOfProcessor"])
        data_feed = self.get_datafeed_model(settings["Feed"])
        strategy = self.get_strategy_model(settings["Strategy"])
        broker = self.get_broker_model(settings["Broker"])
        return processor_type, data_feed, strategy, broker

    def get_datafeed_model(self, feed):
        return DataFeedModel(
            instrument=InstrumentType(feed['Instrument']),
            granularity=GranularityType(feed['Granularity']),
            start_date=datetime.strptime(feed['StartDate'], '%Y-%m-%dT%H:%M:%S'),
            end_date=datetime.strptime(feed['EndDate'], '%Y-%m-%dT%H:%M:%S'),
            stream_granularity=GranularityType(feed['StreamGranularity'])
        )

    def get_strategy_model(self, strategy):
        return StrategyModel(
            strategy_name=strategy["Name"],
            indicators=[self.get_indicator_model(indicator) for indicator in strategy['Indicators']],
            stop_loss=strategy["StopLoss"],
            take_profit=strategy["TakeProfit"]
        )

    def get_indicator_model(self, indicator):
        result = {}
        [result.update({arg['Key']: arg['Value']}) for arg in indicator["Args"]]
        return IndicatorModel(
            indicator["Name"],
            result
        )

    def get_broker_model(self, broker):
        result = {}
        [result.update({arg['Key']: arg['Value']}) for arg in broker["Args"]]
        return BrokerModel(
            broker["Name"],
            result
        )
