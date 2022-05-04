from Domain import *
from pprint import pprint
from datetime import datetime


class IndicatorModel:

    def __init__(self, indicator_name: str, args):
        self.indicator_name = indicator_name
        self.args = args


