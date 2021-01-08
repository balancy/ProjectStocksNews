from flask import Blueprint, render_template
from flaskr.news.parse import get_tickers
from flaskr.tickers.plot_radar_chart import create_chart_perspective

blueprint = Blueprint('ticker', __name__, url_prefix='/tickers')


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    create_chart_perspective(ticker)
    return render_template('ticker.html', pagetitle=f"Ticker {ticker}", ticker=ticker)


@blueprint.route("/")
def tickers():
    _tickers = get_tickers()
    return render_template('tickers.html', tickers=_tickers, pagetitle="Tickers")
