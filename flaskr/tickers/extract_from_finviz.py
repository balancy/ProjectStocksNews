import pandas as pd
import requests
from config import FINVIZ_URL_BASE, FINVIZ_URL_GROUP, FINVIZ_HEADERS


def get_dict_from_df(df):
    """Transforming finviz dataframe to dictionary
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


def get_pe_and_dividend(division_type, division_value):
    """
    :param division_type: 'sector' or 'country'
    :param division_value: sector or country
    :return: demanded P/E and Dividend yield
    """

    link = f"{FINVIZ_URL_GROUP}{division_type}&v=110"
    request = requests.get(link, headers=FINVIZ_HEADERS)

    df = pd.read_html(request.text)[4]

    idx_value = df.index[df[1] == division_value][0]
    pe = df[5][idx_value]
    div = df[4][idx_value][:-1]
    return float(pe), float(div)


def add_pe_div_to_dict(dictionary, sector, country):
    """Adding P/E et Dividend yield for sector and country to the
    resulting dictionary
    """

    # fundamentals of the sector and country
    pe_sector, div_sector = get_pe_and_dividend('sector', sector)
    pe_country, div_country = get_pe_and_dividend('country', country)

    # adding them to dictionary
    dictionary['pe_sector'] = pe_sector
    dictionary['pe_country'] = pe_country
    dictionary['div_sector'] = div_sector
    dictionary['div_country'] = div_country


def get_finviz_fundamentals(ticker):
    """Getting fundamentals from finviz site
    """

    request = requests.get(FINVIZ_URL_BASE + ticker, headers=FINVIZ_HEADERS)
    df = pd.read_html(request.text)

    # useful info
    useful_info = df[4][0][2].split('|')
    sector = useful_info[0].strip()
    country = useful_info[2].strip()

    # main fundamentals table from site
    finviz_fundamentals = df[5]

    # transforming dataframe to dictionary
    dict_finviz = get_dict_from_df(finviz_fundamentals)
    dict_finviz['sector'] = sector
    add_pe_div_to_dict(dict_finviz, sector, country)

    return dict_finviz
