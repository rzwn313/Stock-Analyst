from .config import RuntimeConfig
from .data_provider import MockMarketDataProvider
from .scanner import MarketScanner
from .scoring import SignalScoringEngine
from .strategy import StrategyEngine


def main() -> None:
    config = RuntimeConfig.from_env()
    scanner = MarketScanner(
        config=config,
        data_provider=MockMarketDataProvider(),
        strategy=StrategyEngine(),
        scorer=SignalScoringEngine(),
    )
    scanner.run_forever()


if __name__ == "__main__":
    main()
