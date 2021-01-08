from datetime import datetime
import requests
from config import FINANCIAL_API_KEY, FINANCIAL_BASE_URL
from flaskr.tickers.extract_fundamentals_from_finviz import get_finviz_fundamentals


def index_error_handler(list_, index_):
    """If encounters IndexError, returns empty dictionary
    """

    try:
        list_element = list_[index_]
    except IndexError:
        list_element = {}
    return list_element


def extract_fundamentals(ticker):
    """Getting fundamentals by Ticker from API
    """

    dict_finviz = get_finviz_fundamentals(ticker)

    # URLs
    base_url = FINANCIAL_BASE_URL
    ending_url = f"{ticker}?apikey={FINANCIAL_API_KEY}"
    
    financial_ratios_url = base_url + "ratios/" + ending_url + "&limit=10"
    financial_growth_url = base_url + "financial-growth/" + ending_url + "&limit=10"
    income_statement_url = base_url + "income-statement/" + ending_url + "&limit=10"
    historical_rating_url = base_url + "historical-rating/" + ending_url
    profile_url = base_url + "profile/" + ending_url
    balance_sheet_url = base_url + "balance-sheet-statement/" + ending_url
    cash_flow_url = base_url + "cash-flow-statement/" + ending_url

    # json requests
    # to do - add status code check
    financial_ratios_json = requests.get(financial_ratios_url).json()
    financial_ratios_json_5ya = index_error_handler(financial_ratios_json, 5)
    financial_ratios_json_3ya = index_error_handler(financial_ratios_json, 3)
    financial_ratios_json_now = financial_ratios_json[0]

    income_statement_json = requests.get(income_statement_url).json()
    income_statement_json_now = income_statement_json[0]
    income_statement_json_5ya = index_error_handler(income_statement_json, 5)

    financial_growth_json = requests.get(financial_growth_url).json()
    financial_growth_json_now = financial_growth_json[0]
    financial_growth_json_5ya = index_error_handler(financial_growth_json, 5)

    historical_rating_json = requests.get(historical_rating_url).json()[0]
    profile_json = requests.get(profile_url).json()[0]
    balance_sheet_json = requests.get(balance_sheet_url).json()[0]
    cash_flow_json = requests.get(cash_flow_url).json()[0]
    
    # dict to return
    fundamentals = dict()
    
    # Value
    # to do - make p/e ratio check vs industries p/e - with finviz
    # to do - automatically extract p/e of the market. Now it's a constant

    fundamentals['ticker'] = ticker
    fundamentals['price'] = float(dict_finviz.get('Price'))
    fundamentals['sector'] = dict_finviz.get('sector')
    fundamentals['dcf'] = float(profile_json.get('dcf'))
    fundamentals['pe_ratio'] = float(dict_finviz.get('P/E'))
    fundamentals['peg_ratio'] = float(dict_finviz.get('PEG'))
    fundamentals['pb_ratio'] = float(dict_finviz.get('P/B'))
    
    fundamentals['quick_ratio'] = float(dict_finviz.get('Quick Ratio'))
    fundamentals['ps_ratio'] = float(dict_finviz.get('P/S'))

    # Health
    # to do - read balance sheet from finviz

    fundamentals['short_term_liabilities'] = balance_sheet_json['shortTermDebt']
    fundamentals['long_term_liabilities'] = balance_sheet_json['longTermDebt']
    fundamentals['short_term_assets'] = balance_sheet_json['shortTermInvestments']
    fundamentals['long_term_assets'] = balance_sheet_json['longTermInvestments']
    fundamentals['debt_equity_ratio_now'] = float(financial_ratios_json_now.get('debtEquityRatio', 0))
    fundamentals['debt_equity_ratio_5ya'] = float(financial_ratios_json_5ya.get('debtEquityRatio', 0))
    fundamentals['operating_cash_flow'] = cash_flow_json['operatingCashFlow']
    fundamentals['total_debt'] = balance_sheet_json['totalDebt']
    fundamentals['interest_coverage'] = float(financial_ratios_json_now['interestCoverage'])
    fundamentals['debt_growth'] = float(financial_growth_json_now['debtGrowth'])
    
    # Dividends
    # to do - if the current dividend yield is higher than 25% and 75% of the market dividends
    # to do - calculate if the dividend/share was volatile during last 10 years (dropped over 10 percent)
    # to do - calculate if the dividend payed is greater than dividend payed 10 years ago
    # to do - calculate expected payout ratio

    try:
        fundamentals['dividend_yield'] = float(dict_finviz.get('Dividend %')[:-1])
    except ValueError:
        fundamentals['dividend_yield'] = 0
    fundamentals['payout_ratio'] = float(dict_finviz.get('Payout')[:-1]) * 0.01
    fundamentals['dps_growth'] = float(financial_growth_json_now.get('dividendsperShareGrowth', 0))
    fundamentals['ten_years_dps_growth'] = float(financial_growth_json_now.get('tenYDividendperShareGrowthPerShare', 0))
    
    # Future
    # low risk investments + inflation must be calculated automatically
    # compare net income growth rate to industry average growth rate
    # compare revenue growth rate to industry average growth rate
    # calculate if expected ROE in 3 years > 20% of the stock
    
    fundamentals['net_income_growth'] = float(financial_growth_json_now.get('netIncomeGrowth', 0))
    fundamentals['revenue_growth'] = float(financial_growth_json_now.get('revenueGrowth', 0))
    
    # Past
    # calculate eps growth vs industry eps growth
    # calculate eps now > eps 5 years ago
    # calculate if current eps growth > average annual eps growth over 5 last years
    # calculate if roa > industry average roa

    fundamentals['growth_eps_now'] = float(financial_growth_json_now.get('epsgrowth', 0))
    fundamentals['growth_eps_5ya'] = float(financial_growth_json_5ya.get('epsgrowth', 0))
    fundamentals['eps_now'] = float(income_statement_json_now.get('eps', 0))
    fundamentals['eps_5ya'] = float(income_statement_json_5ya.get('eps', 0))
    fundamentals['roe'] = float(dict_finviz.get('ROE')[:-1]) * 0.01
    fundamentals['roce_now'] = float(financial_ratios_json_now.get('returnOnCapitalEmployed', 0))
    fundamentals['roce_3ya'] = float(financial_ratios_json_3ya.get('returnOnCapitalEmployed', 0))
    fundamentals['roa'] = float(dict_finviz.get('ROA')[:-1]) * 0.01
    
    # Analysts rating
    fundamentals['analysts_rating'] = historical_rating_json['rating']
    fundamentals['analysts_score'] = historical_rating_json['ratingScore']
    fundamentals['analysts_recommendation'] = historical_rating_json['ratingRecommendation']
    fundamentals['rating_DCF'] = historical_rating_json['ratingDetailsDCFScore']
    fundamentals['rating_ROE'] = historical_rating_json['ratingDetailsROEScore']
    fundamentals['rating_ROA'] = historical_rating_json['ratingDetailsROAScore']
    fundamentals['rating_DE'] = historical_rating_json['ratingDetailsDEScore']
    fundamentals['rating_PE'] = historical_rating_json['ratingDetailsPEScore']
    fundamentals['rating_PB'] = historical_rating_json['ratingDetailsPBScore']

    fundamentals['date'] = datetime.today()

    return fundamentals
