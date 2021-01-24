class StockNotFoundException(Exception):
    """
    Exception raised for errors in the reading ticker from finviz.

    Attributes:
        ticker - ticker that cannot be found on finviz
        message - explanation of the error
    """

    def __init__(self, ticker):
        self.ticker = ticker
        self.message = f"There is stock {self.ticker} on Finviz"
        super().__init__(self.message)