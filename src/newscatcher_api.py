from newscatcher import Newscatcher

def get_stock_news(ticker, country='us', max_articles=5):
    nc = Newscatcher(country=country)
    articles = nc.get_news(topic=ticker, max_articles=max_articles)

    news_list = []
    for article in articles['articles']:
        news_list.append({
            'title': article['title'],
            'link': article['link'],
            'published': article['published'],
            'summary': article['summary'],
        })

    return news_list

if __name__ == "__main__":
    stock_ticker = "AAPL"  # Replace with the desired stock symbol
    news_list = get_stock_news(stock_ticker)

    for news in news_list:
        print(f"Title: {news['title']}")
        print(f"Link: {news['link']}")
        print(f"Published: {news['published']}")
        print(f"Summary: {news['summary']}")
        print("\n")

