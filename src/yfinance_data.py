import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from stock_list import StockList
from datetime import datetime, timedelta

def real_time_price(stock_code):
    # Calculate the start date as one month ago from today
    start_date = datetime.now() - timedelta(days=7)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    print('end_date:', end_date)
    # Download the data for the specified period
    try:
        
        data = yf.download(tickers=stock_code, start=start_date, end=end_date, interval='1d', auto_adjust=True)
        print('data:', stock_code)
        #print(data)
    
    except Exception as e:
        print(f'Failed to fetch data {e}')
        return None
    # Get the latest price
    price = data['Close'].iloc[-1]
    return round(price,2)
    
def create_price_chart(symbol,df):
    light_palette = {}
    light_palette["bg_color"] = "#ffffff"
    light_palette["plot_bg_color"] = "#ffffff"
    light_palette["grid_color"] = "#e6e6e6"
    light_palette["text_color"] = "#2e2e2e"
    light_palette["dark_candle"] = "#4d98c4"
    light_palette["light_candle"] = "#b1b7ba"
    light_palette["chop_color"] = "#c74e96"
    light_palette["border_color"] = "#2e2e2e"
    light_palette["color_1"] = "#5c285b"
    light_palette["color_2"] = "#802c62"
    light_palette["color_3"] = "#a33262"
    light_palette["color_4"] = "#c43d5c"
    light_palette["color_5"] = "#de4f51"
    light_palette["color_6"] = "#f26841"
    light_palette["color_7"] = "#fd862b"
    light_palette["color_8"] = "#ffa600"
    light_palette["color_9"] = "#3366d6"
    palette = light_palette
    
    

#main
if __name__ == '__main__':
    # Create an instance of the StockList class
    stock_list = StockList()

    # Get the stock list from the StockList class
    stock_list_data = stock_list.get_stock_list()

    # Set up the Streamlit app
    #st.title('Real time stock prices')

    # Iterate over the stock list
    for stock_code in stock_list_data:
        price = real_time_price(stock_code)
        print('price:', price)
    
    
    
        
   






