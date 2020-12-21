from flask import Flask, render_template
from flaskr.model import get_news, get_news_by_tickers, get_tickers
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


def scheduled_task():
    print("Every 3 seconds")


@app.before_first_request
def init_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=3, id='main_scheduled_job')
    scheduler.start()


@app.route("/")
@app.route("/index")
def stocks_list():
    news = get_news()
    return render_template('index.html', news_list=news, pagetitle="All news")


@app.route("/news_spb")
def stocks_list_spb():
    news = get_news_by_tickers()
    return render_template('index.html', news_list=news, pagetitle="SPB Tickers news")


@app.route("/tickers")
def tickers():
    _tickers = get_tickers()
    return render_template('tickers.html', tickers=_tickers)


init_scheduler()
