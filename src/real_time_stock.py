import requests

# Replace 'YOUR_API_KEY' with your actual IEX Cloud API key
api_key = 'pk_c5d6f2b09e8a40fcb45ae5a0f58fcbb6'

# List of stock symbols you want to fetch data for
stock_symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA','NVDA','SIE','TSM','AMD']

for symbol in stock_symbols:
    # Endpoint to fetch real-time stock price for a specific stock symbol
    endpoint = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}'

    # Sending a GET request to the endpoint
    response = requests.get(endpoint)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        stock_data = response.json()
        latest_price = stock_data.get('latestPrice')
        print(f"Latest price for {symbol}: ${latest_price}")
    else:
        print(f"Failed to fetch data for {symbol}. Status code:", response.status_code)
