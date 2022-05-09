import inspect
import time
from .processor import Processor
from Services.Assistant import AssistantDataframe, Assistant


class LiveProcessor(Processor):

    def __init__(self, args):
        super().__init__(args)
