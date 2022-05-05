from enum import Enum


class GranularityType(Enum):
    D = 'D'
    H1 = 'H1'
    M15 = 'M15'
    M30 = 'M30'
    S15 = 'S15'
    S5 = 'S5'

    def __str__(self):
        return self.value

