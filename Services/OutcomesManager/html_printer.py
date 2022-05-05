from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import tempfile
import webbrowser
from Domain.Enum import PositionType
from Base import BaseObject

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


class HTMLPrinter(BaseObject):

    def __init__(self, data_main, data_stream, outcomes):
        super().__init__()
        self.last_outcome = None
        self.outcomes = outcomes
        self.data_main = data_main
        self.data_stream = data_stream

        self.print_outcomes()

    def print_outcomes(self):
        env = Environment(loader=FileSystemLoader("Services/OutcomesManager/"))
        template = env.get_template("TableTemplate.html")  # the template file name
        context_data = {
            'tabular_data': []
        }
        # context_data["tabular_data"].append(Row("a", "b", "c", "d"))

        for index, row in self.data_stream.reset_index().iterrows():
            row_data_main = self.get_row_data_main_by_open_time(row.Time)
            outcome = self.get_outcome_by_open_time(row.Time)

            ask_class = bid_class = difference = ""
            if outcome is not None:
                self.last_outcome = outcome
                ask_class, bid_class = self.define_ask_bid_class()

            if self.last_outcome is not None:
                difference = self.calc_difference(row)

            if self.last_outcome is not None and row.Time == self.last_outcome.order.stream_row.Time:
                self.last_outcome = None

            if row_data_main is not None:
                print(row_data_main.iloc[0].Open)

            row = Row(
                row.Time,
                str(row.Ask).replace(".", ","),
                ask_class,
                str(row.Bid).replace(".", ","),
                bid_class,
                row_data_main.iloc[0].Open if row_data_main is not None else "",
                row_data_main.iloc[0].Close if row_data_main is not None else "",
                outcome.trade.trade_id if outcome is not None else "",
                outcome.trade.instrument if outcome is not None else "",
                round(outcome.trade.margin_used, 2) if outcome is not None else "",
                outcome.trade.position_type if outcome is not None else "",
                outcome.trade.units if outcome is not None else "",
                outcome.order.price if outcome is not None else "",
                difference,
                outcome.order.order_type if outcome is not None else "",
                outcome.order.stream_row.Time if outcome is not None else "",
                outcome.order.stream_row.Ask if outcome is not None else "",
                outcome.order.stream_row.Bid if outcome is not None else "",
                round(outcome.initial_balance, 2) if outcome is not None else "",
                round(outcome.final_balance, 2) if outcome is not None else "",
            )

            context_data["tabular_data"].append(row)

        html = template.render(**context_data)
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            url = 'file://' + f.name
            f.write(html)
        webbrowser.open(url)

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


