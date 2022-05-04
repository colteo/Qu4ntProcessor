import logging
from datetime import datetime
import uuid
from Services.Assistant import AssistantFilesystem
from Singleton import Singleton


class Logger(metaclass=Singleton):

    def __init__(self):
        self.id = str(uuid.uuid4())
        AssistantFilesystem.remove_all('Logs')
        current_datetime = datetime.today().strftime("%Y-%m-%d-%H-%M-%S")
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            filename='Logs/' + current_datetime + '.log',
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




