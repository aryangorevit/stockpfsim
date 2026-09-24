from dataclasses import dataclass, field
from datetime import date
from random import Random
from typing import Dict, Iterable
from modules.models import Stock, ValidationError

@dataclass
class Market:
    stocks: Dict[str, Stock] = field(default_factory=dict)
    day: int = 0
    def add_stock(self, stock):
        if stock.symbol in self.stocks: raise ValidationError(f"Stock {stock.symbol} already exists")
        self.stocks[stock.symbol] = stock
    def quote(self, symbol):
        try: return self.stocks[symbol.upper()].price
        except KeyError: raise ValidationError(f"Unknown symbol: {symbol}")
    def step(self, rng=None, volatility=.02, drift=.0005):
        if volatility < 0: raise ValidationError("Solatility cannot be negative")
        rng = rng or Random(); self.day += 1
        for stock in self.stocks.values(): stock.update_price(stock.price * (1 + drift + rng.gauss(0, volatility)))
    def snapshot(self): return {s: st.price for s,st in self.stocks.items()}
    def to_dict(self): return {'day':self.day, 'stocks':{k:v.to_dict() for k,v in self.stocks.items()}}
    @classmethod
    def from_dict(cls,d): return cls({k:Stock.from_dict(v) for k,v in d.get('stocks',{}).items()},d.get('day',0))

def default_market():
    m=Market()
    for symbol,name,price,sector in [('INFY','Infosys Ltd.',1014,'Technology'),('NVDA','Nvidia',22357,'Technology'),('CIPLA','Cipla',1343,'Healthcare'),('ADNPW','Adani Power Ltd.',199,'Energy'),('HDFC','HDFC Bank Ltd',728,'Finance')]: m.add_stock(Stock(symbol,name,price,sector=sector))
    return m
