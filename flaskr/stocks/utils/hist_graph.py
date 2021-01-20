from datetime import datetime, timedelta
from pandas_datareader import data as web
import pathlib
import plotly.graph_objects as go
from config import CHART_FILEPATH, CHART_FILENAME

YEARS_AGO = 3
DAYS_IN_YEAR = 365


def get_stocks_df(ticker):
    """
    Reading price data for stocks ticker.
    :param ticker: ticker we are searching for
    :return: data
    """

    three_years_ago = datetime.now() - timedelta(days=YEARS_AGO*DAYS_IN_YEAR)
    df = web.DataReader(ticker, data_source='yahoo', start=three_years_ago)
    return df


def exists(path):
    """
    Verifies if chart on this date exists already.
    :param path - path to the filename
    :return: does this chart exist or not
    """

    fname = pathlib.Path(f"{path}")
    if fname.exists():
        file_mtime = datetime.fromtimestamp(fname.stat().st_mtime)
        if file_mtime.day == datetime.now().day:
            return True
    return False


def create_graph(ticker):
    """
    Creating history price chart of stocks ticker
    :param ticker: ticker we are searching for
    :return: path to the graph
    """

    graph_name = f"{CHART_FILEPATH}{ticker}{CHART_FILENAME}"
    if not exists(graph_name):
        df = get_stocks_df(ticker)
        trace1 = {'x': df.index, 'open': df.Open, 'close': df.Close, 'high': df.High, 'low': df.Low,
                  'type': 'candlestick', 'name': f'{ticker}]'}

        fig = go.Figure(data=[trace1])
        fig.write_image(graph_name)

    return graph_name


if __name__ == '__main__':
    create_graph('FB')
