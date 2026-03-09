from dataclasses import dataclass


@dataclass(slots=True)
class StrategySignal:
    symbol: str
    side: str
    entry: float
    stop_loss: float
    target: float
    conditions: dict[str, bool]
