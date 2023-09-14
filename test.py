import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from pystyle import Colors


ticker = input("Enter the stock symbol: ")


stock = yf.Ticker(ticker)
stock_info = stock.info
print(stock_info)



start_date = '2023-01-01'
end_date = '2023-09-01'

df = stock.history(period='1d', start=start_date, end=end_date)
short_term_ma = df['Close'].rolling(window=20).mean()
long_term_ma = df['Close'].rolling(window=50).mean()
if 'longName' in stock_info:
    long_name = stock_info['longName']
    print(f"{Colors.cyan}Long Name: {long_name}")

if 'currentPrice' in stock_info:
    current_price = stock_info['currentPrice']
    print(f"Current Price: {current_price}")

if 'dayHigh' in stock_info:
    day_high = stock_info['dayHigh']
    print(f"Day High: {day_high}")


fig, ax = plt.subplots()


mpf.plot(df, type='candle', ax=ax)

ax.set_title(f'{long_name} Stock Price')
ax.set_xlabel('Date')
ax.set_ylabel('Price')

plt.show()


mpf.plot(df, type='candle', ax=ax)


plt.plot(df.index, short_term_ma, label='20-Day MA', color='orange', alpha=0.7)
plt.plot(df.index, long_term_ma, label='50-Day MA', color='blue', alpha=0.7)


ax.set_xlabel('Date')
ax.set_ylabel('Price')

plt.title(f'{long_name} Stock Price and Moving Averages')
plt.legend()
plt.show()

