class Asset:
    """Represetns an Asset
    """    
    def __init__(self, symbol: str):
        self._symbol = symbol.lower()
        self._price_precision = None
        self._qty_precision = None
        self._min_qty = None
        self._min_price = None

    #
    def __str__(self):
        return f"Symbol: {self._symbol.upper()}\nPrice Precision: {self._price_precision}\n" + \
            f"Quantity Precision:{self._qty_precision}\nMinimum Quantity: {self._min_qty}\n" + \
            f"Minimum Price: ${self._min_price}"

    # GETTER
    @property
    def symbol(self):
        return self._symbol

    @property
    def price_precision(self):
        return self._price_precision

    @property
    def qty_precision(self):
        return self._qty_precision

    @property
    def min_qty(self):
        return self._min_qty

    @property
    def min_price(self):
        return self._min_price

    # SETTER
    @price_precision.setter
    def price_precision(self, price_precision: str):
        self._price_precision = price_precision

    @qty_precision.setter
    def qty_precision(self, qty_precision: str):
        self._qty_precision = qty_precision

    @min_qty.setter
    def min_qty(self, min_qty: str):
        self._min_qty = min_qty

    @min_price.setter
    def min_price(self, min_price: str):
        self._min_price = min_price
