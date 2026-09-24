from datetime import datetime, timezone
from modules.models import Portfolio, Transaction, Position, ValidationError
class TradingEngine:
    def __init__(self, portfolio=None, fee_rate=.001):
        self.portfolio=portfolio or Portfolio(); self.fee_rate=fee_rate
        if fee_rate < 0: raise ValidationError('Fee_rate cannot be negative')
    def buy(self, market, symbol, shares): return self._trade(market,symbol,shares,'BUY')
    def sell(self, market, symbol, shares): return self._trade(market,symbol,shares,'SELL')
    def _trade(self,market,symbol,shares,side):
        symbol=symbol.upper(); shares=int(shares)
        if shares <= 0: raise ValidationError('Shares must be a positive integer')
        price=market.quote(symbol); fee=price*shares*self.fee_rate
        if side=='BUY':
            total=price*shares+fee
            if total > self.portfolio.cash + 1e-9: raise ValidationError('Insufficient cash')
            old=self.portfolio.positions.get(symbol,Position(symbol)); total_shares=old.shares+shares
            old.average_cost=(old.shares*old.average_cost+total)/total_shares; old.shares=total_shares; self.portfolio.positions[symbol]=old; self.portfolio.cash-=total
        else:
            old=self.portfolio.positions.get(symbol)
            if not old or old.shares < shares: raise ValidationError('Insufficient shares')
            old.shares-=shares; self.portfolio.cash += price*shares-fee
            if not old.shares: del self.portfolio.positions[symbol]
        tx=Transaction(datetime.now(timezone.utc).isoformat(),symbol,side,shares,price,fee); self.portfolio.transactions.append(tx); return tx
    def value(self,market): return self.portfolio.equity(market)
