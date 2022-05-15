import inspect
import json
from Base import BaseObject
from Domain.Enum import ProcessorType
from Services.DataFeed import DataFeed
from Brokers.broker_pricing_info import BrokerPricingInfo
from Singleton import Singleton


class Qu4ntBrokerPricingInfo(BrokerPricingInfo, metaclass=Singleton):

    def __init__(self, args):
        super().__init__(args)

        self.index = 0
        self.last_price_time = None

    def get_current_middle_price(self):
        try:
            price = self.data_main.reset_index().iloc[self.index]
            self.index += 1
            return True, price
        except:
            return False, None

    def get_last_middle_price(self):
        try:
            price = self.data_main.reset_index().iloc[self.index]
            return price
        except:
            return None


    def get_current_ask(self):
        result = self.get_current_price()
        if result is None:
            return None
        # print(result.Time)
        return result.Ask

    def get_current_bid(self):
        result = self.get_current_price()
        if result is None:
            return None
        # print(result.Time)
        return result.Bid

    def get_current_price(self):
        '''
        non sempre nel data_stream troviamo il time corretto
        quindi prendiamo il primo valore utile
        '''
        last = self.get_last_middle_price()
        if last is None:
            return None
        df = self.data_stream.reset_index().loc[self.data_stream.index >= last.Time]
        return df.iloc[0]

    def get_data_stream_to_check_order(self):
        current_index = self.index
        next_index = self.index + 1
        # print("current index {}".format(current))
        # print("next index {}".format(next))

        if current_index >= len(self.data_main) or next_index >= len(self.data_main):
            return False

        df_current = self.data_main.reset_index().iloc[current_index]
        df_next = self.data_main.reset_index().iloc[next_index]

        # print("Current time {}".format(df_current.Time))
        # print("Next time {}".format(df_next.Time))

        df = self.data_stream.reset_index().loc[(self.data_stream.index >= df_current.Time) & (self.data_stream.index < df_next.Time)]

        return df

    def init_data_feed(self):
        self.data_feed = DataFeed(self.args.parameters.data_feed)
        self.data_main = self.data_feed.get_data_main_by_date_middle_price()
        self.data_stream = self.data_feed.get_data_stream_by_date_ask_and_price()

