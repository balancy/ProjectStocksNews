from flaskr.stocks.db_interact import get_stocks_fundamentals
from flaskr.stocks.diagram import Diagram


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
    value_descr.append(f"Is the discounted cash flow value (<b>{dict_['dcf']}</b>) less than 20% of the share price "
                       f"(<b>{dict_['price']}</b>)?")
    value_descr.append(f"Is the discounted cash flow value (<b>{dict_['dcf']}</b>) less than 40% of the share price "
                       f"(<b>{dict_['price']}</b>)?")
    value_descr.append(f"Is the P/E ratio (<b>{dict_['pe_ratio']}</b>) less than the market average "
                       f"(<b>{dict_['pe_country']}</b>) but still greater than 0?")
    value_descr.append(f"Is the P/E ratio (<b>{dict_['pe_ratio']}</b>) less than the sector '{dict_['sector_name']}' average"
                       f" (<b>{dict_['pe_sector']}</b>) but still greater than 0?")
    value_descr.append(f"Is the PEG ratio (<b>{dict_['peg_ratio']}</b>) within a reasonable range (0 to 1)?")
    value_descr.append(f"Is the P/B ratio (<b>{dict_['pb_ratio']}</b>) within a reasonable range (0 to 1)?")

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
    health_descr.append(f"Are short term assets (<b>{human_format(dict_['short_term_assets'])}</b>) greater than "
                        f"short term liabilities (<b>{human_format(dict_['short_term_liabilities'])}</b>)?")
    health_descr.append(f"Are short term assets (<b>{human_format(dict_['short_term_assets'])}</b>) greater than long "
                        f"term liabilities (<b>{human_format(dict_['long_term_liabilities'])}</b>)?")
    health_descr.append(f"Has the debt to equity ratio (<b>{round(dict_['debt_equity_ratio_now'], 2)}</b>) decreased in"
                        f" the past 5 years (vs <b>{round(dict_['debt_equity_ratio_5ya'], 2)}</b>)?")
    health_descr.append(f"Is the debt to equity ratio (<b>{round(dict_['debt_equity_ratio_now'], 2)}</b>) less than 40%"
                        f" (0.4)?")
    health_descr.append(f"Are 20% of debt (<b>{human_format(dict_['total_debt'])}</b>) covered by operating cash flows "
                        f"(<b>{human_format(dict_['operating_cash_flow'])}</b>)?")
    health_descr.append(f"Are earnings greater than 5x (<b>{round(dict_['interest_coverage'], 2)}</b>) the interest on "
                        f"debt (if company pays interest at all)?")

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
    div_description.append(f"Is the current dividend yield (<b>{dict_['dividend_yield']}%</b>) higher than the sector "
                           f"'{dict_['sector_name']}' average (<b>{dict_['div_sector']}%</b>)?")
    div_description.append(f"Is the current dividend yield (<b>{dict_['dividend_yield']}%</b>) higher than the market "
                           f"average (<b>{dict_['div_country']}%</b>)?")
    div_description.append(f"Is the growth in dividends per share over the past 10 years positive "
                           f"(<b>{dict_['ten_years_dps_growth']}</b>)?")
    div_description.append(f"Has the dividend payed (<b>{human_format(dict_['dividends_paid_now'])}</b>) increased in "
                           f"the past 10 years (vs <b>{human_format(dict_['dividends_paid_10ya'])}</b>)?")
    div_description.append(f"Are dividends paid well covered by Net Profit (0 < <b>{round(dict_['payout_ratio'], 2)}</b>"
                           f" < 0.9)?")
    div_description.append(f"Is the growth in dividends per share (<b>{round(dict_['dps_growth'], 3)}</b>) over the "
                           f"past year positive?")

    return div_description


def get_past_checks(dict_):
    """
    Verifies company past checks.
    :param dict_: dict where we get fundamentals
    :return: company past checks in the form of list
    """

    past = list()

    past.append(1 if dict_['eps_g_past_5y'] > dict_['eps_g_past_5y_sector'] else 0)
    past.append(1 if dict_['eps_g_past_5y'] > 0 else 0)
    past.append(1 if dict_['eps_g_now'] > dict_['eps_g_past_5y'] else 0)
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
    past_description.append(f"Has EPS growth (<b>{round(dict_['eps_g_past_5y'], 2)}%</b>) exceeded sector "
                            f"'{dict_['sector_name']}' EPS growth (<b>{round(dict_['eps_g_past_5y_sector'], 2)}%</b>) "
                            f"over the past 5 years ?")
    past_description.append(f"Is Have Earnings Per Share growth over the past 5 years "
                            f"(<b>{dict_['eps_g_past_5y']}</b>%) positive?")
    past_description.append(f"Is the current EPS growth (<b>{round(dict_['eps_g_now'], 2)}%</b>) higher than the "
                            f"average annual growth over the past 5 years (vs <b>{round(dict_['eps_g_past_5y'], 2)}%"
                            f"</b>)?")
    past_description.append(f"Is the Return on Equity (ROE=<b>{round(dict_['roe'], 2)}</b>) higher than 20% (0.2)?")
    past_description.append(f"Has the Return on Capital Employed (ROCE=<b>{round(dict_['roce_now'], 2)}</b>) increased "
                            f"from 3 years ago (vs <b>{round(dict_['roce_3ya'], 2)}</b>)?")
    past_description.append(f"Is the Return on Assets (ROA=<b>{round(dict_['roa'], 2)}</b>) above 5% (0.05)?")

    return past_description


def get_future_checks(dict_):
    """
    Verifies company future checks.
    :param dict_: dict where we get fundamentals
    :return: company future checks in the form of list
    """

    future = list()

    future.append(1 if dict_['forward_pe'] > dict_['forward_pe_country'] else 0)
    future.append(1 if dict_['forward_pe'] > dict_['forward_pe_sector'] else 0)
    future.append(1 if dict_['eps_g_next_5y'] > dict_['eps_g_next_5y_country'] else 0)
    future.append(1 if dict_['eps_g_next_5y'] > dict_['eps_g_next_5y_sector'] else 0)
    future.append(1 if dict_['net_income_growth'] > 0.2 else 0)
    future.append(1 if dict_['revenue_growth'] > 0.2 else 0)

    return future


def get_future_description(dict_):
    """
    Gets company future checks description.
    :param dict_: dict where we get fundamentals
    :return: description of company future checks
    """

    future_description = list()
    future_description.append(f"Is the stocks forward P/E ratio (<b>{round(dict_['forward_pe'], 2)}</b>) expected to "
                              f"exceed the country forward P/E ratio (<b>{round(dict_['forward_pe_country'])}</b>)")
    future_description.append(f"Is the stocks forward P/E ratio (<b>{round(dict_['forward_pe'], 2)}</b>) expected to "
                              f"exceed the sector '{dict_['sector_name']}' forward P/E ratio "
                              f"(<b>{round(dict_['forward_pe_sector'])}</b>)")
    future_description.append(f"Is the predicted stocks EPS growth (<b>{round(dict_['eps_g_next_5y'], 2)}"
                              f"</b>) expected to exceed the predicted country EPS growth in 5 years "
                              f"(<b>{round(dict_['eps_g_next_5y_country'])}</b>)")
    future_description.append(f"Is the predicted stocks EPS growth (<b>{round(dict_['eps_g_next_5y'], 2)}</b>) expected"
                              f" to exceed the sector '{dict_['sector_name']}''s growth"
                              f" (<b>{round(dict_['eps_g_next_5y_sector'])}</b>)")
    future_description.append(f"Is the annual growth rate in earnings (<b>{round(dict_['net_income_growth'], 2)}</b>) "
                              f"above 20% (0.2)?")
    future_description.append(f"Is the annual growth rate in revenue (<b>{round(dict_['revenue_growth'], 2)}</b>) above "
                              f"20% (0.2)?")

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


def get_recommendations(dictionary):
    """
    :param dictionary: dictionary to extract recommendations
    :return: recommendations
    """
    dict_ = dict()
    dict_['Analysts recommendations'] = dictionary['analysts_recommendation']
    dict_['Overall rating'] = dictionary['analysts_score']
    dict_['Discounted cash flow rating'] = dictionary['rating_DCF']
    dict_['Return on equity rating'] = dictionary['rating_ROE']
    dict_['Return on assets rating'] = dictionary['rating_ROA']
    dict_['Price/Earnings ratio rating'] = dictionary['rating_PE']
    dict_['Price/Book ratio rating'] = dictionary['rating_PB']

    return dict_


def check_graph_and_get_recommendations(ticker):
    """
    Checks company perspective and creates a graph if necessary. Also returns analysts recommendations.
    :param ticker: stocks ticker
    :return company perspective checks
    """

    diagram = Diagram(ticker)
    fundamentals = get_stocks_fundamentals(ticker)
    checks = get_checks(fundamentals)

    if not diagram.exists():
        diagram.set_checks(checks)
        diagram.create_and_save_plot()

    recommendations = get_recommendations(fundamentals)

    return checks, recommendations
