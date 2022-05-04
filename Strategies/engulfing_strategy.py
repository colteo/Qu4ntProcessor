import inspect
from .strategy import Strategy


class EngulfingStrategy(Strategy):

    def __init__(self, args):
        super().__init__(args)
