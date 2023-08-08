# Python
from abc import ABCMeta, abstractmethod


# Project
# Third Party


class Order(metaclass=ABCMeta):

    def __init__(self, price: float, qty: float, stop_loss: float):
        self._price = price
        self._qty = qty
        self._stop_loss = stop_loss

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price: float):
        self._price = price

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, qty: float):
        self._qty = qty

    @property
    def stop_loss(self):
        return self._stop_loss

    @stop_loss.setter
    def stop_loss(self, stop_loss: float):
        self._stop_loss = stop_loss

