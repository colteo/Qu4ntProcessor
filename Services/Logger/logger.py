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
        logging.info(self._write(message, sender_class))

    def write_error(self, message, sender_class=None):
        logging.error(self._write(message, sender_class))

    def _write(self, message, sender_class) -> str:
        result = ""

        sender = "Sender: not defined - "
        if sender_class is not None:
            sender = "Sender: " + sender_class + " - "
        result += sender

        method_name = "Method: " + inspect.stack()[2][3]
        result += method_name

        message = "Message: " + message
        result += message

        return result

    def get_logs_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, os.pardir, "Logs", ""))



