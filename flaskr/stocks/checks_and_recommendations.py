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
    value_descr.append(f"Discounted cash flow value (<b>{dict_['dcf']}</b>) < 20% of the share price "
                       f"(<b>{dict_['price']}</b>)?")
    value_descr.append(f"Discounted cash flow value (<b>{dict_['dcf']}</b>) < 40% of the share price "
                       f"(<b>{dict_['price']}</b>)?")
    value_descr.append(f"P/E ratio (<b>{dict_['pe_ratio']}</b>) < P/E ratio of the market "
                       f"(<b>{dict_['pe_country']}</b>) but still > 0?")
    value_descr.append(f"P/E ratio (<b>{dict_['pe_ratio']}</b>) < P/E ratio of the '{dict_['sector_name']}'"
                       f" (<b>{dict_['pe_sector']}</b>) but still > 0?")
    value_descr.append(f"PEG ratio (<b>{dict_['peg_ratio']}</b>) within a reasonable range (0 to 1)?")
    value_descr.append(f"P/B ratio (<b>{dict_['pb_ratio']}</b>) within a reasonable range (0 to 1)?")

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
    health_descr.append(f"Short term assets (<b>{human_format(dict_['short_term_assets'])}</b>) > "
                        f"short term liabilities (<b>{human_format(dict_['short_term_liabilities'])}</b>)?")
    health_descr.append(f"Short term assets (<b>{human_format(dict_['short_term_assets'])}</b>) > long "
                        f"term liabilities (<b>{human_format(dict_['long_term_liabilities'])}</b>)?")
    health_descr.append(f"Debt to equity ratio now (<b>{round(dict_['debt_equity_ratio_now'], 2)}</b>) <"
                        f" 5 years ago (<b>{round(dict_['debt_equity_ratio_5ya'], 2)}</b>)?")
    health_descr.append(f"Debt to equity ratio (<b>{round(dict_['debt_equity_ratio_now'], 2)}</b>) < 0.4 (40%)?")
    health_descr.append(f"20% of debt (<b>{human_format(dict_['total_debt'])}</b>) covered by operating cash flows "
                        f"(<b>{human_format(dict_['operating_cash_flow'])}</b>)?")
    health_descr.append(f"Earnings/Interest on debt (<b>{round(dict_['interest_coverage'], 2)}</b>) > 5 "
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
    div_description.append(f"Current dividend yield (<b>{dict_['dividend_yield']}%</b>) > the "
                           f"'{dict_['sector_name']}' average (<b>{dict_['div_sector']}%</b>)?")
    div_description.append(f"Current dividend yield (<b>{dict_['dividend_yield']}%</b>) > the market "
                           f"average (<b>{dict_['div_country']}%</b>)?")
    div_description.append(f"Growth in dividends per share over the past 10 years "
                           f"(<b>{dict_['ten_years_dps_growth']}%</b>) > 0?")
    div_description.append(f"Dividend payed now (<b>{human_format(dict_['dividends_paid_now'])}</b>) > "
                           f" 10 years ago (vs <b>{human_format(dict_['dividends_paid_10ya'])}</b>)?")
    div_description.append(f"Dividends paid well covered by Net Profit (0 < <b>{round(dict_['payout_ratio'], 2)}</b>"
                           f" < 0.9)?")
    div_description.append(f"Growth in dividends per share (<b>{round(dict_['dps_growth'], 3)}%</b>) over the "
                           f"past year > 0?")

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
    past_description.append(f"EPS growth (<b>{round(dict_['eps_g_past_5y'], 2)}%</b>) > "
                            f"'{dict_['sector_name']}' EPS growth (<b>{round(dict_['eps_g_past_5y_sector'], 2)}%</b>) "
                            f"(bot over the past 5 years)?")
    past_description.append(f"Earnings Per Share growth over the past 5 years "
                            f"(<b>{dict_['eps_g_past_5y']}</b>%) > 0?")
    past_description.append(f"Current EPS growth (<b>{round(dict_['eps_g_now'], 2)}%</b>) > the average EPS growth "
                            f"over the past 5 years (vs <b>{round(dict_['eps_g_past_5y'], 2)}%</b>)?")
    past_description.append(f"Return on Equity (ROE=<b>{round(dict_['roe'], 2)}</b>) > 0.2 (20%)?")
    past_description.append(f"Return on Capital Employed now (<b>{round(dict_['roce_now'], 2)}</b>) > "
                            f"3 years ago (<b>{round(dict_['roce_3ya'], 2)}</b>)?")
    past_description.append(f"Return on Assets (ROA=<b>{round(dict_['roa'], 2)}</b>) > 0.05 (5%)?")

    return past_description


def get_future_checks(dict_):
    """
    Verifies company future checks.
    :param dict_: dict where we get fundamentals
    :return: company future checks in the form of list
    """

    future = list()

    future.append(1 if dict_['forward_pe'] < dict_['forward_pe_country'] else 0)
    future.append(1 if dict_['forward_pe'] < dict_['forward_pe_sector'] else 0)
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
    future_description.append(f"Forward P/E ratio (<b>{round(dict_['forward_pe'], 2)}</b>) expected to be "
                              f"< forward P/E ratio of the market (<b>{round(dict_['forward_pe_country'])}</b>)")
    future_description.append(f"Forward P/E ratio (<b>{round(dict_['forward_pe'], 2)}</b>) expected to be "
                              f"< forward P/E ratio of the '{dict_['sector_name']}'"
                              f"(<b>{round(dict_['forward_pe_sector'])}</b>)")
    future_description.append(f"EPS growth (<b>{round(dict_['eps_g_next_5y'], 2)}%</b>) "
                              f"expected to be > EPS growth of the market "
                              f"(<b>{round(dict_['eps_g_next_5y_country'])}%</b>) (both in 5 years)")
    future_description.append(f"EPS growth (<b>{round(dict_['eps_g_next_5y'], 2)}%</b>) expected to be "
                              f"> EPS growth of the '{dict_['sector_name']}' "
                              f" (<b>{round(dict_['eps_g_next_5y_sector'])}%</b>) (both in 5 years)")
    future_description.append(f"Annual growth rate in earnings (<b>{round(dict_['net_income_growth'], 2)}%</b>) > 0.2 "
                              f"(20%)?")
    future_description.append(f"Annual growth rate in revenue (<b>{round(dict_['revenue_growth'], 2)}%</b>) > 0.2 "
                              f"(20%)?")

    return future_description


def get_checks(fundamentals):
    """
    Gets all checks of company perspective and concatenates them with their description.
    :param fundamentals: stock fundamentals
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


def get_recommendations_for_view(fundamentals):
    """
    Get analysts recommendations.
    :param fundamentals: fundamentals
    :return: recommendations
    """

    if fundamentals:
        dict_ = dict()
        dict_['Analysts recommendations'] = fundamentals['analysts_recommendation']
        dict_['Overall rating'] = fundamentals['analysts_score']
        dict_['Discounted cash flow rating'] = fundamentals['rating_DCF']
        dict_['Return on equity rating'] = fundamentals['rating_ROE']
        dict_['Return on assets rating'] = fundamentals['rating_ROA']
        dict_['Price/Earnings ratio rating'] = fundamentals['rating_PE']
        dict_['Price/Book ratio rating'] = fundamentals['rating_PB']

        return dict_
    return dict()


def check_graph(ticker, fundamentals):
    """
    Checks company perspective and creates a graph if necessary.
    :param ticker: stock ticker
    :param fundamentals: stock fundamentals
    :return company perspective checks
    """

    diagram = Diagram(ticker)

    if fundamentals:
        checks = get_checks(fundamentals)

        if not diagram.exists():
            diagram.set_checks(checks)
            diagram.create_and_save_plot()

        return checks
    return dict()
