import inspect
from .processor import Processor
from Services.Assistant import AssistantDataframe, Assistant


class BacktestProcessor(Processor):

    def __init__(self, args):
        super().__init__(args)
