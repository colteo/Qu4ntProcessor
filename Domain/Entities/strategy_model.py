class StrategyModel:

    def __init__(self, strategy_name: str, indicators: list, stop_loss, take_profit):
        self.strategy_name = strategy_name
        self.indicators = indicators
        self.stop_loss = stop_loss
        self.take_profit = take_profit

    def reprJSON(self):
        indicators_dict = {}
        for index, indicator in enumerate(self.indicators):
            indicators_dict[index] = indicator.reprJSON()

        return dict(
            strategy_name=self.strategy_name,
            indicators=indicators_dict,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit,
        )

