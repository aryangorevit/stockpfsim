import math
class Analysis:
    @staticmethod
    def summary(equity_curve):
        if not equity_curve: return {'initial':0,'final':0,'return_pct':0,'max_drawdown_pct':0,'volatility_pct':0}
        initial, final=equity_curve[0],equity_curve[-1]; peak=initial; drawdown=0
        returns=[]
        for prev,cur in zip(equity_curve,equity_curve[1:]):
            if prev: returns.append(cur/prev-1)
            peak=max(peak,cur); drawdown=max(drawdown,(peak-cur)/peak)
        mean=sum(returns)/len(returns) if returns else 0
        vol=(sum((r-mean)**2 for r in returns)/len(returns))**.5 if returns else 0
        return {'initial':initial,'final':final,'return_pct':(final/initial-1)*100 if initial else 0,'max_drawdown_pct':drawdown*100,'volatility_pct':vol*100}
    @staticmethod
    def compare(results):
        return {name:Analysis.summary(result.equity_curve if hasattr(result,'equity_curve') else result) for name,result in results.items()}
