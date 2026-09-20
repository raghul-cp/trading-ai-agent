import yfinance as yf
import pandas as pd


def trading_signal(symbol):
    data = yf.download(
        symbol,
        period="3mo",
        interval="1d",
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        return "NO DATA"

    close = data["Close"].squeeze()

    # Moving averages
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    current_price = float(close.iloc[-1])
    current_ma20 = float(ma20.iloc[-1])
    current_ma50 = float(ma50.iloc[-1])

    if current_ma20 > current_ma50:
        signal = "BUY"
    elif current_ma20 < current_ma50:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "Symbol": symbol,
        "Price": round(current_price, 2),
        "MA20": round(current_ma20, 2),
        "MA50": round(current_ma50, 2),
        "Signal": signal
    }


if __name__ == "__main__":
    symbol = input("Enter stock symbol (example: RELIANCE.NS): ")
    result = trading_signal(symbol)

    print("\n===== TRADING AI AGENT =====")
    print(result)
    print("============================")