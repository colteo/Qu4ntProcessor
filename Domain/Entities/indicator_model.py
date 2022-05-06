class IndicatorModel:

    def __init__(self, indicator_name: str, args):
        self.indicator_name = indicator_name
        self.args = args

    def reprJSON(self):
        return dict(
            indicator_name=self.indicator_name,
            args=self.args,
        )


