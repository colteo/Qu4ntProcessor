from dependency_injector import containers, providers
from Services.Logger import *


class ContainerLogs(containers.DeclarativeContainer):
    logger_provider = providers.Singleton(Logger)

