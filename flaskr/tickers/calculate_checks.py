US_INFLATION = 0.62                 # now constant - needs to be extracted
US_LOW_RISK = 0.01
US_NET_INCOME_GROWTH_RATE = -6.52   # https://csimarket.com/Industry/industry_growth_rates.php?rev&
US_REVENUE_GROWTH_RATE = 1.63       # now constant - needs to be extracted


def get_value_checks(dictionary):
    """
    :param dictionary: dict where we get fundamentals
    :return: checks of company value
    """

    # Value - done completely
    value = list()
    value.append(1 if dictionary['dcf'] < 0.2 * dictionary['price'] else 0)
    value.append(1 if dictionary['dcf'] < 0.4 * dictionary['price'] else 0)
    value.append(1 if dictionary['pe_country'] >= dictionary['pe_ratio'] > 0 else 0)
    value.append(1 if dictionary['pe_sector'] >= dictionary['pe_ratio'] > 0 else 0)
    value.append(1 if 1 > dictionary['peg_ratio'] > 0 else 0)
    value.append(1 if 1 > dictionary['pb_ratio'] > 0 else 0)

    return value


def get_health_checks(dictionary):
    """
    :param dictionary: dict where we get fundamentals
    :return: coefficient of company health
    """

    # Health - done completely
    health = list()
    health.append(1 if dictionary['short_term_assets'] > dictionary['short_term_liabilities'] else 0)
    health.append(1 if dictionary['short_term_assets'] > dictionary['long_term_liabilities'] else 0)
    health.append(1 if dictionary['debt_equity_ratio_now'] <= dictionary['debt_equity_ratio_5ya'] else 0)
    health.append(1 if dictionary['debt_equity_ratio_now'] < 0.4 else 0)
    health.append(1 if dictionary['operating_cash_flow'] > 0.2 * dictionary['total_debt'] else 0)
    health.append(1 if dictionary['interest_coverage'] > 5 else 0)

    return health


def get_dividends_checks(dictionary):
    """
    :param dictionary: dict where we get fundamentals
    :return: coefficient of company dividends
    """

    # Dividends - some replaced, some need to be implemented
    dividends = list()

    # the first two are replaced by checking if div are higher than sector and country averages
    dividends.append(1 if dictionary['dividend_yield'] > dictionary['div_sector'] else 0)
    dividends.append(1 if dictionary['dividend_yield'] > dictionary['div_country'] else 0)
    # the next one needs to be calculated as if the dividend/share has been volatile in past 10 years
    dividends.append(1 if dictionary['ten_years_dps_growth'] > 0 else 0)
    dividends.append(1 if dictionary['dividends_paid_now'] > dictionary['dividends_paid_10ya'] else 0)
    dividends.append(1 if 0 < dictionary['payout_ratio'] < 0.9 else 0)
    # the next one needs to be calculated as if expected dividends will be covered by net profit in 3 years
    dividends.append(1 if dictionary['dps_growth'] > 0 else 0)

    return dividends


def get_past_checks(dictionary):
    """
    :param dictionary: dict where we get fundamentals
    :return: coefficient of company past
    """

    # Past - the first replaced and the last need to be calculated
    past = list()

    # the next one needs to be calculated as if eps_growth is over the industry eps growth
    past.append(1 if dictionary['growth_eps_now'] > 0.2 else 0)
    past.append(1 if dictionary['eps_now'] > dictionary['eps_5ya'] else 0)
    past.append(1 if dictionary['growth_eps_now'] > dictionary['growth_eps_5ya'] else 0)
    past.append(1 if dictionary['roe'] > 0.2 else 0)
    past.append(1 if dictionary['roce_now'] > dictionary['roce_3ya'] else 0)
    # the next one needs to be calculated as if roa > industry average ROA
    past.append(1 if dictionary['roa'] > 0.05 else 0)

    return past


def get_future_checks(dictionary):
    """
    :param dictionary: dict where we get fundamentals
    :return: coefficient of company future
    """

    # Future - constants need to be calculated automatically
    future = list()

    # for the next us_inflation and us_low_risk_investments to be calculated automatically
    future.append(1 if dictionary['net_income_growth'] > US_LOW_RISK + US_INFLATION else 0)
    # the next one needs to calculate market average growth rate in earnings
    future.append(1 if dictionary['net_income_growth'] > US_NET_INCOME_GROWTH_RATE else 0)
    future.append(1 if dictionary['revenue_growth'] > US_REVENUE_GROWTH_RATE else 0)
    future.append(1 if dictionary['net_income_growth'] > 0.2 else 0)
    future.append(1 if dictionary['revenue_growth'] > 0.2 else 0)
    future.append(1 if dictionary['rating_ROE'] >= 3 else 0)

    return future


def get_checks(fundamentals_dict):
    """Performing checks for perspective diagram
    """

    coefficients = dict()

    # Calculating coefficients
    coefficients['value'] = get_value_checks(fundamentals_dict)
    coefficients['health'] = get_health_checks(fundamentals_dict)
    coefficients['dividends'] = get_dividends_checks(fundamentals_dict)
    coefficients['past'] = get_past_checks(fundamentals_dict)
    coefficients['future'] = get_future_checks(fundamentals_dict)

    return coefficients
