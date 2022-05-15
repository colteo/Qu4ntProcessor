from Brokers.broker_account import BrokerAccount
from Singleton import Singleton
import uuid


class Qu4ntBrokerAccount(BrokerAccount, metaclass=Singleton):

    def __init__(self, args):
        super().__init__(args)
        self.leverage = None
        self.margin_available = None
        self.balance = None
        self.initial_balance = None
        self.currency = None

        self.id = str(uuid.uuid4())

        self.args = args
        self.init_values()
        
    def init_values(self):
        self.set_currency(self.args.parameters.broker.args["currency"])
        self.set_initial_balance(int(self.args.parameters.broker.args["balance"]))
        self.set_balance(int(self.args.parameters.broker.args["balance"]))
        self.set_margin_available(int(self.args.parameters.broker.args["balance"]))
        self.set_leverage(int(self.args.parameters.broker.args["leverage"]))

    def set_currency(self, currency):
        self.currency = currency

    def get_currency(self):
        return self.currency

    def set_balance(self, balance):
        self.balance = balance

    def get_balance(self):
        return self.balance

    def set_initial_balance(self, initial_balance):
        self.initial_balance = initial_balance

    def get_initial_balance(self):
        return self.initial_balance

    def get_margin_available(self):
        return self.margin_available

    def set_margin_available(self, margin_available):
        self.margin_available = margin_available

    def get_leverage(self):
        return self.leverage

    def set_leverage(self, leverage):
        self.leverage = leverage
