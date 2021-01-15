from flask import render_template, Blueprint, send_from_directory
from flaskr.news.db_interact import get_news_from_db

blueprint = Blueprint('/', __name__)


@blueprint.route("/")
@blueprint.route("/index")
def stocks_list():
    """
    Gets news from db and shows it in the frontend.
    :return: shows index.html
    """
    news = get_news_from_db()
    return render_template('index.html', news_list=news, pagetitle="All news")


@blueprint.route("/news_spb")
def stocks_list_spb():
    """
    Gets news from db with the flag 'is_on_spb"=True and shows it in the frontend.
    :return: shows spb.html
    """
    news = get_news_from_db(only_spb=True)
    return render_template('spb.html', news_list=news, pagetitle="SPB Tickers news")


@blueprint.route("/news_spb/static/<path:path>")
def get_image(path):
    """
    Makes path to the graph visible to the project.
    :param path: path to the graph
    :return: graph
    """
    return send_from_directory("static", path)
