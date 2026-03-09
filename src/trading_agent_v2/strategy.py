from __future__ import annotations

import pandas as pd

from .indicators import add_ema, add_volume_spike_flag
from .patterns import is_bearish_engulfing, is_bullish_engulfing, red_to_green_reversal


from .models import StrategySignal


class StrategyEngine:
    def evaluate(
        self,
        symbol: str,
        stock_df: pd.DataFrame,
        index_df: pd.DataFrame,
        prev_day_high: float,
        prev_day_low: float,
    ) -> StrategySignal | None:
        if len(stock_df) < 60 or len(index_df) < 60:
            return None

        stock = stock_df.copy()
        idx = index_df.copy()
        stock["ema21"] = add_ema(stock, 21)
        stock["ema50"] = add_ema(stock, 50)
        stock["volume_spike"] = add_volume_spike_flag(stock)
        idx["ema50"] = add_ema(idx, 50)

        c = stock.iloc[-1]
        market_bullish = idx.iloc[-1]["close"] > idx.iloc[-1]["ema50"]
        market_bearish = idx.iloc[-1]["close"] < idx.iloc[-1]["ema50"]
        near_pd_low = abs(c["close"] - prev_day_low) / max(prev_day_low, 1e-9) <= 0.007
        near_pd_high = abs(c["close"] - prev_day_high) / max(prev_day_high, 1e-9) <= 0.007

        buy_conditions = {
            "market_bullish": market_bullish,
            "stock_above_50ema": c["close"] > c["ema50"],
            "pullback_21ema": c["low"] <= c["ema21"] <= c["high"],
            "bullish_candle": is_bullish_engulfing(stock) or red_to_green_reversal(stock),
            "near_pd_support": near_pd_low,
            "volume_spike": bool(c["volume_spike"]),
        }

        if all(buy_conditions.values()):
            entry = float(c["close"])
            stop = float(min(c["low"], c["ema21"]))
            risk = entry - stop
            return StrategySignal(
                symbol=symbol,
                side="BUY",
                entry=entry,
                stop_loss=stop,
                target=entry + (2.0 * risk),
                conditions=buy_conditions,
            )

        sell_conditions = {
            "market_bearish": market_bearish,
            "price_below_21ema": c["close"] < c["ema21"],
            "bearish_candle": is_bearish_engulfing(stock),
            "near_pd_resistance": near_pd_high,
            "volume_spike": bool(c["volume_spike"]),
        }

        if all(sell_conditions.values()):
            entry = float(c["close"])
            stop = float(max(c["high"], c["ema21"]))
            risk = stop - entry
            return StrategySignal(
                symbol=symbol,
                side="SELL",
                entry=entry,
                stop_loss=stop,
                target=entry - (2.0 * risk),
                conditions=sell_conditions,
            )

        return None
