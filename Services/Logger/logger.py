import logging
from datetime import datetime
import uuid
import os
from Services.Assistant import AssistantFilesystem
from Singleton import Singleton


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

    def write_info(self, message, sender_class=None, method_name=None):
        logging.info(self._write(message, sender_class, method_name))

    def write_error(self, message, sender_class=None, method_name=None):
        logging.error(self._write(message, sender_class, method_name))

    def _write(self, message, sender_class, method_name) -> str:
        result = ""

        sender = "Sender: not defined - "
        if sender_class is not None:
            sender = "Sender: " + sender_class + " - "
        result += sender

        method = "Method: not defined - "
        if method_name is not None:
            method = "Method: " + method_name + " - "
        result += method

        message = "Message: " + message
        result += message

        return result

    def get_logs_path(self):
        this_file_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.abspath(os.path.join(this_file_path, os.pardir, "Logs", ""))



