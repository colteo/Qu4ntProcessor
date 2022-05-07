from Base import BaseObject
from Services.Communications import ServerAPI
from Services.Assistant import Assistant
from .html_printer import HTMLPrinter
import json
import configparser


class OutcomesManager(BaseObject):

    def __init__(self, args, processor, print_html=False, send_result_to_server_api=False):
        super().__init__()
        self.args = args
        self.processor = processor
        self.outcomes = processor.broker.trade_manager.outcomes
        self.data_main = processor.broker.pricing.data_main
        self.data_stream = processor.broker.pricing.data_stream
        self.check_url = None

        if print_html:
            self.html_printer = HTMLPrinter(self.data_main, self.data_stream, self.outcomes)

        if send_result_to_server_api:
            self.server_api = ServerAPI()

            strategy_id = self.create_strategy()
            if strategy_id is not None:
                for outcome in self.outcomes:
                    self.send_outcome(outcome, strategy_id)
                self.set_strategy_final_cash(strategy_id)

    def create_strategy(self):
        post_data = {}
        post_data["Type"] = self.args.parameters.processor_type.value
        post_data["Name"] = self.args.parameters.strategy.strategy_name
        post_data["Meta"] = self.args.parameters.strategy.reprJSON()
        post_data["Instrument"] = self.args.parameters.data_feed.instrument.value
        post_data["Granularity"] = self.args.parameters.data_feed.granularity.value
        post_data["Start"] = str(self.args.parameters.data_feed.start_date.isoformat())
        post_data["End"] = str(self.args.parameters.data_feed.end_date.isoformat())
        post_data["InitialCash"] = self.processor.broker.account.get_initial_balance()
        post_data["Leverage"] = self.processor.broker.account.get_leverage()
        post_data = json.dumps(post_data)

        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        url_add_strategy = config_parser["server_api"]["url_add_strategy"]

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        content = self.server_api.post_request(
            url_add_strategy,
            data=post_data,
            headers=headers
        )
        if content is None:
            return None
        data = json.loads(content)
        return data["result"]["id"]

    def send_outcome(self, outcome, strategy_id):
        post_data = {}
        post_data["StrategyId"] = strategy_id
        post_data["TradeId"] = outcome.trade.trade_id
        post_data["TradePrice"] = round(outcome.trade.price, 5)
        post_data["TradeType"] = outcome.trade.position_type.value
        post_data["TradeDatetime"] = str(outcome.trade.open_time.isoformat())
        post_data["TradeStreamDatetime"] = str(outcome.trade.stream_row.Time.isoformat())
        post_data["TradeStreamAsk"] = outcome.trade.stream_row.Ask
        post_data["TradeStreamBid"] = outcome.trade.stream_row.Bid
        post_data["OrderId"] = outcome.order.order_id
        post_data["OrderParentId"] = outcome.order.trade_id
        post_data["OrderType"] = outcome.order.order_type.value
        post_data["OrderPrice"] = outcome.order.price
        post_data["OrderStreamDatetime"] = str(outcome.order.stream_row.Time.isoformat())
        post_data["OrderStreamAsk"] = outcome.order.stream_row.Ask
        post_data["OrderStreamBid"] = outcome.order.stream_row.Bid
        post_data["InitialCash"] = outcome.initial_balance
        post_data["FinalCash"] = outcome.final_balance
        post_data = json.dumps(post_data)

        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        url_add_outcome = config_parser["server_api"]["url_add_outcome"]

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        self.server_api.post_request(
            url_add_outcome,
            data=post_data,
            headers=headers
        )

    def set_strategy_final_cash(self, strategy_id):
        post_data = {}
        post_data["StrategyId"] = strategy_id
        post_data["FinalCash"] = self.processor.broker.account.get_balance()
        post_data = json.dumps(post_data)

        config_parser = configparser.ConfigParser()
        config_parser.read('config.ini')
        url_set_strategy_completed = config_parser["server_api"]["url_set_strategy_completed"]

        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        content = self.server_api.post_request(
            url_set_strategy_completed,
            data=post_data,
            headers=headers
        )
