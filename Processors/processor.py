import inspect
import sys
from Base import BaseObject
from Domain.Enum import PositionType
from Domain.Enum import ProcessorType
from Domain.Enum import OrderType
from Services.Assistant import AssistantDataframe, Assistant
from Services.Communications import Telegram
from Brokers import OandaBroker, Qu4ntBroker
from Strategies import *
from Domain.Enum import InstrumentType


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
        self.logger.write_info(
            "Inizio elaborazione",
            self.__class__.__name__,
            inspect.stack()[0][3]
        )

        while True:
            result, price = self.broker.pricing.get_current_middle_price()
            if result is False or price is None:
                break

            self.strategy.df = AssistantDataframe.add_row_to_dataframe(
                self.strategy.df,
                price,
                AssistantDataframe.columns_data_main_by_date()
            )
            self.strategy.next()

            if self.args.parameters.processor_type == ProcessorType.backtest:
                if len(self.broker.trade_manager.get_open_trade()) > 0:
                    self.broker.check_trade_and_related_orders()

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
        # self.telegram.send("evento ricevuto")
        # print("evento ricevuto")
        # print(position_type)
        if position_type is PositionType.LONG:
            units = self.strategy.sizer.calc_units(
                self.broker.account.get_margin_available(),
                self.broker.account.get_leverage(),
                self.broker.pricing.get_current_ask(),
            )
            print(units)

            # units = 10000
        elif position_type is PositionType.SHORT:
            units = self.strategy.sizer.calc_units(
                self.broker.account.get_margin_available(),
                self.broker.account.get_leverage(),
                self.broker.pricing.get_current_ask(),
            )
            units = -units
            print(units)

            # units = -10000

        result, response = self.broker.market_order_request(
            InstrumentType.eurusd.value,
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


