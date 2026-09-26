import argparse
from pathlib import Path

from modules.analysis import Analysis
from modules.market import default_market
from modules.models import Portfolio, ValidationError
from modules.reports import plot_equity, text_report
from modules.simulation import Simulator
from modules.storage import JsonStore, export_equity
#Table titles 
def _show_market(sim):
    print("\nSymbol  Name                  Sector        Price       Change")
    print("-" * 67)
    for stock in sim.market.stocks.values():
        print(f"{stock.symbol:<7} {stock.name:<21} {stock.sector:<13} "
              f"₹{stock.price:>8.2f}  {stock.change_percent:>7.2f}%")
#Portfolio showcase
def _show_portfolio(sim):
    portfolio = sim.engine.portfolio
    print(f"\nCash: ₹{portfolio.cash:,.2f}")
    print(f"Total value: ₹{sim.engine.value(sim.market):,.2f}")
    if not portfolio.positions:
        print("No open positions.")
        return
    print("\nSymbol  Shares  Average cost  Market value")
    for symbol, position in portfolio.positions.items():
        value = position.market_value(sim.market.quote(symbol))
        print(f"{symbol:<7} {position.shares:>6}  ₹{position.average_cost:>12.2f}  ₹{value:>12.2f}")

def _read_int(prompt, minimum=1):
    value = int(input(prompt))
    if value < minimum:
        raise ValueError(f"value must be at least {minimum}")
    return value
#Options
def interactive():
    sim = Simulator()
    last_result = None
    while True:
        print("\n" + "=" * 42)
        print("       STOCK PORTFOLIO SIMULATOR")
        print("=" * 42)
        print("1. View market\n2. View portfolio\n3. Buy stock\n4. Sell stock")
        print("5. View transactions\n6. Run market simulation\n7. Analyze portfolio")
        print("8. Compare scenarios\n9. Generate report\n10. Save simulation")
        print("11. Load simulation\n0. Exit")
        choice = input("\nChoose an option: ").strip()
        try:
            if choice == "0":
                print("Goodbye.")
                return
            if choice == "1":
                _show_market(sim)
            elif choice == "2":
                _show_portfolio(sim)
            elif choice in ("3", "4"):
                symbol = input("Stock symbol: ").strip().upper()
                shares = _read_int("Number of shares: ")
                transaction = (sim.engine.buy if choice == "3" else sim.engine.sell)(
                    sim.market, symbol, shares
                )
                print(f"{transaction.side.title()} order completed: {transaction.shares} "
                      f"{transaction.symbol} at ₹{transaction.price:.2f}.")
            elif choice == "5":
                if not sim.engine.portfolio.transactions:
                    print("No transactions recorded.")
                for transaction in sim.engine.portfolio.transactions:
                    print(f"{transaction.timestamp}  {transaction.side:<4} "
                          f"{transaction.shares:>4} {transaction.symbol:<5} "
                          f"₹{transaction.price:>8.2f}")
            elif choice == "6":
                days = _read_int("Simulation days: ")
                last_result = sim.run(days)
                print(f"Advanced to market day {sim.market.day}. "
                      f"Portfolio value: ₹{last_result.equity_curve[-1]:,.2f}")
            elif choice == "7":
                curve = last_result.equity_curve if last_result else [sim.engine.value(sim.market)]
                metrics = Analysis.summary(curve)
                print(text_report(type("Result", (), {"equity_curve": curve,
                                                       "transactions": sim.engine.portfolio.transactions})()))
                print(f"Volatility: {metrics['volatility_pct']:.2f}%")
            elif choice == "8":
                days = _read_int("Days per scenario: ")
                scenarios = {}
                for name, volatility in (("Low", .01), ("Medium", .02), ("High", .05)):
                    scenario = Simulator(seed=sim.market.day + len(name))
                    scenarios[name] = scenario.run(days, volatility=volatility)
                for name, metrics in Analysis.compare(scenarios).items():
                    print(f"{name:<8} final ₹{metrics['final']:>10,.2f}  "
                          f"return {metrics['return_pct']:>7.2f}%  "
                          f"drawdown {metrics['max_drawdown_pct']:>6.2f}%")
            elif choice == "9":
                if last_result is None:
                    last_result = sim.run(0)
                print(text_report(last_result))
            elif choice == "10":
                path = input("Save path [simulation.json]: ").strip() or "simulation.json"
                JsonStore.save(path, sim.market, sim.engine.portfolio)
                print(f"Saved simulation to {Path(path)}.")
            elif choice == "11":
                path = input("Load path [simulation.json]: ").strip() or "simulation.json"
                market, portfolio = JsonStore.load(path)
                sim = Simulator(market=market, portfolio=portfolio)
                last_result = None
                print(f"Loaded simulation from {Path(path)}.")
            else:
                print("Please choose a number from the menu.")
        except (ValueError, ValidationError, OSError, KeyError, TypeError) as error:
            print(f"Unable to complete that action: {error}")
#Optional_matplotlib
def demo(argv=None):
    parser = argparse.ArgumentParser(description="modules stock-market simulator")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--save")
    parser.add_argument("--csv")
    parser.add_argument("--plot")
    args = parser.parse_args(argv)
    sim = Simulator(seed=args.seed)
    result = sim.run(args.days)
    print(text_report(result))
    if args.csv:
        export_equity(args.csv, result.equity_curve)
    if args.plot and not plot_equity(result, args.plot):
        print("Matplotlib unavailable; skipped plot")
    if args.save:
        JsonStore.save(args.save, sim.market, sim.engine.portfolio)
    return result

def main(argv=None):
    if argv is None and len(__import__("sys").argv) == 1:
        return interactive()
    return demo(argv)

if __name__=='__main__':
    main()
