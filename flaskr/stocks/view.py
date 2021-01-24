from flask import Blueprint, render_template, send_from_directory
from flaskr.stocks.db_interact import get_stocks_fundamentals
from flaskr.errors.exceptions import StockNotFoundException
from flaskr.news.parse import get_tickers
from flaskr.stocks.checks_and_recommendations import check_graph, get_recommendations_for_view

blueprint = Blueprint('ticker', __name__, url_prefix='/stocks')


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    """
    Shows stocks ticker page with all needed data.
    :param ticker: company ticker
    :return: shows ticker.html
    """

    try:
        ticker = ticker.upper()
        fundamentals = get_stocks_fundamentals(ticker)
        checks = check_graph(ticker, fundamentals)
        recommendations = get_recommendations_for_view(fundamentals)
        return render_template('ticker.html',
                               pagetitle=f"{ticker}",
                               ticker=ticker,
                               fundamentals=fundamentals,
                               checks=checks,
                               recommendations=recommendations)
    except StockNotFoundException:
        return render_template('error.html', parameter="ticker")


@blueprint.route("/")
def tickers():
    """
    Shows tickers page.
    :return: shows tickers.html
    """
    _tickers = get_tickers()
    return render_template('tickers.html', tickers=_tickers, pagetitle="Tickers")


@blueprint.route("/charts/<path:path>")
def get_chart(path):
    """
    Gives access for project to the charts folder.
    :param path: path to the chart
    :return: graph
    """
    return send_from_directory("charts", path)


@blueprint.route("/diagrams/<path:path>")
def get_diagram(path):
    """
    Gives access for project to the diagrams folder.
    :param path: path to the diagram
    :return: graph
    """
    return send_from_directory("diagrams", path)
