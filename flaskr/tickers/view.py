from flask import Blueprint, render_template, send_from_directory
from flaskr.news.parse import get_tickers
from flaskr.tickers.calculate_checks import check_graph_and_get_recommendations

blueprint = Blueprint('ticker', __name__, url_prefix='/tickers')


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    """
    Shows stocks ticker page with all needed data.
    :param ticker: company ticker
    :return: shows ticker.html
    """
    try:
        checks, recommendations = check_graph_and_get_recommendations(ticker)
    except NameError:
        return render_template('404.html', ticker=True)

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


@blueprint.route("/graphs/<path:path>")
def get_graph(path):
    """
    Gives access for project to the graphs folder.
    :param path: path to the graph
    :return: graph
    """
    return send_from_directory("graphs", path)


@blueprint.route("/static/<path:path>")
def get_image(path):
    """
    Gives access for project to the static folder.
    :param path: path to the static
    :return: static files
    """
    return send_from_directory("static", path)
