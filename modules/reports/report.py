from modules.analysis import Analysis
def text_report(result, title='Simulation report'):
    s=Analysis.summary(result.equity_curve)
    return '\n'.join([title,'='*len(title),f"Initial equity: {s['initial']:.2f}",f"Final equity: {s['final']:.2f}",f"Return: {s['return_pct']:.2f}%",f"Max drawdown: {s['max_drawdown_pct']:.2f}%",f"Volatility: {s['volatility_pct']:.2f}%",f"Trades: {len(result.transactions)}"])
def plot_equity(result, path=None):
    try:
        import matplotlib.pyplot as plt
    except ImportError: return False
    plt.plot(result.equity_curve); plt.xlabel('Day'); plt.ylabel('Equity'); plt.title('Equity curve'); plt.tight_layout()
    if path: plt.savefig(path); plt.close()
    else: plt.show()
    return True
