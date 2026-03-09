from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def save_signal_chart(symbol: str, df: pd.DataFrame, output_dir: str = "artifacts") -> Path:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    out = Path(output_dir) / f"{symbol}_signal.png"

    view = df.tail(60)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(view["timestamp"], view["close"], label="Close")
    ax.plot(view["timestamp"], view["close"].ewm(span=21, adjust=False).mean(), label="EMA21")
    ax.plot(view["timestamp"], view["close"].ewm(span=50, adjust=False).mean(), label="EMA50")
    ax.set_title(f"{symbol} - 15m setup")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)
    return out
