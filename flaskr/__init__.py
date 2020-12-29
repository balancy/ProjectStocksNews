from flask import Flask, render_template
from flaskr.db_news_interact import get_news_from_db
from flaskr.parse_news import get_tickers
from flaskr.tasks import get_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    get_scheduler(app)

    @app.route("/")
    @app.route("/index")
    def stocks_list():
        pass
        news = get_news_from_db()
        return render_template('index.html', news_list=news, pagetitle="All news")

    @app.route("/news_spb")
    def stocks_list_spb():
        pass
        news = get_news_from_db(only_spb=True)
        return render_template('spb.html', news_list=news, pagetitle="SPB Tickers news")

    @app.route("/tickers")
    def tickers():
        _tickers = get_tickers()
        return render_template('tickers.html', tickers=_tickers, pagetitile="Tickers")

    return app
