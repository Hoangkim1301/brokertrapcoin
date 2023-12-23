class StockList:
    def __init__(self):
        self.stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA','NVDA','SIE.DE','TSM','AMD']

    def add_stock(self, stock):
        if stock not in self.stocks:
            self.stocks.append(stock)

    def remove_stock(self, stock):
        if stock in self.stocks:
            self.stocks.remove(stock)

    def display_stocks(self):
        for stock in self.stocks:
            print(stock)
            
    def get_stock_list(self):
        return self.stocks
        