import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime
from stock_list import StockList

def real_time_price(stock_code):
    # Calculate the start date as one month ago from today
    start_date = datetime.datetime.now() - datetime.timedelta(days=93)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    print('end_date:', end_date)
    # Download the data for the specified period
    data = yf.download(tickers=stock_code, start=start_date, end=end_date, interval='1d', auto_adjust=True)
    print('data:', stock_code)
    print(data)
    
    # Get the latest price
    price = data['Close'].iloc[-1]
    

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
        #st.write(f'The latest price for {stock_code} is {price}')
    
    
    
        
   






