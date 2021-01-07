from flask import Blueprint, render_template
from flaskr.news.parse import get_tickers

blueprint = Blueprint('ticker', __name__)


@blueprint.route('/<ticker>')
def ticker_fundamentals(ticker):
    return ticker


@blueprint.route("/tickers")
def tickers():
    _tickers = get_tickers()
    return render_template('tickers.html', tickers=_tickers, pagetitile="Tickers")
