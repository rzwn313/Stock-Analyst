from __future__ import annotations

from pathlib import Path
import requests

from .config import TelegramConfig
from .scoring import ScoredSignal


class TelegramAlerter:
    def __init__(self, config: TelegramConfig):
        self.config = config

    def send(self, scored: ScoredSignal, chart_path: Path | None = None) -> None:
        s = scored.signal
        true_conditions = [k for k, v in s.conditions.items() if v]
        condition_lines = "\n".join([f"✔ {c}" for c in true_conditions])
        msg = (
            "AI Trading Agent Alert\n\n"
            f"Stock: {s.symbol}\n"
            f"Setup: {s.side}\n"
            f"Score: {scored.score}\n"
            f"Probability: {scored.probability}\n\n"
            f"Conditions:\n{condition_lines}\n\n"
            f"Entry: {s.entry:.2f}\n"
            f"Stop Loss: {s.stop_loss:.2f}\n"
            f"Target: {s.target:.2f}"
        )

        requests.post(
            f"https://api.telegram.org/bot{self.config.bot_token}/sendMessage",
            json={"chat_id": self.config.chat_id, "text": msg},
            timeout=10,
        ).raise_for_status()

        if chart_path and chart_path.exists():
            with chart_path.open("rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{self.config.bot_token}/sendPhoto",
                    data={"chat_id": self.config.chat_id},
                    files={"photo": f},
                    timeout=20,
                ).raise_for_status()
