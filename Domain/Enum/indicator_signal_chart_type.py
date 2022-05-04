from enum import Enum


class IndicatorSignalChartType(Enum):
    marker = 'marker'
    line = 'line'

    def __str__(self):
        return self.value

