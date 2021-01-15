from flaskr.tickers.db_interact import get_stocks_fundamentals
from flaskr.tickers.extract_fundamentals import get_recommendations
from flaskr.tickers.plot_radar_chart import check_perspective_chart


US_INFLATION = 0.62                 # now constant - needs to be extracted
US_LOW_RISK = 0.01
US_NET_INCOME_GROWTH_RATE = -6.52   # https://csimarket.com/Industry/industry_growth_rates.php?rev&
US_REVENUE_GROWTH_RATE = 1.63       # now constant - needs to be extracted


def human_format(num):
    """
    Transforms bit number in human readable form.
    :param num: big number
    :return: number in human readable form
    """

    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def get_value_checks(dict_):
    """
    Verifies company value checks.
    :param dict_: dict where we get fundamentals
    :return: company value checks in the form of list
    """

    value = list()
    value.append(1 if dict_['dcf'] < 0.2 * dict_['price'] else 0)
    value.append(1 if dict_['dcf'] < 0.4 * dict_['price'] else 0)
    value.append(1 if dict_['pe_country'] >= dict_['pe_ratio'] > 0 else 0)
    value.append(1 if dict_['pe_sector'] >= dict_['pe_ratio'] > 0 else 0)
    value.append(1 if 1 > dict_['peg_ratio'] > 0 else 0)
    value.append(1 if 1 > dict_['pb_ratio'] > 0 else 0)

    return value


def get_value_description(dict_):
    """
    Gets company value checks description.
    :param dict_: dict where we get fundamentals
    :return: description of company value checks
    """

    value_descr = list()
    value_descr.append(f"Is the discounted cash flow value ({dict_['dcf']}) less than 20% of the share price "
                       f"({dict_['price']})?")
    value_descr.append(f"Is the discounted cash flow value ({dict_['dcf']}) less than 40% of the share price "
                       f"({dict_['price']})?")
    value_descr.append(f"Is the P/E ratio ({dict_['pe_ratio']}) less than the market average ({dict_['pe_country']}) "
                       f"but still greater than 0?")
    value_descr.append(f"Is the P/E ratio ({dict_['pe_ratio']}) less than the industry average ({dict_['pe_sector']}) "
                       f"but still greater than 0?")
    value_descr.append(f"Is the PEG ratio ({dict_['peg_ratio']}) within a reasonable range (0 to 1)?")
    value_descr.append(f"Is the P/B ratio ({dict_['pb_ratio']}) within a reasonable range (0 to 1)?")

    return value_descr


def get_health_checks(dict_):
    """
    Verify company health checks.
    :param dict_: dict where we get fundamentals
    :return: company health checks in the form of list
    """

    health = list()
    health.append(1 if dict_['short_term_assets'] > dict_['short_term_liabilities'] else 0)
    health.append(1 if dict_['short_term_assets'] > dict_['long_term_liabilities'] else 0)
    health.append(1 if dict_['debt_equity_ratio_now'] <= dict_['debt_equity_ratio_5ya'] else 0)
    health.append(1 if dict_['debt_equity_ratio_now'] < 0.4 else 0)
    health.append(1 if dict_['operating_cash_flow'] > 0.2 * dict_['total_debt'] else 0)
    health.append(1 if dict_['interest_coverage'] > 5 else 0)

    return health


def get_health_description(dict_):
    """
    Gets company health checks description.
    :param dict_: dict where we get fundamentals
    :return: description of company health checks
    """

    health_descr = list()
    health_descr.append(f"Are short term assets ({human_format(dict_['short_term_assets'])}) greater than "
                        f"short term liabilities ({human_format(dict_['short_term_liabilities'])})?")
    health_descr.append(f"Are short term assets ({human_format(dict_['short_term_assets'])}) greater than long term "
                        f"liabilities ({human_format(dict_['long_term_liabilities'])})?")
    health_descr.append(f"Has the debt to equity ratio ({round(dict_['debt_equity_ratio_now'], 2)}) decreased in the "
                        f"past 5 years (vs {round(dict_['debt_equity_ratio_5ya'], 2)})?")
    health_descr.append(f"Is the debt to equity ratio ({round(dict_['debt_equity_ratio_now'], 2)}) less than 40% "
                        f"(0.4)?")
    health_descr.append(f"Are 20% of debt ({human_format(dict_['total_debt'])}) covered by operating cash flows "
                        f"({human_format(dict_['operating_cash_flow'])})?")
    health_descr.append(f"Are earnings greater than 5x ({round(dict_['interest_coverage'], 2)}) the interest on debt "
                        f"(if company pays interest at all)?")

    return health_descr


def get_dividends_checks(dict_):
    """
    Verifies company dividends checks.
    :param dict_: dict where we get fundamentals
    :return: company dividends checks in the form of list
    """

    dividends = list()

    # the first two are replaced by checking if div are higher than sector and country averages
    dividends.append(1 if dict_['dividend_yield'] > dict_['div_sector'] else 0)
    dividends.append(1 if dict_['dividend_yield'] > dict_['div_country'] else 0)
    # the next one needs to be calculated as if the dividend/share has been volatile in past 10 years
    dividends.append(1 if dict_['ten_years_dps_growth'] > 0 else 0)
    dividends.append(1 if dict_['dividends_paid_now'] > dict_['dividends_paid_10ya'] else 0)
    dividends.append(1 if 0 < dict_['payout_ratio'] < 0.9 else 0)
    # the next one needs to be calculated as if expected dividends will be covered by net profit in 3 years
    dividends.append(1 if dict_['dps_growth'] > 0 else 0)

    return dividends


def get_dividends_description(dict_):
    """
    Gets company dividends checks description.
    :param dict_: dict where we get fundamentals
    :return: description of company dividends checks
    """

    div_description = list()
    div_description.append(f"Is the current dividend yield ({dict_['dividend_yield']}) higher than the industry "
                           f"average ({dict_['div_sector']})?")
    div_description.append(f"Is the current dividend yield ({dict_['dividend_yield']}) higher than the market average "
                           f"({dict_['div_country']})?")
    div_description.append(f"Is the growth in dividends per share over the past 10 years positive "
                           f"({dict_['ten_years_dps_growth']})?")
    div_description.append(f"Has the dividend payed ({human_format(dict_['dividends_paid_now'])}) increased in the past"
                           f" 10 years (vs {human_format(dict_['dividends_paid_10ya'])})?")
    div_description.append(f"Are dividends paid well covered by Net Profit (0 < {round(dict_['payout_ratio'], 2)} < "
                           f"0.9)?")
    div_description.append(f"Is the growth in dividends per share ({round(dict_['dps_growth'], 3)}) over the past year "
                           f"positive?")

    return div_description


def get_past_checks(dict_):
    """
    Verifies company past checks.
    :param dict_: dict where we get fundamentals
    :return: company past checks in the form of list
    """

    past = list()

    # the next one needs to be calculated as if eps_growth is over the industry eps growth
    past.append(1 if dict_['growth_eps_now'] > 0.2 else 0)
    past.append(1 if dict_['eps_now'] > dict_['eps_5ya'] else 0)
    past.append(1 if dict_['growth_eps_now'] > dict_['growth_eps_5ya'] else 0)
    past.append(1 if dict_['roe'] > 0.2 else 0)
    past.append(1 if dict_['roce_now'] > dict_['roce_3ya'] else 0)
    # the next one needs to be calculated as if roa > industry average ROA
    past.append(1 if dict_['roa'] > 0.05 else 0)

    return past


def get_past_description(dict_):
    """
    Gets company past checks description
    :param dict_: dict where we get fundamentals
    :return: description of company past checks
    """

    past_description = list()
    past_description.append(f"Is Has Earnings Per Share (EPS) growth ({round(dict_['growth_eps_now'], 2)}) exceeded "
                            f"20% (0.2) over the past year?")
    past_description.append(f"Is Have Earnings Per Share (EPS={dict_['eps_now']}) increased in past 5 years "
                            f"(vs {dict_['eps_5ya']})?")
    past_description.append(f"Is the current EPS growth ({round(dict_['growth_eps_now'], 2)}) higher than the average "
                            f"annual growth over the past 5 years (vs {round(dict_['growth_eps_5ya'], 2)})?")
    past_description.append(f"Is the Return on Equity (ROE={round(dict_['roe'], 2)}) higher than 20% (0.2)?")
    past_description.append(f"Has the Return on Capital Employed (ROCE={round(dict_['roce_now'], 2)}) increased from 3 "
                            f"years ago (vs {round(dict_['roce_3ya'], 2)})?")
    past_description.append(f"Is the Return on Assets (ROA={round(dict_['roa'], 2)}) above 5% (0.05)?")

    return past_description


def get_future_checks(dict_):
    """
    Verifies company future checks.
    :param dict_: dict where we get fundamentals
    :return: company future checks in the form of list
    """

    future = list()

    # for the next us_inflation and us_low_risk_investments to be calculated automatically
    future.append(1 if dict_['net_income_growth'] > US_LOW_RISK + US_INFLATION else 0)
    # the next one needs to calculate market average growth rate in earnings
    future.append(1 if dict_['net_income_growth'] > US_NET_INCOME_GROWTH_RATE else 0)
    future.append(1 if dict_['revenue_growth'] > US_REVENUE_GROWTH_RATE else 0)
    future.append(1 if dict_['net_income_growth'] > 0.2 else 0)
    future.append(1 if dict_['revenue_growth'] > 0.2 else 0)
    future.append(1 if dict_['rating_ROE'] > 3 else 0)

    return future


def get_future_description(dict_):
    """
    Gets company future checks description.
    :param dict_: dict where we get fundamentals
    :return: description of company future checks
    """

    future_description = list()
    future_description.append(f"Is the annual growth rate in earnings ({round(dict_['net_income_growth'], 2)}) expected"
                              f" to exceed the low risk savings rate ({US_LOW_RISK}) + inflation ({US_INFLATION})?")
    future_description.append(f"Is the annual growth rate in earnings ({round(dict_['net_income_growth'], 2)}) expected"
                              f" to exceed the market average in the country of listing ({US_NET_INCOME_GROWTH_RATE})?")
    future_description.append(f"Is the annual growth rate in revenue ({round(dict_['revenue_growth'], 2)}) expected to "
                              f"exceed the market average in the country of listing ({US_REVENUE_GROWTH_RATE})?")
    future_description.append(f"Is the annual growth rate in earnings ({round(dict_['net_income_growth'], 2)}) above "
                              f"20% (0.2)?")
    future_description.append(f"Is the annual growth rate in revenue ({round(dict_['revenue_growth'], 2)}) above 20% "
                              f"(0.2)?")
    future_description.append(f"Is the Return on Equity (ROE) in 3 years expected to be over 20% "
                              f"({dict_['rating_ROE']>3})?")

    return future_description


def get_checks(fundamentals):
    """
    Gets all checks of company perspective and concatenates them with their description.
    :param fundamentals: dictionary with company fundamentals
    :return: all checks
    """

    coefficients = dict()

    # Calculating coefficients
    coefficients['value'] = dict(zip(get_value_description(fundamentals), get_value_checks(fundamentals)))
    coefficients['health'] = dict(zip(get_health_description(fundamentals), get_health_checks(fundamentals)))
    coefficients['dividends'] = dict(zip(get_dividends_description(fundamentals), get_dividends_checks(fundamentals)))
    coefficients['past'] = dict(zip(get_past_description(fundamentals), get_past_checks(fundamentals)))
    coefficients['future'] = dict(zip(get_future_description(fundamentals), get_future_checks(fundamentals)))

    return coefficients


def check_graph_and_get_recommendations(ticker):
    """
    Checks company perspective and creates a graph if necessary. Also returns analysts recommendations.
    :param ticker: stocks ticker
    :return company perspective checks
    """

    fundamentals = get_stocks_fundamentals(ticker)
    checks = get_checks(fundamentals)
    check_perspective_chart(ticker, checks)

    recommendations = get_recommendations(fundamentals)

    return checks, recommendations
