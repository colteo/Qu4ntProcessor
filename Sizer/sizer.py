from Base import BaseObject
from enum import Enum


class MoneyManagementType(Enum):
    ALL_IN = 'ALL_IN'

    def __str__(self):
        return self.value


class Sizer(BaseObject):

    def __init__(self, args):
        super().__init__()
        self.args = args
        self.type_of_money_management = MoneyManagementType.ALL_IN

    def calc_units(self, margin_available, leverage, price):
        # print(margin_available)
        # print(leverage)
        # print(price)

        if price is None:
            return None

        if self.type_of_money_management is MoneyManagementType.ALL_IN:
            # impostato a 0.95 per evitare errori tipo fondi non sufficienti
            multiplier = 0.95
            # multiplier = 2
            units = round(((margin_available * multiplier) * leverage) / price, 0)
            return units
