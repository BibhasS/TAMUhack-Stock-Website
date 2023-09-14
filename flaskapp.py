from flask import Flask, render_template, request
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
from time import sleep
from pystyle import Colors
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import datetime


app = Flask(__name__)

df = None
ticker = ""
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    global ticker
    input_data = request.form['input_data']
    ticker = input_data
    try:
     calcstock(ticker)
     return render_template('stocks.html')
     
    except Exception as e:
        return f'Error: {e}'

    





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



def calcstock(ticker):
    global df
    stock = yf.Ticker(ticker)
    stock_info = stock.info
    
    print(stock_info)
    if 'longName' in stock_info:
        long_name = stock_info['longName']
        print(f"{Colors.cyan}Long Name: {long_name}")
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
    
    
    def stockImageGen(end_date, start_date, daysbefore, period, long_name, market_colors):
        

        try:
            df = stock.history(period=period, start=start_date, end=end_date)
            df['PriceChange'] = df['Close'].diff()
            colors = ['g' if price_change >= 0 else 'r' for price_change in df['PriceChange']]
            plt.switch_backend('agg') 
            s = mpf.make_mpf_style(marketcolors=market_colors)
            mpf.plot(df, type='candle', style=s, title=f'{long_name} Stock Price', ylabel='Price', volume=False)
            plt.savefig(f'static/images/stockimage_{daysbefore}.png') 
            plt.close()
        
            print("Candlestick chart saved successfully.")
   
        
        except Exception as e:
             print(f'Error {e}')
             return f'Error: {e}'
             
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    end_date = formatted_date
    
    start_date = current_datetime - datetime.timedelta(days=365)
    formatted_date = start_date.strftime("%Y-%m-%d")
    start_date = formatted_date
    df = stock.history(period='1d', start=start_date, end=end_date)

    stockImageGen(end_date, (current_datetime - datetime.timedelta(days=365)).strftime("%Y-%m-%d"), '1y', '1d', long_name, market_colors)
    stockImageGen(end_date, (current_datetime - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), '1w', '1h', long_name, market_colors)
    stockImageGen(end_date, (current_datetime - datetime.timedelta(days=30)).strftime("%Y-%m-%d"), '1m', '1h', long_name, market_colors)
    stockImageGen(end_date, (current_datetime - datetime.timedelta(days=1)).strftime("%Y-%m-%d"), '1d', '20m', long_name, market_colors)
    



    short_term_ma = df['Close'].rolling(window=20).mean()
    long_term_ma = df['Close'].rolling(window=50).mean()


    


    long_name = ''
    current_price = ''
    day_high = ''
    trailing_eps = ''
    fiftyTwoWeekHigh = ''
    fiftyTwoWeekLow = ''
    dayLow = ''
    previousClose = ''



    if 'currentPrice' in stock_info:
        current_price = stock_info['currentPrice']
        print(f"Current Price: {current_price}")

    if 'dayHigh' in stock_info:
        day_high = stock_info['dayHigh']
        print(f"Day High: {day_high}")
    if 'trailingEps' in stock_info:
        trailing_eps = stock_info['trailingEps']
        print(f"Trailing Eps: {trailing_eps}")
    if 'fiftyTwoWeekHigh' in stock_info:
        fiftyTwoWeekHigh = stock_info['fiftyTwoWeekHigh']
        print(f"fiftyTwoWeekHigh: {fiftyTwoWeekHigh}")
    
    if 'fiftyTwoWeekLow' in stock_info:
        fiftyTwoWeekLow = stock_info['fiftyTwoWeekLow']
        print(f"fiftyTwoWeekLow: {fiftyTwoWeekLow}")

    if 'dayLow' in stock_info:
        dayLow = stock_info['dayLow']
        print(f"Day Low: {dayLow}")
    if 'previousClose' in stock_info:
        previousClose = stock_info['previousClose']
        print(f"previous Close: {previousClose}")
    if 'longName' in stock_info:
        long_name = stock_info['longName']
        print(f"{Colors.cyan}Long Name: {long_name}")
    valuation = doStockCalc(current_price, trailing_eps, calculate_pe_ratio(current_price, trailing_eps))
    print(f'The stock is {valuation}.')




    
    
    #Graph 2

    
    plt.clf()
    plt.plot(df.index, short_term_ma, label='20-Day MA', color='orange', alpha=0.7)
    plt.plot(df.index, long_term_ma, label='50-Day MA', color='blue', alpha=0.7)



    plt.title(f'{long_name} Stock Price and Moving Averages')

    plt.savefig('static/images/movingaverage.png', dpi=100) 

    with open('values.txt', 'w') as file:
        info = f"Name: {long_name}\nCurrentPrice: {current_price}\nStockValuation: {valuation}\nDayHigh: {day_high}\nDayLow: {dayLow}\nPreviousClose: {previousClose}\nFiftyTwoWeekHigh: {fiftyTwoWeekHigh}\nFiftyTwoWeekLow: {fiftyTwoWeekLow}"
        file.write(info)


    analyzer = SentimentIntensityAnalyzer()
    news = stock.news 

    scores = []
    for item in news:
        text = item['title']
        sentiment = analyzer.polarity_scores(text)
        compound_sentiment = sentiment['compound']
        website_name = item['link']  
        scores.append((text, website_name, compound_sentiment))

    
    df = pd.DataFrame(scores, columns=['article_title', 'website_name', 'sentiment_rating'])
    file_path = 'sentiment_analysis.csv'
    if os.path.exists(file_path):
     os.remove(file_path)
    df.to_csv('sentiment_analysis.csv', index=False)


   


if __name__ == '__main__':
     app.run(debug=True)


