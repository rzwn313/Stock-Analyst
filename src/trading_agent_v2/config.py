from dataclasses import dataclass, field
import os


@dataclass(slots=True)
class ScannerConfig:
    symbols: list[str] = field(default_factory=list)
    index_symbol: str = "NIFTY50"
    scan_interval_seconds: int = 15
    candle_interval: str = "15minute"
    score_threshold: int = 70
    lookback_bars: int = 120


@dataclass(slots=True)
class TelegramConfig:
    bot_token: str
    chat_id: str


@dataclass(slots=True)
class RuntimeConfig:
    scanner: ScannerConfig
    telegram: TelegramConfig | None = None

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        symbols_raw = os.getenv("SYMBOLS", "")
        symbols = [s.strip().upper() for s in symbols_raw.split(",") if s.strip()]
        scanner = ScannerConfig(
            symbols=symbols,
            index_symbol=os.getenv("INDEX_SYMBOL", "NIFTY50"),
            scan_interval_seconds=int(os.getenv("SCAN_INTERVAL_SECONDS", "15")),
            candle_interval=os.getenv("CANDLE_INTERVAL", "15minute"),
            score_threshold=int(os.getenv("SCORE_THRESHOLD", "70")),
            lookback_bars=int(os.getenv("LOOKBACK_BARS", "120")),
        )

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        telegram = TelegramConfig(bot_token=token, chat_id=chat_id) if token and chat_id else None
        return cls(scanner=scanner, telegram=telegram)
