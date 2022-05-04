import inspect
from Services.Logger import Logger


class BaseObject(object):
    def __init__(self):
        self.logger = None

        self.name = self.__class__.__name__
        self.init_logger()
        self.logger.write_info("Init della classe: " + self.name, self.__class__.__name__, inspect.stack()[0][3])

    def init_logger(self):
        self.logger = Logger()
