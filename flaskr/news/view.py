from flask import render_template, Blueprint
from flaskr.news.db_interact import get_news_from_db

blueprint = Blueprint('/', __name__)


@blueprint.route("/")
@blueprint.route("/index")
def stocks_list():
    news = get_news_from_db()
    return render_template('index.html', news_list=news, pagetitle="All news")


@blueprint.route("/news_spb")
def stocks_list_spb():
    news = get_news_from_db(only_spb=True)
    return render_template('spb.html', news_list=news, pagetitle="SPB Tickers news")

