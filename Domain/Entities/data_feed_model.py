from Domain.Enum import InstrumentType
from Domain.Enum import GranularityType
from Domain.Enum import DataFeedType
from pprint import pprint
from datetime import datetime
'''
se vengono passati sia count che start_date e end_date le date prevalgono sul count
'''


class DataFeedModel:

    def __init__(self, instrument, granularity, count=None, start_date=None, end_date=None, stream_granularity=GranularityType.M1):
        self.instrument = None
        self.granularity = None
        self.count = None
        self.start_date = None
        self.end_date = None
        self.stream_granularity = None
        self.type = None
        self.init_values(instrument, granularity, count, start_date, end_date, stream_granularity)
        self.define_type()

    def init_values(self, instrument, granularity, count, start_date, end_date, stream_granularity):
        if isinstance(instrument, InstrumentType):
            self.instrument = instrument

        if isinstance(granularity, GranularityType):
            self.granularity = granularity

        if isinstance(count, int):
            self.count = count

        format = "%Y-%m-%d"

        if isinstance(start_date, datetime):
            self.start_date = start_date
        elif isinstance(start_date, str):
            res = True
            # using try-except to check for truth value
            try:
                res = bool(datetime.strptime(start_date, format))
            except ValueError:
                res = False
            if res:
                self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

        if isinstance(end_date, datetime):
            self.end_date = end_date
        elif isinstance(end_date, str):
            res = True
            # using try-except to check for truth value
            try:
                res = bool(datetime.strptime(end_date, format))
            except ValueError:
                res = False
            if res:
                self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        if stream_granularity is not None:
            self.stream_granularity = stream_granularity

    def define_type(self):
        # TODO verificare se serve o no
        # self.check_if_is_valid()
        if self.start_date is not None and self.end_date is not None:
            self.type = DataFeedType.by_datetime
            self.count = None
        elif self.count is not None:
            self.type = DataFeedType.by_count
            self.start_date = None
            self.end_date = None

    def check_if_is_valid(self) -> str:
        if (
                self.instrument is None
                or self.granularity is None
                or
                (
                    self.count is None
                    and
                    (
                        self.start_date is None
                        or self.end_date is None
                    )
                )
        ):
            print("Errore modello non valido")
            exit()

    def print_yourself(self):
        pprint(vars(self))
