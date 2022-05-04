import configparser
from Brokers.broker import Broker
from .oanda_broker_pricing_info import OandaBrokerPricingInfo
from .oanda_broker_account import OandaBrokerAccount
from .oanda_broker_order import OandaBrokerOrder
from .oanda_broker_trade import OandaTradeBroker


class OandaBroker(Broker):

    def __init__(self, args):
        super().__init__(args)

    def init_config_values(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        # TODO oanda_test deve diventare dinamico
        account_id = config_parser["oanda_test"]["account_id"]
        access_token = config_parser["oanda_test"]["access_token"]
        return account_id, access_token

    def init_pricing_info(self):
        account_id, access_token = self.init_config_values()
        self.pricing = OandaBrokerPricingInfo(self.args, account_id, access_token)

    def init_account(self):
        account_id, access_token = self.init_config_values()
        self.account = OandaBrokerAccount(self.args, account_id, access_token)

    def init_order_manager(self):
        account_id, access_token = self.init_config_values()
        self.order_manager = OandaBrokerOrder(self.args, account_id, access_token, self.trade_manager)

    def init_trade_manager(self):
        account_id, access_token = self.init_config_values()
        self.trade_manager = OandaTradeBroker(self.args, account_id, access_token)
