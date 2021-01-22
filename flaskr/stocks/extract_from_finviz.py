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


def get_finviz_table(ticker):
    """
    Getting the header of the finviz site.
    :param ticker: stocks ticker to search for on the site.
    :return: site header dataframe
    """
    request = requests.get(f"{FINVIZ_URL_BASE}", headers=FINVIZ_HEADERS, params={"t": ticker})
    df = pd.read_html(request.text)

    return df


def get_finviz_stocks_fundamentals(ticker):
    """
    Getting fundamentals from finviz site.
    :param ticker: ticker to search for on the site
    :return: fundamentals in the form of dictionary
    """

    df = get_finviz_table(ticker)

    # main fundamentals table from site
    finviz_fundamentals = df[5]

    # transforming dataframe to dictionary
    dict_finviz = get_dict_from_df(finviz_fundamentals)

    return dict_finviz


def get_division_fundamentals_from_overview_page(division_type, division_value):
    """
    Getting P/E, Forward P/E and Dividend for demanded type
    :param division_type: 'sector' or 'country'
    :param division_value: sector or country
    :return: demanded P/E, forward P/E and Dividend yield
    """

    request = requests.get(FINVIZ_URL_GROUP, headers=FINVIZ_HEADERS, params={'v': 110, 'g': division_type})
    df = pd.read_html(request.text)[4]

    idx_value = df.index[df[1] == division_value][0]
    pe = df[5][idx_value]
    fw_pe = df[6][idx_value]
    div = df[4][idx_value][:-1]
    return float(pe), float(fw_pe), float(div)


def get_division_fundamentals_from_valuation_page(division_type, division_value):
    """
    Getting EPS_last_5Y, EPS_next_5Y for demanded type
    :param division_type: 'sector' or 'country'
    :param division_value: sector or country
    :return: demanded eps_next_5y, eps_last_5y
    """

    request = requests.get(FINVIZ_URL_GROUP, headers=FINVIZ_HEADERS, params={'v': 120, 'g': division_type})
    df = pd.read_html(request.text)[4]

    idx_value = df.index[df[1] == division_value][0]
    eps_past_5y = df[9][idx_value][:-1]
    eps_next_5y = df[10][idx_value][:-1]
    return float(eps_past_5y), float(eps_next_5y)


def get_sector_country_fundamentals(sector, country):
    """
    Getting fundamentals for country and sector
    :param sector: stocks sector
    :param country: stocks country
    :return: dictionary with fundamentals of country and sector
    """

    dictionary = dict()
    dictionary['pe_sector'], dictionary['forward_pe_sector'], dictionary['div_sector'] = \
        get_division_fundamentals_from_overview_page('sector', sector)
    dictionary['pe_country'], dictionary['forward_pe_country'], dictionary['div_country'] = \
        get_division_fundamentals_from_overview_page('country', country)
    dictionary['eps_g_past_5y_sector'], dictionary['eps_g_next_5y_sector'] = \
        get_division_fundamentals_from_valuation_page('sector', sector)
    dictionary['eps_g_past_5y_country'], dictionary['eps_g_next_5y_country'] = \
        get_division_fundamentals_from_valuation_page('country', country)

    return dictionary


def get_finviz_sector_and_country(ticker):
    """
    Getting the country and the sector of the demanded stock.
    :param ticker: ticker which sector and country we are searching for
    :return: dictionary with sector name, country name and their fundamentals
    """

    df = get_finviz_table(ticker)

    # useful info (line like 'Technology | Consumer Electronics | USA' for Apple, from which we can extract its sector
    # and country)
    useful_info = df[4][0][2].split('|')
    sector = useful_info[0].strip()
    country = useful_info[2].strip()

    sector_country_fundamentals = get_sector_country_fundamentals(sector, country)
    sector_country_fundamentals['sector'] = sector
    sector_country_fundamentals['country'] = country

    return sector_country_fundamentals
