import yfinance as yf


def trading_signal(symbol):
    data = yf.download(
        symbol,
        period="6mo",
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

    # RSI
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal_line = macd.ewm(span=9, adjust=False).mean()

    # Latest values
    price = float(close.iloc[-1])
    ma20_value = float(ma20.iloc[-1])
    ma50_value = float(ma50.iloc[-1])
    rsi_value = float(rsi.iloc[-1])
    macd_value = float(macd.iloc[-1])
    signal_value = float(signal_line.iloc[-1])

    # Scoring system
    score = 0

    if ma20_value > ma50_value:
        score += 1
    else:
        score -= 1

    if rsi_value < 30:
        score += 1
    elif rsi_value > 70:
        score -= 1

    if macd_value > signal_value:
        score += 1
    else:
        score -= 1

    if score >= 2:
        signal = "BUY"
    elif score <= -2:
        signal = "SELL"
    else:
        signal = "HOLD"

    return {
        "Symbol": symbol,
        "Price": round(price, 2),
        "MA20": round(ma20_value, 2),
        "MA50": round(ma50_value, 2),
        "RSI": round(rsi_value, 2),
        "MACD": round(macd_value, 2),
        "MACD Signal": round(signal_value, 2),
        "Score": score,
        "Signal": signal
    }


if __name__ == "__main__":
    symbol = input("Enter stock symbol (example: RELIANCE.NS): ")

    result = trading_signal(symbol)

    print("\n===== TRADING AI AGENT =====")

    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)

    print("============================")