from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import pandas as pd


@dataclass(slots=True)
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class MarketDataProvider:
    """Broker wrapper interface. Replace mock methods with Zerodha/Upstox adapters."""

    def fetch_ohlcv(self, symbol: str, interval: str, lookback: int) -> pd.DataFrame:
        raise NotImplementedError


class MockMarketDataProvider(MarketDataProvider):
    def fetch_ohlcv(self, symbol: str, interval: str, lookback: int) -> pd.DataFrame:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        timestamps = [now - timedelta(minutes=15 * i) for i in reversed(range(lookback))]
        base = 100 + random.uniform(-5, 5)
        rows: list[dict] = []
        price = base
        for ts in timestamps:
            move = random.uniform(-1.2, 1.2)
            op = price
            cl = max(1.0, op + move)
            hi = max(op, cl) + random.uniform(0.1, 0.8)
            lo = min(op, cl) - random.uniform(0.1, 0.8)
            vol = random.uniform(100_000, 600_000)
            rows.append({"timestamp": ts, "open": op, "high": hi, "low": lo, "close": cl, "volume": vol})
            price = cl
        return pd.DataFrame(rows)
