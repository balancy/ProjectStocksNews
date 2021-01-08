import pandas as pd
import requests
from config import FINVIZ_URL_BASE, FINVIZ_HEADERS


def get_dict_from_df(df):
    """Transforming dataframe to dictionary
    """

    attributes = list()
    values = list()

    for key, value in df.to_dict().items():
        if not key % 2:
            attributes += value.values()
        else:
            values += value.values()
    dict_finviz = dict(zip(attributes, values))

    return dict_finviz


def get_finviz_fundamentals(ticker):

    request = requests.get(FINVIZ_URL_BASE + ticker, headers=FINVIZ_HEADERS)
    df = pd.read_html(request.text)

    # sector
    sector = df[4][0][2].split('|')[0].rstrip()

    # dataframe transforming to dict
    finviz_fundamentals = df[5]

    # getting dictionary
    dict_finviz = get_dict_from_df(finviz_fundamentals)
    dict_finviz['sector'] = sector

    return dict_finviz
