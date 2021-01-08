from flaskr.tickers.db_interact import get_fundamentals

US_INFLATION = 2.3              # now constant - needs to be extracted
US_LOW_RISK = 0.1
US_EARNINGS_GROWTH_RATE = 9.5   # now constant - needs to be extracted
PE_MARKET = 33.83               # now constant - needs to be extracted


def get_coefficients(ticker):
    """Calculating coefficients of stocks perspective
    """

    json_dict = get_fundamentals(ticker)
    coefficients = dict()

    # Value
    # the next one needs to calculate p/e of us market
    coefficients['value'] = 1 if PE_MARKET >= json_dict['pe_ratio'] > 0 else 0
    coefficients['value'] += 1 if 1 > json_dict['peg_ratio'] > 0 else 0
    coefficients['value'] += 1 if 1 > json_dict['pb_ratio'] > 0 else 0
    coefficients['value'] += 1 if json_dict['dcf'] < 0.2 * json_dict['price'] else 0
    coefficients['value'] += 1 if json_dict['dcf'] < 0.4 * json_dict['price'] else 0
    # the next one needs to be replaced by comparing stocks p/e to industry p/e
    coefficients['value'] += 1 if 0 < json_dict['ps_ratio'] <= 2 else 0

    # Health
    # watch closely balance sheet from finviz
    coefficients['health'] = 1 if json_dict['short_term_assets'] > json_dict['short_term_liabilities'] else 0
    coefficients['health'] += 1 if json_dict['short_term_assets'] > json_dict['long_term_liabilities'] else 0
    coefficients['health'] += 1 if json_dict['debt_equity_ratio_now'] < json_dict['debt_equity_ratio_5ya'] else 0
    coefficients['health'] += 1 if json_dict['debt_equity_ratio_now'] < 0.4 else 0
    coefficients['health'] += 1 if json_dict['operating_cash_flow'] > 0.2 * json_dict['total_debt'] else 0
    coefficients['health'] += 1 if json_dict['interest_coverage'] > 5 else 0

    # Dividends
    # the next two needs to be calculated automatically as top25% and top75% us companies dividend yield
    high_dividend_yield = 2
    low_dividend_yield = 1
    coefficients['dividends'] = 1 if json_dict['dividend_yield'] > low_dividend_yield else 0
    coefficients['dividends'] += 1 if json_dict['dividend_yield'] > high_dividend_yield else 0
    # the next one needs to be calculated as if the dividend/share has been volatile in past 10 years
    # needs to think of - possible with financial API
    coefficients['dividends'] += 1 if json_dict['dividend_yield'] else 0
    coefficients['dividends'] += 1 if 0 < json_dict['payout_ratio'] < 0.9 else 0
    coefficients['dividends'] += 1 if json_dict['ten_years_dps_growth'] > 0 else 0
    # the next one needs to be calculated as if expected dividends will be covered by net profit in 3 years
    coefficients['dividends'] += 1 if json_dict['dps_growth'] > 0 else 0

    # Past
    # the next one needs to be calculated as if eps_growth is over the industry eps growth
    coefficients['past'] = 1 if json_dict['growth_eps_now'] > 0.2 else 0
    coefficients['past'] += 1 if json_dict['eps_now'] > json_dict['eps_5ya']  else 0
    coefficients['past'] += 1 if json_dict['growth_eps_now'] > json_dict['growth_eps_5ya'] else 0
    coefficients['past'] += 1 if json_dict['roe'] > 0.2 else 0
    coefficients['past'] += 1 if json_dict['roce_now'] > json_dict['roce_3ya'] else 0
    # the next one needs to be calculated as if roa > industry average ROA
    coefficients['past'] += 1 if json_dict['roa'] > 0.05 else 0

    # Future
    # for the next us_inflation and us_low_risk_investments to be calculated automatically
    coefficients['future'] = 1 if json_dict['net_income_growth'] > US_LOW_RISK + US_INFLATION else 0
    # the next one needs to calculate market average growth rate in earnings
    coefficients['future'] += 1 if json_dict['net_income_growth'] > US_EARNINGS_GROWTH_RATE else 0
    coefficients['future'] += 1 if json_dict['revenue_growth'] > 0.2 else 0
    coefficients['future'] += 1 if json_dict['net_income_growth'] > 0.2 else 0
    coefficients['future'] += 1 if json_dict['rating_ROE'] >= 3 else 0
    # we need also to to calculate if growth rate in revenue is greater than market average growth rate in revenue
    # we'll use analysts rating
    coefficients['future'] += 1 if json_dict['analysts_score'] >= 3 else 0

    return coefficients
