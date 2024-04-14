# TAMU Hackathon Stocks Website

Welcome to the TAMU Hackathon Stocks Website, a powerful Flask-based application designed for tracking and analyzing stock data. This site uses the Yahoo Finance API to fetch real-time stock information and provide detailed insights into market trends.

## Features

- **Real-Time Stock Data:** Utilizes `yfinance` to fetch the latest stock information.
- **Stock Price Visualization:** Generates candlestick charts and moving averages using `matplotlib` and `mplfinance`.
- **Sentiment Analysis:** Analyzes news headlines related to stocks using the `vaderSentiment` library to gauge market sentiment.
- **Performance Metrics:** Calculates PE ratios and stock valuations based on current earnings data.

## How It Works

1. **Fetching Data:** Users input a stock ticker symbol, and the application retrieves data such as current price, daily high/low, and 52-week metrics.
2. **Chart Generation:** The application plots candlestick charts and moving averages for specified time frames (daily, weekly, monthly).
3. **Sentiment Analysis:** News headlines are analyzed for sentiment, helping users understand the market's emotional response to recent events.
