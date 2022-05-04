from enum import Enum


class Status(Enum):
    NONE = "NONE"
    SENT = "SENT"
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    # canceled = 4
    # rejected = 5
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"

    def __str__(self):
        return self.value
