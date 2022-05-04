import inspect
from .processor import Processor


class BacktestProcessor(Processor):

    def __init__(self, args):
        super().__init__(args)

