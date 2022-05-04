import json
import configparser
import oandapyV20
import oandapyV20.endpoints.trades as trades
from Domain.Entities import TradeModel
from Services.Assistant import Assistant


class OandaTradeBroker:

    def __init__(self, args, account_id, access_token):
        self.account_id = account_id
        self.access_token = access_token

    def get_trade_list(self):
        client = oandapyV20.API(access_token=self.access_token)
        r = trades.TradesList(accountID=self.account_id)
        client.request(r)
        # print(json.dumps(r.response, indent=4, sort_keys=True))
        return r.response

    def get_trade_by_id(self, trade_id):
        client = oandapyV20.API(access_token=self.access_token)
        r = trades.TradeDetails(accountID=self.account_id, tradeID=trade_id)
        client.request(r)
        # print(json.dumps(r.response["trade"], indent=4, sort_keys=True))
        return TradeModel(
            r.response["trade"]["id"],
            r.response["trade"]["instrument"],
            r.response["trade"]["initialUnits"],
            r.response["trade"]["openTime"],
            r.response["trade"]["price"],
            r.response["trade"]["marginUsed"],
            r.response["trade"]["state"],
        )

    def close_all_trade(self):
        _trades = self.get_trade_list()
        for trade in _trades["trades"]:
            self.close_trade(trade["id"])

    def close_trade(self, trade_id):
        client = oandapyV20.API(access_token=self.access_token)
        r = trades.TradeClose(accountID=self.account_id, tradeID=trade_id)
        client.request(r)

    def get_open_trade(self):
        _trades = self.get_trade_list()
        # print(json.dumps(_trades["trades"], indent=4, sort_keys=True))

        list_of_trade = []
        for trade in _trades["trades"]:
            # print(json.dumps(trade, indent=4, sort_keys=True))
            new_trade = TradeModel(
                trade["id"],
                trade["instrument"],
                trade["initialUnits"],
                trade["openTime"],
                trade["price"],
                trade["initialMarginRequired"],
                trade["state"],
            )
            list_of_trade.append(new_trade)
