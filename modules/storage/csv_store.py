import csv
from pathlib import Path
def export_equity(path, equity_curve):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['day','equity']); w.writerows(enumerate(equity_curve))
