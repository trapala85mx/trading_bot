# Python
from decimal import Decimal
from dataclasses import dataclass
# Project
from abstracts.order import Order
# Third Party


@dataclass(kw_only=True)
class MarketOrder(Order):

    def __init__(self, symbol: str, position_side: str, position_type: str, qty: Decimal):
        self.symbol = symbol
        self.position_side = position_side
        self.position_type = position_type
        self.qty = qty

    @property
    def symbol(self):
        return self.symbol

    @symbol.setter
    def symbol(self, symbol: str):
        if len(symbol) > 0:
            self.symbol = symbol.upper()
        raise ValueError("You must send a symbol")

    @property
    def position_side(self):
        return self.position_side

    @position_side.setter
    def position_side(self, position_side: str):
        self.position_side = position_side

    @property
    def position_type(self):
        return self.position_type

    @position_type.setter
    def position_type(self, pos_type: str):
        self.position_type = pos_type

    @property
    def qty(self):
        return self.qty

    @qty.setter
    def qty(self, qty: Decimal):
        self.qty = qty