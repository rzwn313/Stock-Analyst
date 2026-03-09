from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import logging
import time

from .alerting import TelegramAlerter
from .charting import save_signal_chart
from .config import RuntimeConfig
from .data_provider import MarketDataProvider
from .scoring import SignalScoringEngine
from .strategy import StrategyEngine


logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")


@dataclass(slots=True)
class MarketScanner:
    config: RuntimeConfig
    data_provider: MarketDataProvider
    strategy: StrategyEngine
    scorer: SignalScoringEngine

    def run_forever(self) -> None:
        alerter = TelegramAlerter(self.config.telegram) if self.config.telegram else None
        logging.info("Scanner started for %s symbols", len(self.config.scanner.symbols))

        while True:
            started = datetime.utcnow()
            try:
                self.scan_once(alerter=alerter)
            except Exception as exc:  # noqa: BLE001
                logging.exception("Scan cycle failed: %s", exc)

            elapsed = (datetime.utcnow() - started).total_seconds()
            sleep_for = max(0, self.config.scanner.scan_interval_seconds - elapsed)
            time.sleep(sleep_for)

    def scan_once(self, alerter: TelegramAlerter | None = None) -> list[tuple[str, int]]:
        results: list[tuple[str, int]] = []
        index_df = self.data_provider.fetch_ohlcv(
            self.config.scanner.index_symbol,
            self.config.scanner.candle_interval,
            self.config.scanner.lookback_bars,
        )

        for symbol in self.config.scanner.symbols:
            stock_df = self.data_provider.fetch_ohlcv(
                symbol,
                self.config.scanner.candle_interval,
                self.config.scanner.lookback_bars,
            )
            prev_day_high = float(stock_df.iloc[-2]["high"])
            prev_day_low = float(stock_df.iloc[-2]["low"])
            signal = self.strategy.evaluate(symbol, stock_df, index_df, prev_day_high, prev_day_low)
            if not signal:
                continue

            scored = self.scorer.score(signal)
            if scored.score < self.config.scanner.score_threshold:
                continue

            results.append((symbol, scored.score))
            logging.info("Signal %s score=%s side=%s", symbol, scored.score, scored.signal.side)
            chart_path = save_signal_chart(symbol, stock_df)
            if alerter:
                alerter.send(scored, chart_path=chart_path)

        return sorted(results, key=lambda x: x[1], reverse=True)
