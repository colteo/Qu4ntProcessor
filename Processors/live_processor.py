import inspect
import time
from .processor import Processor
from Services.Assistant import AssistantDataframe, Assistant


class LiveProcessor(Processor):

    def __init__(self, args):
        super().__init__(args)

    def run(self):
        self.logger.write_info(
            "Inizio elaborazione",
            self.__class__.__name__,
            inspect.stack()[0][3]
        )
        self.broker.trade_manager.close_all_trade()
        while True:
            time.sleep(5)
            result, price = self.broker.pricing.get_current_middle_price()

            # if result is False or price is None:
            #     break

            if result:
                self.strategy.df = AssistantDataframe.add_row_to_dataframe(
                    self.strategy.df,
                    price,
                    AssistantDataframe.columns_data_main_by_date()
                )
                self.strategy.next()


