import pandas as pd
import requests
from config import FINVIZ_URL_BASE, FINVIZ_URL_GROUP, FINVIZ_HEADERS


def get_dict_from_df(df):
    """
    Transforming dataframe to dictionary
    :param df: dataframe
    :return: dictionary
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


def get_finviz_info(ticker):
    """
    Getting the header of the finviz site.
    :param ticker: stocks ticker to search for on the site.
    :return: site header dataframe
    """

    request = requests.get(f"{FINVIZ_URL_BASE}{ticker}", headers=FINVIZ_HEADERS)
    if request.status_code == 404:
        raise NameError

    df = pd.read_html(request.text)

    return df


def get_finviz_fundamentals(ticker):
    """
    Getting fundamentals from finviz site.
    :param ticker: ticker to search for on the site
    :return: fundamentals in the form of dictionary
    """

    df = get_finviz_info(ticker)

    # main fundamentals table from site
    finviz_fundamentals = df[5]

    # transforming dataframe to dictionary
    dict_finviz = get_dict_from_df(finviz_fundamentals)

    return dict_finviz


def get_pe_and_dividend(division_type, division_value):
    """
    Getting P/E and Dividend for demanded type
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


def get_sector_country_pe_div(sector, country):
    """
    Getting P/E et Dividend yield for sector and country.
    :param sector: stocks sector
    :param country: stocks country
    :return: dictionary with P/E and Div yield of country and sector
    """

    # fundamentals of the sector and country
    pe_sector, div_sector = get_pe_and_dividend('sector', sector)
    pe_country, div_country = get_pe_and_dividend('country', country)

    dictionary = dict()
    dictionary['pe_sector'] = pe_sector
    dictionary['pe_country'] = pe_country
    dictionary['div_sector'] = div_sector
    dictionary['div_country'] = div_country

    return dictionary


def get_finviz_sector_country(ticker):
    """
    Getting country and sector of demanded stock.
    :param ticker: ticker which sector and country we are searching for
    :return: dictionary with sector name, country name and their fundamentals
    """

    df = get_finviz_info(ticker)

    # useful info (line like 'Technology | Consumer Electronics | USA' for Apple, from which we can extract its sector
    # and country)
    useful_info = df[4][0][2].split('|')
    sector = useful_info[0].strip()
    country = useful_info[2].strip()

    sector_country = get_sector_country_pe_div(sector, country)
    sector_country['sector'] = sector
    sector_country['country'] = country

    return sector_country
