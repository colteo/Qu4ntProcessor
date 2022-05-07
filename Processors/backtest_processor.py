import inspect
from .processor import Processor
from Services.Assistant import AssistantDataframe, Assistant


class BacktestProcessor(Processor):

    def __init__(self, args):
        super().__init__(args)

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

            if len(self.broker.trade_manager.get_open_trade()) > 0:
                self.broker.check_trade_and_related_orders()
