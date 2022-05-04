from dependency_injector import containers, providers
from Processors import BacktestProcessor, LiveProcessor


class ContainerProcessors(containers.DeclarativeContainer):
    backtest_processor_provider = providers.Singleton(BacktestProcessor)
    live_processor_provider = providers.Singleton(LiveProcessor)
