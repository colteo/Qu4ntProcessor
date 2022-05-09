import inspect
import sys
from Base import BaseObject
from Domain.Enum import PositionType
from Domain.Enum import ProcessorType
from Domain.Enum import OrderType
from Domain.Enum import Status
from Services.Assistant import AssistantDataframe, Assistant
from Services.Communications import Telegram
from Brokers import OandaBroker, Qu4ntBroker
from Strategies import *
from Domain.Enum import InstrumentType
from Domain.Entities import OrderModel


class Processor(BaseObject):
    def __init__(self, args):
        super().__init__()
        self.strategy = None
        self.broker = None
        self.telegram = None
        self.args = args

        self.init_broker()
        self.init_strategy()

        self.init_communicator()

    def run(self):
        pass

    def init_broker(self):
        try:
            broker = self.args.parameters.broker
        except:
            broker = None
        if broker is not None:
            class_ = getattr(sys.modules[__name__], broker.broker_name)
            self.broker = class_(self.args)

    def init_strategy(self):
        try:
            strategy = self.args.parameters.strategy
        except:
            strategy = None

        if strategy is None:
            # self.logger.write_info("Inizializzo strategia vuota", self.__class__.__name__, inspect.stack()[0][3])
            self.strategy = EmptyStrategy(self.args)
        else:
            class_ = getattr(sys.modules[__name__], strategy.strategy_name)
            self.strategy = class_(self.args)

        self.strategy.strategy_event += self.event_received

    def init_communicator(self):
        self.telegram = Telegram()

    def event_received(self, position_type, stop_loss=None, take_profit=None, trailing_profit=None):
        """
        Questo metodo fa da intermediario, tra broker e strategy.
        Basto su eventi a catena indicator -> strategy -> processor

        Qui abbiamo il self.index che ha valore successivo a quello in cui si è verificato l'evento nell'indicatore.
        (se ci sono problemi spostare l'incremento di index sotto strategy.next nel metodo run)
        Il che dovrebbe essere corretto per i backtest.
        capire live
        """
        self.telegram.send("evento ricevuto")
        print("evento ricevuto")

        trades = self.broker.trade_manager.get_open_trade()
        if len(trades) == 1:
            # print("sei nella if trades == 1")
            trade = trades[0]

            if position_type is trade.position_type:
                return
            else:
                result = self.broker.trade_manager.close_trade_without_order(
                    trade=trade,
                    order=OrderModel(
                        order_id=len(self.broker.order_manager.orders),
                        trade_id=trade.trade_id,
                        price=None,
                        state=Status.OPEN,
                        order_type=OrderType.FORCED_CLOSURE
                    )
                )
                if result:
                    self.broker.order_manager.close_related_orders_by_trade_id(trade.trade_id)

                self.open_trade(position_type)
        elif len(trades) == 0:
            # print("sei nella if trades == 0")
            self.open_trade(position_type)
        elif len(trades) > 1:
            # TODO chiudere tutto
            print("sei nella else trades > 1")
            self.logger.write_error("Errore ho trovato più di un trade aperto", self.__class__.__name__, inspect.stack()[0][3])
            exit()

    def open_trade(self, position_type):
        units = self.calc_units(position_type)
        if units is None:
            return

        result, response = self.broker.market_order_request(
            units
        )
        if result:
            self.broker.stop_loss_order_request(
                response,
                self.strategy.stop_loss
            )
            self.broker.take_profit_order_request(
                response,
                self.strategy.take_profit
            )
        pass

    def calc_units(self, position_type):
        units = 0
        if position_type is PositionType.LONG:
            units = self.strategy.sizer.calc_units(
                self.broker.account.get_margin_available(),
                self.broker.account.get_leverage(),
                self.broker.pricing.get_current_ask(),
            )
        elif position_type is PositionType.SHORT:
            units = self.strategy.sizer.calc_units(
                self.broker.account.get_margin_available(),
                self.broker.account.get_leverage(),
                self.broker.pricing.get_current_ask(),
            )
            units = -units
        return units

