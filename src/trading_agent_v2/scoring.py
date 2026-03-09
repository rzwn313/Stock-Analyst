from __future__ import annotations

from dataclasses import dataclass

from .models import StrategySignal


@dataclass(slots=True)
class ScoredSignal:
    signal: StrategySignal
    score: int
    probability: str


class SignalScoringEngine:
    def score(self, signal: StrategySignal) -> ScoredSignal:
        weights = {
            "ema_alignment": 25,
            "candlestick": 20,
            "volume_spike": 20,
            "support_resistance": 20,
            "trend_alignment": 15,
        }

        cond = signal.conditions
        ema_alignment = cond.get("stock_above_50ema", False) or cond.get("price_below_21ema", False)
        candlestick = cond.get("bullish_candle", False) or cond.get("bearish_candle", False)
        support_res = cond.get("near_pd_support", False) or cond.get("near_pd_resistance", False)
        trend = cond.get("market_bullish", False) or cond.get("market_bearish", False)

        score = 0
        score += weights["ema_alignment"] if ema_alignment else 0
        score += weights["candlestick"] if candlestick else 0
        score += weights["volume_spike"] if cond.get("volume_spike", False) else 0
        score += weights["support_resistance"] if support_res else 0
        score += weights["trend_alignment"] if trend else 0

        if score >= 85:
            probability = "Very High"
        elif score >= 70:
            probability = "High"
        elif score >= 55:
            probability = "Medium"
        else:
            probability = "Low"

        return ScoredSignal(signal=signal, score=score, probability=probability)
