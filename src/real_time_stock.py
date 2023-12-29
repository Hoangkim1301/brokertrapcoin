import requests
import json

# Replace 'YOUR_API_KEY' with your actual IEX Cloud API key
api_key = 'pk_c5d6f2b09e8a40fcb45ae5a0f58fcbb6'

# List of stock symbols you want to fetch data for
stock_symbols = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA','NVDA','SIE','TSM','AMD']

# Create a def to get api and return the stock price of given stock
# ...

def get_stock_price(symbol):
    # Contact API.
    try:
        #api_key = os.environ.get("API_KEY")
        #response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}")
        #response.raise_for_status()       
        endpoint = f'https://cloud.iexapis.com/stable/stock/{symbol}/quote?token={api_key}'
        
        # Sending a GET request to the endpoint
        response = requests.get(endpoint)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            stock_data = response.json()
            latest_price = stock_data.get('latestPrice')
            stock_info = {
                'name': stock_data.get('companyName'),
                'symbol': stock_data.get('symbol'),
                'latest_price': stock_data.get('latestPrice')
            }
            return print(stock_info)
    except requests.RequestException:
        return None
    except (KeyError, TypeError, ValueError):
        return None

#main
if __name__ == '__main__':
    get_stock_price('AAPL')