# Stock Analyst - Version 2 Intraday Scanner

This repository now contains a production-ready architecture scaffold for an **AI intraday scanner focused on Nifty 100**.

## What it does

- Scans configured symbols continuously (default every 15 seconds).
- Uses 15-minute candle data.
- Evaluates strategy conditions (EMA pullback + candlestick + PDH/PDL + volume + market trend).
- Scores each setup and keeps only high-probability alerts.
- Sends Telegram alerts with optional chart snapshot.

## Architecture

1. `MarketDataProvider`: adapter interface for Upstox/Zerodha/AngelOne.
2. `StrategyEngine`: BUY/SELL condition validation.
3. `SignalScoringEngine`: weighted score out of 100.
4. `MarketScanner`: loop runner and ranking.
5. `TelegramAlerter` + `save_signal_chart`: outbound notifications.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

Run scanner:

```bash
export SYMBOLS="HDFCBANK,ICICIBANK,RELIANCE,TATASTEEL"
export INDEX_SYMBOL="NIFTY50"
export SCORE_THRESHOLD="70"
# Optional Telegram
# export TELEGRAM_BOT_TOKEN="..."
# export TELEGRAM_CHAT_ID="..."
python -m trading_agent_v2.main
```

## Notes

- `MockMarketDataProvider` is included for local development.
- Replace `fetch_ohlcv` with broker API integration for live trading.
- Suggested deployment: AWS EC2 / DigitalOcean / Railway / Render.
