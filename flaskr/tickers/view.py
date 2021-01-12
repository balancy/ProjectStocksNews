from flask import Blueprint, render_template, send_from_directory
from flaskr.news.parse import get_tickers
from flaskr.tickers.calculate_checks import get_checks
from flaskr.tickers.checks_description import CHECKS_DESCR
from flaskr.tickers.db_interact import get_fundamentals
from flaskr.tickers.extract_fundamentals import get_recommendations
from flaskr.tickers.plot_radar_chart import check_perspective_chart

blueprint = Blueprint('ticker', __name__, url_prefix='/tickers')


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    fundamentals = get_fundamentals(ticker)
    checks = get_checks(fundamentals)
    check_perspective_chart(ticker, checks)
    recommendations = get_recommendations(fundamentals)
    return render_template('ticker.html', pagetitle=f"Ticker {ticker}", ticker=ticker, checks=checks,
                           recommendations=recommendations, checks_descr=CHECKS_DESCR)


@blueprint.route("/")
def tickers():
    _tickers = get_tickers()
    return render_template('tickers.html', tickers=_tickers, pagetitle="Tickers")


@blueprint.route("/graphs/<path:path>")
def get_graph(path):
    return send_from_directory("graphs", path)


@blueprint.route("/static/<path:path>")
def get_image(path):
    return send_from_directory("static", path)
