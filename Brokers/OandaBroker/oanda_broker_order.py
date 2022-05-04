from Services.Assistant import Assistant
from Brokers.broker_order import BrokerOrder
import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest, TakeProfitOrderRequest, StopLossOrderRequest


class OandaBrokerOrder(BrokerOrder):

    def __init__(self, args, account_id, access_token, trade_manager):
        super().__init__(args)
        self.account_id = account_id
        self.access_token = access_token
        self.trade_manager = trade_manager

    def market_order_request(self, instrument, units):
        mo = MarketOrderRequest(instrument=instrument, units=units)
        return self._create_order(mo.data)

    def take_profit_order_request(self, trade_id, pips):
        price = self.calc_take_profit_price(trade_id, pips)
        ordr = TakeProfitOrderRequest(tradeID=trade_id, price=price)
        return self._create_order(ordr.data)

    def stop_loss_order_request(self, trade_id, pips):
        price = self.calc_stop_loss_price(trade_id, pips)
        ordr = StopLossOrderRequest(tradeID=trade_id, price=price)
        return self._create_order(ordr.data)

    def _create_order(self, data):
        client = oandapyV20.API(access_token=self.access_token)
        r = orders.OrderCreate(self.account_id, data=data)
        rv = client.request(r)

        # print(json.dumps(rv, indent=4))

        return self.handle_response(rv)

    def handle_response(self, response):
        if "orderCancelTransaction" in response:
            reason = response["orderCancelTransaction"]["reason"]
            return False, reason
        else:
            if "orderFillTransaction" in response:
                trade_id = response["orderFillTransaction"]["tradeOpened"]["tradeID"]
                return True, trade_id

            return True, None
