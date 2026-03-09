from __future__ import annotations

import pandas as pd


def add_ema(df: pd.DataFrame, period: int, source_col: str = "close") -> pd.Series:
    return df[source_col].ewm(span=period, adjust=False).mean()


def add_volume_spike_flag(df: pd.DataFrame, window: int = 20, multiplier: float = 1.5) -> pd.Series:
    avg_volume = df["volume"].rolling(window=window, min_periods=window).mean()
    return df["volume"] > (avg_volume * multiplier)
