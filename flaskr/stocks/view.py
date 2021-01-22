from flask import Blueprint, render_template, send_from_directory
import logging
from flaskr.news.parse import get_tickers
from flaskr.stocks.calculate_checks import check_graph_and_get_recommendations

blueprint = Blueprint('ticker', __name__, url_prefix='/stocks')


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    """
    Shows stocks ticker page with all needed data.
    :param ticker: company ticker
    :return: shows ticker.html
    """
    try:
        checks, recommendations = check_graph_and_get_recommendations(ticker.upper())
    except TimeoutError:
        logging.info(f"Timeout error during parsing {ticker} info from Finviz.")
        return render_template('error.html', parameter="timeout")
    except ConnectionError:
        logging.info(f"Connection error during parsing {ticker} info from Finviz.")
        return render_template('error.html', parameter="connection")
    except IndexError:
        logging.info(f"There is no such ticker {ticker} found on Finviz.")
        return render_template('error.html', parameter="ticker")

    return render_template('ticker.html', pagetitle=f"Ticker {ticker}", ticker=ticker, checks=checks,
                           recommendations=recommendations)


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


@blueprint.route("/static/<path:path>")
def get_image(path):
    """
    Gives access for project to the static folder.
    :param path: path to the static
    :return: static files
    """
    return send_from_directory("static", path)
