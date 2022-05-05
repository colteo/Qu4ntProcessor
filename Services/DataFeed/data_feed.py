from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.instruments as instruments
import tpqoa
import os
import json
import pandas as pd
import configparser
from Services.Assistant import Assistant, AssistantDataframe, AssistantFilesystem
from Domain.Entities import DataFeedModel
from Domain.Enum import GranularityType


class DataFeed:
    path = 'csv/'

    def __init__(self, model: DataFeedModel):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.account_id = None
        self.access_token = None
        self.api = None
        self.init_config_values()
        self.model = model
        self.init_connection()

    def init_config_values(self):
        '''
        sia che si tratti di live che di backtest vengono usati i dati di "oanda_data_feed".
        :return:
        '''
        config_parser = configparser.ConfigParser()
        config_parser.read('oanda_default_account.ini')
        self.account_id = config_parser["oanda"]["account_id"]
        self.access_token = config_parser["oanda"]["access_token"]
        pass

    def init_connection(self):
        self.api = API(
            access_token=self.access_token,
            environment="practice"
        )
        # self.test_connection()
        pass

    def test_connection(self):
        r = trades.TradesList(self.account_id)
        print("REQUEST:{}".format(r))
        rv = self.api.request(r)
        print("RESPONSE:\n{}".format(json.dumps(rv, indent=2)))
        pass

    def get_candles_by_count(self, count=None):
        count = count if count is not None else self.model.count

        params = {}
        params.update({"granularity": self.model.granularity})
        params.update({"count": count})
        r = instruments.InstrumentsCandles(instrument=self.model.instrument, params=params)
        try:
            self.api.request(r) # ouputs a large JSON object
        except:
            self.init_connection()
            self.api.request(r) # ouputs a large JSON object

        dat = []
        for oo in r.response['candles']:
            dat.append([oo['time'], oo['volume'], oo['mid']['o'], oo['mid']['h'], oo['mid']['l'], oo['mid']['c'], oo['complete']])

        # output time,  open, high, low, close in a table
        df = pd.DataFrame(dat)
        df.columns = AssistantDataframe.columns_data_main_by_count()

        self.shift_close_to_open(df)

        df = df.set_index('Time')
        df = df.drop(df[df.Complete == False].index)
        return df

    # OPEN, HIGH, LOW, CLOSE (middle)
    def get_data_main_by_date_middle_price(self):
        datapath = self.get_data_path(
            self.model.instrument,
            self.model.start_date,
            self.model.end_date,
            self.model.granularity
        )

        if AssistantFilesystem.file_exist(datapath) is False:
            api = tpqoa.tpqoa("oanda_default_account.ini")

            price = api.get_history(
                instrument=self.model.instrument.value,
                start=self.model.start_date,
                end=self.model.end_date,
                granularity=self.model.granularity.value,
                price="M",
                localize=False
            )

            price.rename(columns={"o": "Open"}, inplace=True)
            price.rename(columns={"h": "High"}, inplace=True)
            price.rename(columns={"l": "Low"}, inplace=True)
            price.rename(columns={"c": "Close"}, inplace=True)
            price.rename(columns={"volume": "Volume"}, inplace=True)
            price.rename(columns={"complete": "Complete"}, inplace=True)

            price.reset_index(inplace=True)

            price.rename(columns={"time": "Time"}, inplace=True)

            self.shift_close_to_open(price)

            price.set_index('Time', inplace=True)

            price = price.drop(price[price.Complete == False].index)
            price.drop('Complete', axis=1, inplace=True)

            data = pd.concat([price], axis=1)
            data.to_csv(datapath)

        return self.get_csv(datapath)

    # BID, ASK (middle)
    def get_data_stream_by_date_ask_and_price(self):
        data_stream_granularity = GranularityType.M30.value
        datapath = self.get_data_path(
            self.model.instrument,
            self.model.start_date,
            self.model.end_date,
            data_stream_granularity
        )

        if AssistantFilesystem.file_exist(datapath) is False:
            api = tpqoa.tpqoa("oanda_default_account.ini")

            # BID calculated on askclose price
            bid = api.get_history(
                instrument=self.model.instrument.value,
                start=self.model.start_date,
                end=self.model.end_date,
                granularity=data_stream_granularity,
                price="B",
                localize=False
            )

            bid.rename(columns={"c": "Bid"}, inplace=True)
            bid.rename(columns={"complete": "Complete"}, inplace=True)

            bid.reset_index(inplace=True)
            bid.rename(columns={"time": "Time"}, inplace=True)
            bid.set_index('Time', inplace=True)
            bid = bid.drop(bid[bid.Complete == False].index)
            # bid.drop('Complete', axis=1, inplace=True)
            bid = bid[['Bid']]

            # ASK calculated on askclose price
            ask = api.get_history(
                instrument=self.model.instrument.value,
                start=self.model.start_date,
                end=self.model.end_date,
                granularity=data_stream_granularity,
                price="A",
                localize=False
            )

            ask.rename(columns={"c": "Ask"}, inplace=True)
            ask.rename(columns={"complete": "Complete"}, inplace=True)

            ask.reset_index(inplace=True)
            ask.rename(columns={"time": "Time"}, inplace=True)
            ask.set_index('Time', inplace=True)
            ask = ask.drop(ask[ask.Complete == False].index)
            # ask.drop('Complete', axis=1, inplace=True)
            ask = ask[['Ask']]

            data = pd.concat([ask, bid], axis=1)
            data.to_csv(datapath)

        return self.get_csv(datapath)

    def shift_close_to_open(self, df):
        df.Open = df.Close.shift(1)
        df.dropna(inplace=True)

    def get_data_path(self, instrument_name, start_date, end_date, timeframe):
        '''
        instrument_name = "EUR_USD", "EUR_USD", "EUR_JPY", "DE30_EUR"
        start_date = "2021-01-01"
        start_end = "2021-12-31"
        timeframe = "H1" # "M5", "H1, "D"
        '''
        return os.path.join(self.path, self.filename(instrument_name, start_date, end_date, timeframe))

    def filename(self, instrument_name, start_date, end_date, granularity):
        filename = str(instrument_name) + "-" + str(start_date) + "-" + str(end_date) + "_" + str(granularity)
        filename = Assistant.normalize_string(filename)
        filename += ".csv"
        return filename


    def get_csv(self, path):
        skiprows = 0
        header = 0
        dataframe = pd.read_csv(path,
            skiprows=skiprows,
            header=header,
            parse_dates=True,
            index_col=0
        )

        return dataframe