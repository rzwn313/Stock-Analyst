from trading_agent_v2.scoring import SignalScoringEngine
from trading_agent_v2.models import StrategySignal


def test_scoring_high_probability():
    signal = StrategySignal(
        symbol="HDFCBANK",
        side="BUY",
        entry=100,
        stop_loss=98,
        target=104,
        conditions={
            "market_bullish": True,
            "stock_above_50ema": True,
            "pullback_21ema": True,
            "bullish_candle": True,
            "near_pd_support": True,
            "volume_spike": True,
        },
    )
    scored = SignalScoringEngine().score(signal)
    assert scored.score >= 70
    assert scored.probability in {"High", "Very High"}
