import json
from pathlib import Path
from modules.market import Market
from modules.models import Portfolio
class JsonStore:
    @staticmethod
    def save(path, market, portfolio):
        Path(path).write_text(json.dumps({'market':market.to_dict(),'portfolio':portfolio.to_dict()}, indent=2), encoding='utf-8')
    @staticmethod
    def load(path):
        data=json.loads(Path(path).read_text(encoding='utf-8')); return Market.from_dict(data['market']),Portfolio.from_dict(data['portfolio'])
