import oandapyV20
import oandapyV20.endpoints.accounts as accounts
from Brokers.broker_account import BrokerAccount


class OandaBrokerAccount(BrokerAccount):

    def __init__(self, args, account_id, access_token):
        super().__init__(args)
        self.account_id = account_id
        self.access_token = access_token
        self.leverage = 30

    def get_account_details(self):
        client = oandapyV20.API(access_token=self.access_token)
        r = accounts.AccountDetails(self.account_id)
        client.request(r)
        # print(json.dumps(r.response, indent=4, sort_keys=True))
        return r.response

    def get_currency(self):
        details = self.get_account_details()
        currency = details["account"]["currency"]
        return currency

    def get_balance(self):
        details = self.get_account_details()
        balance = details["account"]["balance"]
        balance = int(round(float(balance), 0))
        return balance

    def get_margin_available(self):
        details = self.get_account_details()
        margin_available = details["account"]["marginAvailable"]
        margin_available = int(round(float(margin_available), 0))
        return margin_available

    def get_leverage(self):
        return self.leverage
