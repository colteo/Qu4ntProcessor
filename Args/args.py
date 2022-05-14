from argparse import ArgumentParser
from Base.base_object import BaseObject
from Args.manual_settings import ManualSettings
from Args.api_settings import ApiSettings
import inspect


class Args(BaseObject):
    def __init__(self):
        super().__init__()
        self.parser = ArgumentParser()
        self.parameters = self.get_args()

    def get_args(self):
        self.parser.add_argument('--manual_mode', required=False, default=False, choices=["True", "False"],
                                 help="Manual mode allow settings load from static file.")
        self.parser.add_argument('--settings_id', required=False, default=None,
                                 help="Settings ID for retrieving Qu4nt settings")
        try:
            args = self.parser.parse_args()
            if self.is_manual_setup(args):
                return ManualSettings().parameters
            else:
                return ApiSettings(args.settings_id).parameters
        except Exception as e:
            self.logger.write_error("Parse args problems. Exception: {}".format(e),
                                    self.__class__.__name__, inspect.stack()[0][3])
            exit(e)

    def is_manual_setup(self, args):
        if args.manual_mode is False and args.settings_id is None:
            self.parser.error("Without settings_id, manual_mode is required to be True.")
        return args.manual_mode
