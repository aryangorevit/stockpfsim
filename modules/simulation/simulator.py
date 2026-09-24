from dataclasses import dataclass, field
from random import Random
from modules.market import Market, default_market
from modules.models import Portfolio
from modules.trading import TradingEngine
@dataclass
class SimulationResult:
    equity_curve: list = field(default_factory=list)
    prices: list = field(default_factory=list)
    transactions: list = field(default_factory=list)
    final_cash: float = 0.0
    def to_dict(self): return {'equity_curve':self.equity_curve,'prices':self.prices,'transactions':[t.to_dict() for t in self.transactions],'final_cash':self.final_cash}
class Simulator:
    def __init__(self, market=None, portfolio=None, seed=None): self.market=market or default_market(); self.engine=TradingEngine(portfolio); self.rng=Random(seed)
    def run(self, days=30, strategy=None, volatility=.02):
        if not isinstance(days,int) or days < 0: raise ValueError('days must be a non-negative integer')
        result=SimulationResult([self.engine.value(self.market)], [self.market.snapshot()], [], self.engine.portfolio.cash)
        for day in range(days):
            self.market.step(self.rng,volatility)
            if strategy: strategy(self.market,self.engine,day)
            result.equity_curve.append(round(self.engine.value(self.market),4)); result.prices.append(self.market.snapshot())
        result.transactions=list(self.engine.portfolio.transactions); result.final_cash=self.engine.portfolio.cash; return result
