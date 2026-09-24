from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Dict, List

class ValidationError(ValueError): pass

def _positive(value, name):
    if value <= 0: raise ValidationError(f"{name} must be positive")

@dataclass
class Stock:
    symbol: str
    name: str
    price: float
    shares_outstanding: int = 1_000_000
    sector: str = "General"
    history: List[float] = field(default_factory=list)
    def __post_init__(self):
        self.symbol = self.symbol.strip().upper()
        if not self.symbol or not self.name.strip(): raise ValidationError("Symbol and name are required")
        _positive(self.price, "price")
        if self.shares_outstanding < 1: raise ValidationError("Shares_outstanding must be positive")
        if not self.history: self.history = [float(self.price)]
    def update_price(self, new_price: float):
        _positive(new_price, "price")
        self.price = round(float(new_price), 4); self.history.append(self.price)
    @property
    def change(self): return self.price - self.history[-2] if len(self.history) > 1 else 0.0
    @property
    def change_percent(self): return self.change / self.history[-2] * 100 if len(self.history)>1 else 0.0
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls, d): return cls(**d)

@dataclass
class Position:
    symbol: str
    shares: int = 0
    average_cost: float = 0.0
    def market_value(self, price): return self.shares * price
    def to_dict(self): return asdict(self)

@dataclass
class Transaction:
    timestamp: str
    symbol: str
    side: str
    shares: int
    price: float
    fee: float = 0.0
    def __post_init__(self):
        self.side = self.side.upper()
        if self.side not in ('BUY','SELL'): raise ValidationError("side must be BUY or SELL")
        if self.shares <= 0: raise ValidationError("shares must be positive")
        _positive(self.price, "price")
    @property
    def total(self): return self.shares * self.price + self.fee if self.side == 'BUY' else self.shares * self.price - self.fee
    def to_dict(self): return asdict(self)

@dataclass
class Portfolio:
    cash: float = 10000.0
    positions: Dict[str, Position] = field(default_factory=dict)
    transactions: List[Transaction] = field(default_factory=list)
    initial_cash: float = 10000.0
    def __post_init__(self):
        _positive(self.cash, "cash")
        if self.initial_cash <= 0: self.initial_cash = self.cash
    def equity(self, market):
        def price(symbol):
            quote = market.quote(symbol) if hasattr(market, "quote") else market[symbol].price
            return quote
        return self.cash + sum(p.market_value(price(p.symbol)) for p in self.positions.values())
    def to_dict(self):
        return {'cash': self.cash, 'initial_cash': self.initial_cash, 'positions': {k:v.to_dict() for k,v in self.positions.items()}, 'transactions':[t.to_dict() for t in self.transactions]}
    @classmethod
    def from_dict(cls, d):
        return cls(d['cash'], {k:Position(**v) for k,v in d.get('positions',{}).items()}, [Transaction(**t) for t in d.get('transactions',[])], d.get('initial_cash', d['cash']))
