import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from pystyle import Colors

def calculate_pe_ratio(price_per_share, earnings_per_share):
    try:
        pe_ratio = price_per_share / earnings_per_share
        return pe_ratio
    except ZeroDivisionError:
        return None

def determine_valuation(pe_ratio, industry_average_pe_ratio):
    if pe_ratio is None:
        return "Cannot determine valuation due to zero earnings per share"
    
    if pe_ratio < industry_average_pe_ratio:
        return "Undervalued"
    elif pe_ratio > industry_average_pe_ratio:
        return "Overvalued"
    else:
        return "Fairly valued"

def doStockCalc(price_per_share, earnings_per_share, industry_average_pe_ratio):
    try:
     

        pe_ratio = calculate_pe_ratio(price_per_share, earnings_per_share)
        valuation = determine_valuation(pe_ratio, industry_average_pe_ratio)

        if pe_ratio is not None:
            return valuation
        else:
            print("Cannot determine valuation due to zero earnings per share.")
    
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")



#code



ticker = input("Enter the stock symbol: ")

stock = yf.Ticker(ticker)
stock_info = stock.info
print(stock_info)

start_date = '2023-01-01'
end_date = '2023-09-01'

df = stock.history(period='1d', start=start_date, end=end_date)
df['PriceChange'] = df['Close'].diff()
short_term_ma = df['Close'].rolling(window=20).mean()
long_term_ma = df['Close'].rolling(window=50).mean()


colors = ['g' if price_change >= 0 else 'r' for price_change in df['PriceChange']]

if 'longName' in stock_info:
    long_name = stock_info['longName']
    print(f"{Colors.cyan}Long Name: {long_name}")

if 'currentPrice' in stock_info:
    current_price = stock_info['currentPrice']
    print(f"Current Price: {current_price}")

if 'dayHigh' in stock_info:
    day_high = stock_info['dayHigh']
    print(f"Day High: {day_high}")
if 'trailingEps' in stock_info:
    trailing_eps = stock_info['trailingEps']
    print(f"Trailing Eps: {trailing_eps}")

print(f'The stock is {doStockCalc(current_price, trailing_eps, calculate_pe_ratio(current_price, trailing_eps))}.')

market_colors = {
    'candle': {
        'up': 'g',
        'down': 'r',
    },
    'edge': {
        'up': 'k',
        'down': 'k',
    },
    'wick': {
        'up': 'k',
        'down': 'k',
    },
    'ohlc': {
        'up': 'k',
        'down': 'k',
    },
    'volume': {
        'up': '#1f77b4',
        'down': '#1f77b4',
    },
    'vcedge': {
        'up': '#1f77b4',
        'down': '#1f77b4',
    },
    'alpha': 1.0,  
}



s = mpf.make_mpf_style(marketcolors=market_colors)
mpf.plot(df, type='candle', style=s, title=f'{long_name} Stock Price', ylabel='Price', volume=False)

plt.show()


#Graph 2
fig, ax = plt.subplots()
mpf.plot(df, type='candle', ax=ax)


plt.plot(df.index, short_term_ma, label='20-Day MA', color='orange', alpha=0.7)
plt.plot(df.index, long_term_ma, label='50-Day MA', color='blue', alpha=0.7)


ax.set_xlabel('Date')
ax.set_ylabel('Price')

plt.title(f'{long_name} Stock Price and Moving Averages')
plt.legend()
plt.show()





