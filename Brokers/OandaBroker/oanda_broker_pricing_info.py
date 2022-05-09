import oandapyV20
import oandapyV20.endpoints.pricing as pricing
from Services.DataFeed import DataFeed
from Services.Assistant import AssistantDataframe, Assistant
from Brokers.broker_pricing_info import BrokerPricingInfo


class OandaBrokerPricingInfo(BrokerPricingInfo):

    def __init__(self, args, account_id, access_token):
        super().__init__(args)
        self.account_id = account_id
        self.access_token = access_token

        self.params = {
            "instruments": self.args.parameters.data_feed.value
        }

    def get_pricing_info(self):
        client = oandapyV20.API(access_token=self.access_token)
        r = pricing.PricingInfo(accountID=self.account_id, params=self.params)
        client.request(r)
        # print(json.dumps(r.response, indent=4, sort_keys=True))
        return r.response

    def get_current_middle_price(self):
        new_data = self.data_feed.get_candles_by_count(5)
        for index, row in new_data.reset_index().iterrows():
            if not any(self.data_main.reset_index().Time == row.Time):
                self.data_main = AssistantDataframe.add_row_to_dataframe(
                    self.data_main,
                    row,
                    AssistantDataframe.columns_data_main_by_count()
                )
                return True, row

        return False, None

    def get_current_ask(self):
        pricing_info = self.get_pricing_info()
        ask = float(pricing_info["prices"][0]["closeoutAsk"])
        return ask

    def get_current_bid(self):
        pricing_info = self.get_pricing_info()
        bid = float(pricing_info["prices"][0]["closeoutBid"])
        return bid

    def init_data_feed(self):
        self.data_feed = DataFeed(self.args.parameters.data_feed)
        self.data_main = self.data_feed.get_candles_by_count(5)

