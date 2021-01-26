from datetime import datetime
import json
import requests
from config import FINANCIAL_API_KEY, FINANCIAL_BASE_URL
from flaskr.stocks.extract_from_finviz import get_finviz_stocks_fundamentals


def index_error_handler(list_, index_):
    """
    If encounters IndexError, returns an empty dictionary.
    :param list_: list in which we search element
    :param index_: index of element
    :return: element in the list or empty dictionary
    """

    try:
        list_element = list_[index_]
    except IndexError:
        list_element = {}
    return list_element


def none_handler(value):
    """
    If encounters None value, replace it by zero
    :param value: value from API
    :return: value or zero if None
    """

    try:
        value = float(value)
    except TypeError:
        value = 0
    return value


def value_handler(value):
    """
    If encounters '-', returns 0.
    :param value: value from the field in finviz dictionary
    :return: int value from this field
    """

    if value == '-':
        return 0
    elif value[-1] == '%':
        return float(value[:-1])
    else:
        return value


def get_checked_finviz_fundamentals(dict_from_finviz):
    """
    Getting reformatted to correct form fundamentals from finviz.
    :param dict_from_finviz: fundamentals from finviz
    :return resulting dictionary
    """

    dict_ = dict()
    dict_['price'] = float(dict_from_finviz.get('Price'))
    dict_['sector'] = dict_from_finviz.get('sector')
    dict_['pe_ratio'] = value_handler(dict_from_finviz.get('P/E'))
    dict_['peg_ratio'] = value_handler(dict_from_finviz.get('PEG'))
    dict_['pb_ratio'] = value_handler(dict_from_finviz.get('P/B'))
    dict_['dividend_yield'] = value_handler(dict_from_finviz.get('Dividend %'))
    dict_['payout_ratio'] = value_handler(dict_from_finviz.get('Payout')) * 0.01
    dict_['roe'] = value_handler(dict_from_finviz.get('ROE')) * 0.01
    dict_['roa'] = value_handler(dict_from_finviz.get('ROA')) * 0.01
    dict_['forward_pe'] = value_handler(dict_from_finviz.get('Forward P/E'))
    dict_['eps_g_next_5y'] = value_handler(dict_from_finviz.get('EPS next 5Y'))
    dict_['eps_g_past_5y'] = value_handler(dict_from_finviz.get('EPS past 5Y'))
    dict_['eps_g_now'] = value_handler(dict_from_finviz.get('EPS this Y'))

    return dict_


def get_financial_ratios(ticker):
    """
    Getting financial ratios.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    financial_ratios_url = FINANCIAL_BASE_URL + f"ratios/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    try:
        financial_ratios_json = requests.get(financial_ratios_url).json()
    except json.decoder.JSONDecodeError:
        financial_ratios_json = dict(dict())

    financial_ratios_json_now = financial_ratios_json[0]
    financial_ratios_json_3ya = index_error_handler(financial_ratios_json, 3)
    financial_ratios_json_5ya = index_error_handler(financial_ratios_json, 5)

    dict_ = dict()
    dict_['debt_equity_ratio_now'] = none_handler(financial_ratios_json_now.get('debtEquityRatio', 0))
    dict_['debt_equity_ratio_5ya'] = none_handler(financial_ratios_json_5ya.get('debtEquityRatio', 0))
    dict_['interest_coverage'] = none_handler(financial_ratios_json_now.get('interestCoverage', 0))
    dict_['roce_now'] = none_handler(financial_ratios_json_now.get('returnOnCapitalEmployed', 0))
    dict_['roce_3ya'] = none_handler(financial_ratios_json_3ya.get('returnOnCapitalEmployed', 0))

    return dict_


def get_financial_growth_data(ticker):
    """
    Getting financial growth data.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    financial_growth_url = FINANCIAL_BASE_URL + f"financial-growth/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    try:
        financial_growth_json = requests.get(financial_growth_url).json()
    except json.decoder.JSONDecodeError:
        financial_growth_json = dict(dict())

    financial_growth_json_now = financial_growth_json[0]

    dict_ = dict()
    dict_['debt_growth'] = none_handler(financial_growth_json_now.get('debtGrowth', 0))
    dict_['dps_growth'] = none_handler(financial_growth_json_now.get('dividendsperShareGrowth', 0))
    dict_['ten_years_dps_growth'] = none_handler(financial_growth_json_now.get('tenYDividendperShareGrowthPerShare', 0))
    dict_['net_income_growth'] = none_handler(financial_growth_json_now.get('netIncomeGrowth', 0))
    dict_['revenue_growth'] = none_handler(financial_growth_json_now.get('revenueGrowth', 0))

    return dict_


def get_historical_rating(ticker):
    """
    Getting historical rating.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    historical_rating_url = FINANCIAL_BASE_URL + f"historical-rating/{ticker}?apikey={FINANCIAL_API_KEY}"
    try:
        historical_rating_json = requests.get(historical_rating_url).json()[0]
    except json.decoder.JSONDecodeError:
        historical_rating_json = dict()

    dict_ = dict()
    dict_['analysts_rating'] = historical_rating_json.get('rating', '')
    dict_['analysts_score'] = historical_rating_json.get('ratingScore', 0)
    dict_['analysts_recommendation'] = historical_rating_json.get('ratingRecommendation', '')
    dict_['rating_DCF'] = historical_rating_json.get('ratingDetailsDCFScore', 0)
    dict_['rating_ROE'] = historical_rating_json.get('ratingDetailsROEScore', 0)
    dict_['rating_ROA'] = historical_rating_json.get('ratingDetailsROAScore', 0)
    dict_['rating_DE'] = historical_rating_json.get('ratingDetailsDEScore', 0)
    dict_['rating_PE'] = historical_rating_json.get('ratingDetailsPEScore', 0)
    dict_['rating_PB'] = historical_rating_json.get('ratingDetailsPBScore', 0)

    return dict_


def get_profile_data(ticker):
    """
    Getting profile data.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    profile_url = FINANCIAL_BASE_URL + f"profile/{ticker}?apikey={FINANCIAL_API_KEY}"
    try:
        profile_json = requests.get(profile_url).json()[0]
    except json.decoder.JSONDecodeError:
        profile_json = dict()

    dict_ = dict()
    dict_['dcf'] = none_handler(profile_json.get('dcf', 0))
    dict_['description'] = profile_json.get('description', '')
    return dict_


def get_balance_sheet_data(ticker):
    """
    Getting balance sheet data.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    balance_sheet_url = FINANCIAL_BASE_URL + f"balance-sheet-statement/{ticker}?apikey={FINANCIAL_API_KEY}"
    try:
        balance_sheet_json = requests.get(balance_sheet_url).json()[0]
    except json.decoder.JSONDecodeError:
        balance_sheet_json = dict()

    dict_ = dict()
    dict_['short_term_liabilities'] = balance_sheet_json.get('totalCurrentLiabilities', 0)
    dict_['long_term_liabilities'] = balance_sheet_json.get('totalLiabilities', 0)
    dict_['short_term_assets'] = balance_sheet_json.get('totalCurrentAssets', 0)
    dict_['long_term_assets'] = balance_sheet_json.get('totalAssets', 0)
    dict_['total_debt'] = balance_sheet_json.get('totalDebt', 0)

    return dict_


def get_cash_flow_data(ticker):
    """
    Getting cash flow data.
    :param ticker: ticker we are working with
    :return resulting dictionary
    """

    cash_flow_url = FINANCIAL_BASE_URL + f"cash-flow-statement/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    try:
        cash_flow_json = requests.get(cash_flow_url).json()
    except json.decoder.JSONDecodeError:
        cash_flow_json = dict(dict())

    cash_flow_json_now = cash_flow_json[0]
    cash_flow_json_10ya = index_error_handler(cash_flow_json, 9)

    dict_ = dict()
    dict_['operating_cash_flow'] = cash_flow_json_now.get('operatingCashFlow', 0)
    dict_['dividends_paid_now'] = none_handler(-cash_flow_json_now.get('dividendsPaid', 0))
    dict_['dividends_paid_10ya'] = none_handler(-cash_flow_json_10ya.get('dividendsPaid', 0))

    return dict_


def get_all_stocks_fundamentals(ticker):
    """
    Extracting stocks fundamentals by its ticker from API and finviz site.
    :param ticker: ticker which fundamentals we are searching for
    :return: fundamentals in the form of dictionary
    """

    fundamentals = dict()
    fundamentals['ticker'] = ticker

    finviz_fundamentals = get_finviz_stocks_fundamentals(ticker)
    fundamentals.update(get_checked_finviz_fundamentals(finviz_fundamentals))
    fundamentals.update(get_financial_ratios(ticker))
    fundamentals.update(get_financial_growth_data(ticker))
    fundamentals.update(get_historical_rating(ticker))
    fundamentals.update(get_profile_data(ticker))
    fundamentals.update(get_balance_sheet_data(ticker))
    fundamentals.update(get_cash_flow_data(ticker))

    fundamentals['date'] = datetime.today()
    fundamentals['dividend_volatile'] = 0

    return fundamentals

