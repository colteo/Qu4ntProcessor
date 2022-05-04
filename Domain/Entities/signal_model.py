

class SignalModel:

    def __init__(self, name, time, marker, symbol, color):
        self.name = name
        self.time = time
        self.marker = marker
        self.symbol = symbol
        self.color = color

    def to_dict(self):
        return {
            'name': self.name,
            'time': self.time,
            'marker': self.marker,
            'symbol': self.symbol,
            'color': self.color,
        }
