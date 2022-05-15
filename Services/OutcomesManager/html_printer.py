from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import tempfile
import webbrowser
from Domain.Enum import PositionType
from Base import BaseObject
import os

#  https://stackoverflow.com/questions/52776955/creating-a-html-table-with-python-with-multiple-columns-for-a-specific-row
#  Row = namedtuple("Row", ["one", "two", "three", "four"])
Row = namedtuple(
    "Row",
    [
        "Time",
        "Ask",
        "AskClass",
        "Bid",
        "BidClass",
        "Open",
        "Close",
        "TradeID",
        "Instrument",
        "Margin",
        "Position",
        "Units",
        "OrderPrice",
        "Difference",
        "OrderType",
        "OrderTime",
        "OrderAsk",
        "OrderBid",
        "InitialBalance",
        "FinalBalance",
    ]
)

RowNew = namedtuple(
    "Row",
    [
        "Position",
        "OpenTime",
        "TradeAsk",
        "TradeBid",
        "TradeMiddle",
        "Price",
        "Margin",
        "Units",
        "OrderType",
        "CloseTime",
        "OrderAsk",
        "OrderBid",
        "OrderMiddle",
        "Initial",
        "Final",
    ]
)


class HTMLPrinter(BaseObject):

    def __init__(self, data_main, data_stream, outcomes):
        super().__init__()
        self.last_outcome = None
        self.outcomes = outcomes
        self.data_main = data_main
        self.data_stream = data_stream

        self.print_outcomes_new()

    def print_outcomes_new(self):
        env = Environment(loader=FileSystemLoader(self.get_config_path()))
        template = env.get_template("TableTemplateNew.html")  # the template file name
        context_data = {
            'tabular_data': []
        }

        for outcome in self.outcomes:
            row = RowNew(
                outcome.trade.position_type,
                outcome.trade.open_time,
                outcome.trade.stream_row.Ask,
                outcome.trade.stream_row.Bid,
                round((outcome.trade.stream_row.Ask + outcome.trade.stream_row.Bid) / 2, 5),
                outcome.trade.price,
                round(outcome.trade.margin_used, 2),
                outcome.trade.units,
                outcome.order.order_type,
                outcome.order.stream_row.Time,
                outcome.order.stream_row.Ask,
                outcome.order.stream_row.Bid,
                round((outcome.order.stream_row.Ask + outcome.order.stream_row.Bid) / 2, 5),
                round(outcome.initial_balance, 2),
                round(outcome.final_balance, 2)
            )

            context_data["tabular_data"].append(row)

        html = template.render(**context_data)
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            url = 'file://' + f.name
            f.write(html)
        webbrowser.open(url)

        pass

    def get_outcome_by_open_time(self, time):
        result = [outcome for outcome in self.outcomes if outcome.trade.open_time == time]
        if len(result) > 1:
            print("Errore trovati troppi outcome")
            exit()

        if len(result) > 0:
            return result[0]

        return None

    def get_row_data_main_by_open_time(self, time):
        row = self.data_main.reset_index().loc[(self.data_main.index == time)]
        if row.empty:
            return None

        return row

    def define_ask_bid_class(self):
        if self.last_outcome.trade.position_type is PositionType.LONG:
            return "ask-used", ""
        elif self.last_outcome.trade.position_type is PositionType.SHORT:
            return "", "bid-used"

    def calc_difference(self, row):
        if self.last_outcome.trade.position_type is PositionType.LONG:
            result = row.Bid - self.last_outcome.trade.price
        elif self.last_outcome.trade.position_type is PositionType.SHORT:
            result = row.Ask - self.last_outcome.trade.price
        return round(result * 10000, 5)

    def get_config_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, "OutcomesManager"))

