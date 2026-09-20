import yfinance as yf


SYMBOL = "RELIANCE.NS"
INITIAL_CAPITAL = 100000


data = yf.download(
    SYMBOL,
    period="6mo",
    interval="1d",
    auto_adjust=True,
    progress=False
)

close = data["Close"].squeeze()

ma20 = close.rolling(20).mean()
ma50 = close.rolling(50).mean()

delta = close.diff()
gain = delta.clip(lower=0)
loss = -delta.clip(upper=0)

avg_gain = gain.rolling(14).mean()
avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

ema12 = close.ewm(span=12, adjust=False).mean()
ema26 = close.ewm(span=26, adjust=False).mean()

macd = ema12 - ema26
macd_signal = macd.ewm(span=9, adjust=False).mean()


cash = INITIAL_CAPITAL
shares = 0
entry_price = 0
trades = 0


for i in range(50, len(close)):

    price = float(close.iloc[i])

    score = 0

    if float(ma20.iloc[i]) > float(ma50.iloc[i]):
        score += 1
    else:
        score -= 1

    if float(rsi.iloc[i]) < 30:
        score += 1
    elif float(rsi.iloc[i]) > 70:
        score -= 1

    if float(macd.iloc[i]) > float(macd_signal.iloc[i]):
        score += 1
    else:
        score -= 1

    # BUY
    if score >= 2 and shares == 0:
        shares = int(cash / price)

        if shares > 0:
            cash -= shares * price
            entry_price = price
            trades += 1

    # SELL
    elif score <= -2 and shares > 0:
        cash += shares * price
        shares = 0
        trades += 1


# Close open position at final price
final_price = float(close.iloc[-1])

if shares > 0:
    cash += shares * final_price
    shares = 0

profit = cash - INITIAL_CAPITAL
return_percent = (profit / INITIAL_CAPITAL) * 100


print("\n===== TRADING AI BACKTEST =====")
print(f"Symbol: {SYMBOL}")
print(f"Initial Capital: ₹{INITIAL_CAPITAL:,.2f}")
print(f"Final Capital: ₹{cash:,.2f}")
print(f"Profit/Loss: ₹{profit:,.2f}")
print(f"Return: {return_percent:.2f}%")
print(f"Trades: {trades}")
print("===============================")