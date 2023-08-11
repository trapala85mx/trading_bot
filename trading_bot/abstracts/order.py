# Python
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from decimal import Decimal


@dataclass(kw_only=True)
class Order(metaclass=ABCMeta):

    @property
    @abstractmethod
    def symbol(self): pass

    @symbol.setter
    @abstractmethod
    def symbol(self, symbol: str): pass

    @property
    @abstractmethod
    def position_side(self): pass

    @position_side.setter
    @abstractmethod
    def position_side(self, position_side: str): pass

    @property
    @abstractmethod
    def position_type(self): pass

    @position_type.setter
    @abstractmethod
    def position_type(self, position_type: str): pass

    @property
    @abstractmethod
    def qty(self): pass

    @qty.setter
    @abstractmethod
    def qty(self, qty: Decimal): pass
