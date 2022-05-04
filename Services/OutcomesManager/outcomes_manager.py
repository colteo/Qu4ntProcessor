from Base import BaseObject
from Services.Assistant import Assistant
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple
import tempfile
import webbrowser

#  https://stackoverflow.com/questions/52776955/creating-a-html-table-with-python-with-multiple-columns-for-a-specific-row
#  Row = namedtuple("Row", ["one", "two", "three", "four"])
Row = namedtuple(
    "Row",
    [
        "Time",
        "Ask",
        "Bid",
        "TradeID",
        "Instrument",
        "TradePrice",
        "Margin",
        "Position",
        "Units",
        "OrderID",
        "OrderTradeID",
        "OrderPrice",
        "OrderType",
        "OrderTime",
        "OrderAsk",
        "OrderBid",
        "InitialBalance",
        "FinalBalance",
    ]
)


class OutcomesManager(BaseObject):

    def __init__(self, args, data_main, data_stream, outcomes):
        super().__init__()
        self.args = args
        self.outcomes = outcomes
        self.data_main = data_main
        self.data_stream = data_stream

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

            row = Row(
                row.Time,
                row.Ask,
                row.Bid,
                outcome.trade.trade_id if outcome is not None else "",
                outcome.trade.instrument if outcome is not None else "",
                outcome.trade.price if outcome is not None else "",
                round(outcome.trade.margin_used, 2) if outcome is not None else "",
                outcome.trade.position_type if outcome is not None else "",
                outcome.trade.units if outcome is not None else "",
                outcome.order.order_id if outcome is not None else "",
                outcome.order.trade_id if outcome is not None else "",
                outcome.order.price if outcome is not None else "",
                outcome.order.order_type if outcome is not None else "",
                outcome.order.stream_row.Time if outcome is not None else "",
                outcome.order.stream_row.Ask if outcome is not None else "",
                outcome.order.stream_row.Bid if outcome is not None else "",
                outcome.initial_balance if outcome is not None else "",
                outcome.final_balance if outcome is not None else "",
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
