from enum import Enum


class DataFeedType(Enum):
    by_count = 1
    by_datetime = 2

    def __str__(self):
        return self.value


class DataFeedPriceType(Enum):
    A = 'A'  # Ask
    B = 'B'  # Bid
    M = 'M'  # Middle

    def __str__(self):
        return self.value