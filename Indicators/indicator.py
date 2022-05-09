import inspect
from Event import EventHook
from Base import BaseObject


class Indicator(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.indicator_event = EventHook()
        self.signals = []

    def next(self):
        pass

    def add_signal(self, signal_dict):
        self.signals.append(signal_dict)


