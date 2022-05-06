class StrategyModel:

    def __init__(self, strategy_name: str, indicators: list, stop_loss, take_profit):
        self.strategy_name = strategy_name
        self.indicators = indicators
        self.stop_loss = stop_loss
        self.take_profit = take_profit


