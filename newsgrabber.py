import yfinance as yf

# Create a Ticker object for the stock or index you're interested in (e.g., Apple Inc. with ticker symbol AAPL)
ticker_symbol = input("ENTER THE TICKER: ")
ticker = yf.Ticker(ticker_symbol)

# Fetch news articles
news_data = ticker.news
print(news_data)
# Print the headlines and URLs of the news articles
for item in news_data:
    title = item['title']
    publisher = item['publisher']
    link = item['link']
    provider_publish_time = item['providerPublishTime']

    # Print or process the extracted information as needed
    print("Title:", title)
    print("Publisher:", publisher)
    print("Link:", link)
    print("Provider Publish Time:", provider_publish_time)
    print("\n")