from datetime import datetime
import requests
from config import FINANCIAL_API_KEY, FINANCIAL_BASE_URL
from flaskr.stocks.extract_from_finviz import get_finviz_fundamentals


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


def add_finviz_fundamentals(dict_to_add, dict_from_finviz) -> None:
    """
    Adding fundamentals from finviz dict to resulting dictionary.
    :param dict_to_add: dictionary to add fundamentals from finviz
    :param dict_from_finviz: fundamentals from finviz
    """

    dict_to_add['price'] = float(dict_from_finviz.get('Price'))
    dict_to_add['sector'] = dict_from_finviz.get('sector')
    dict_to_add['pe_ratio'] = value_handler(dict_from_finviz.get('P/E'))
    dict_to_add['peg_ratio'] = value_handler(dict_from_finviz.get('PEG'))
    dict_to_add['pb_ratio'] = value_handler(dict_from_finviz.get('P/B'))
    dict_to_add['dividend_yield'] = value_handler(dict_from_finviz.get('Dividend %'))
    dict_to_add['payout_ratio'] = value_handler(dict_from_finviz.get('Payout')) * 0.01
    dict_to_add['roe'] = value_handler(dict_from_finviz.get('ROE')) * 0.01
    dict_to_add['roa'] = value_handler(dict_from_finviz.get('ROA')) * 0.01


def add_financial_ratios(dict_to_add, ticker) -> None:
    """
    Adding financial ratios to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    financial_ratios_url = FINANCIAL_BASE_URL + f"ratios/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    financial_ratios_json = requests.get(financial_ratios_url).json()
    financial_ratios_json_now = financial_ratios_json[0]
    financial_ratios_json_3ya = index_error_handler(financial_ratios_json, 3)
    financial_ratios_json_5ya = index_error_handler(financial_ratios_json, 5)

    dict_to_add['debt_equity_ratio_now'] = float(financial_ratios_json_now.get('debtEquityRatio', 0))
    dict_to_add['debt_equity_ratio_5ya'] = float(financial_ratios_json_5ya.get('debtEquityRatio', 0))
    dict_to_add['interest_coverage'] = float(financial_ratios_json_now.get('interestCoverage', 0))
    dict_to_add['roce_now'] = float(financial_ratios_json_now.get('returnOnCapitalEmployed', 0))
    dict_to_add['roce_3ya'] = float(financial_ratios_json_3ya.get('returnOnCapitalEmployed', 0))


def add_financial_growth_data(dict_to_add, ticker) -> None:
    """
    Adding financial growth data to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    financial_growth_url = FINANCIAL_BASE_URL + f"financial-growth/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    financial_growth_json = requests.get(financial_growth_url).json()
    financial_growth_json_now = financial_growth_json[0]
    financial_growth_json_5ya = index_error_handler(financial_growth_json, 5)

    dict_to_add['debt_growth'] = float(financial_growth_json_now.get('debtGrowth', 0))
    dict_to_add['dps_growth'] = float(financial_growth_json_now.get('dividendsperShareGrowth', 0))
    dict_to_add['ten_years_dps_growth'] = float(financial_growth_json_now.get('tenYDividendperShareGrowthPerShare', 0))
    dict_to_add['net_income_growth'] = float(financial_growth_json_now.get('netIncomeGrowth', 0))
    dict_to_add['revenue_growth'] = float(financial_growth_json_now.get('revenueGrowth', 0))
    dict_to_add['growth_eps_now'] = float(financial_growth_json_now.get('epsgrowth', 0))
    dict_to_add['growth_eps_5ya'] = float(financial_growth_json_5ya.get('epsgrowth', 0))


def add_income_stmt_data(dict_to_add, ticker):
    """
    Adding income statement data to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    income_statement_url = FINANCIAL_BASE_URL + f"income-statement/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    income_statement_json = requests.get(income_statement_url).json()
    income_statement_json_now = income_statement_json[0]
    income_statement_json_5ya = index_error_handler(income_statement_json, 5)

    dict_to_add['eps_now'] = float(income_statement_json_now.get('eps', 0))
    dict_to_add['eps_5ya'] = float(income_statement_json_5ya.get('eps', 0))


def add_historical_rating(dict_to_add, ticker):
    """
    Adding historical rating to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    historical_rating_url = FINANCIAL_BASE_URL + f"historical-rating/{ticker}?apikey={FINANCIAL_API_KEY}"
    historical_rating_json = requests.get(historical_rating_url).json()[0]

    dict_to_add['analysts_rating'] = historical_rating_json['rating']
    dict_to_add['analysts_score'] = historical_rating_json.get('ratingScore', 0)
    dict_to_add['analysts_recommendation'] = historical_rating_json['ratingRecommendation']
    dict_to_add['rating_DCF'] = historical_rating_json.get('ratingDetailsDCFScore', 0)
    dict_to_add['rating_ROE'] = historical_rating_json.get('ratingDetailsROEScore', 0)
    dict_to_add['rating_ROA'] = historical_rating_json.get('ratingDetailsROAScore', 0)
    dict_to_add['rating_DE'] = historical_rating_json.get('ratingDetailsDEScore', 0)
    dict_to_add['rating_PE'] = historical_rating_json.get('ratingDetailsPEScore', 0)
    dict_to_add['rating_PB'] = historical_rating_json.get('ratingDetailsPBScore', 0)


def add_profile_data(dict_to_add, ticker):
    """
    Adding profile data to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    profile_url = FINANCIAL_BASE_URL + f"profile/{ticker}?apikey={FINANCIAL_API_KEY}"
    profile_json = requests.get(profile_url).json()[0]

    dict_to_add['dcf'] = float(profile_json.get('dcf', 0))


def add_balance_sheet_data(dict_to_add, ticker):
    """
    Adding balance sheet data to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    balance_sheet_url = FINANCIAL_BASE_URL + f"balance-sheet-statement/{ticker}?apikey={FINANCIAL_API_KEY}"
    balance_sheet_json = requests.get(balance_sheet_url).json()[0]

    dict_to_add['short_term_liabilities'] = balance_sheet_json.get('totalCurrentLiabilities', 0)
    dict_to_add['long_term_liabilities'] = balance_sheet_json.get('totalLiabilities', 0)
    dict_to_add['short_term_assets'] = balance_sheet_json.get('totalCurrentAssets', 0)
    dict_to_add['long_term_assets'] = balance_sheet_json.get('totalAssets', 0)
    dict_to_add['total_debt'] = balance_sheet_json.get('totalDebt', 0)


def add_cash_flow_data(dict_to_add, ticker):
    """
    Adding cash flow data to the dict.
    :param dict_to_add: dictionary to add info
    :param ticker: ticker we are working with
    """

    cash_flow_url = FINANCIAL_BASE_URL + f"cash-flow-statement/{ticker}?apikey={FINANCIAL_API_KEY}&limit=10"
    cash_flow_json = requests.get(cash_flow_url).json()
    cash_flow_json_now = cash_flow_json[0]
    cash_flow_json_10ya = index_error_handler(cash_flow_json, 9)

    dict_to_add['operating_cash_flow'] = cash_flow_json_now.get('operatingCashFlow', 0)
    dict_to_add['dividends_paid_now'] = float(-cash_flow_json_now.get('dividendsPaid', 0))
    dict_to_add['dividends_paid_10ya'] = float(-cash_flow_json_10ya.get('dividendsPaid', 0))


def extract_fundamentals(ticker):
    """
    Extracting fundamentals by Ticker from API and finviz site.
    :param ticker: ticker which fundamentals we are searching for
    :return: fundamentals in the form of dictionary
    """

    fundamentals = dict()
    fundamentals['ticker'] = ticker

    # adding fundamentals to returning dictionary
    finviz_fundamentals = get_finviz_fundamentals(ticker)
    add_finviz_fundamentals(fundamentals, finviz_fundamentals)
    add_financial_ratios(fundamentals, ticker)
    add_financial_growth_data(fundamentals, ticker)
    add_income_stmt_data(fundamentals, ticker)
    add_historical_rating(fundamentals, ticker)
    add_profile_data(fundamentals, ticker)
    add_balance_sheet_data(fundamentals, ticker)
    add_cash_flow_data(fundamentals, ticker)

    fundamentals['date'] = datetime.today()
    fundamentals['dividend_volatile'] = 0

    return fundamentals


def get_recommendations(dictionary):
    """
    Getting analytics recommendations from fundamentals dictionary.
    :param dictionary: dictionary in which we are searching for recommendations
    :return: recommendations in the form of dictionary
    """

    dict_recommendations = dict()
    dict_recommendations['Analysts recommendations'] = dictionary['analysts_recommendation']
    dict_recommendations['Overall rating'] = dictionary['analysts_score']
    dict_recommendations['Discounted cash flow rating'] = dictionary['rating_DCF']
    dict_recommendations['Return on equity rating'] = dictionary['rating_ROE']
    dict_recommendations['Return on assets rating'] = dictionary['rating_ROA']
    dict_recommendations['Price/Earnings ratio rating'] = dictionary['rating_PE']
    dict_recommendations['Price/Book ratio rating'] = dictionary['rating_PB']

    return dict_recommendations
