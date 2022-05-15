import logging
from datetime import datetime
import uuid
import os
from Services.Assistant import AssistantFilesystem
from Singleton import Singleton
import inspect


class Logger(metaclass=Singleton):

    def __init__(self):
        self.id = str(uuid.uuid4())
        logs_path = self.get_logs_path()

        current_datetime = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        filename = os.path.join(logs_path, '.'.join((current_datetime, "log")))

        AssistantFilesystem.remove_all(logs_path)
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            filename=filename,
            datefmt='%Y-%m-%d %H:%M:%S',
            level=logging.INFO,
        )
        # self.write_info('Logger init')

    def write_info(self, message, sender_class=None):
        logging.info(self._write(message))

    def write_error(self, message, sender_class=None):
        logging.error(self._write(message))

    def _write(self, message) -> str:
        stack = inspect.stack()
        sender = stack[2][0].f_locals["self"].__class__.__name__
        method = stack[2][0].f_code.co_name
        return "Sender: {} - Method: {} - Message {}".format(sender, method, message)

    def get_logs_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, os.pardir, "Logs", ""))



