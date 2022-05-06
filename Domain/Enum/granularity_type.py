from enum import Enum


class GranularityType(Enum):
    D = 'D'
    H1 = 'H1'
    M30 = 'M30'
    M15 = 'M15'
    M5 = 'M5'
    M1 = 'M1'
    S15 = 'S15'
    S5 = 'S5'

    def __str__(self):
        return self.value

