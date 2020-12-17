from flask import Flask, render_template
from flaskr.model import get_news, get_news_by_tickers, get_tickers

app = Flask(__name__)


@app.route("/")
@app.route("/index")
@app.route("/all_news")
def stocks_list():
    news = get_news()
    return render_template('index.html', news_list=news, pagetitle="All news")


@app.route("/news_spb")
def stocks_list_spb():
    news = get_news_by_tickers()
    return render_template('index.html', news_list=news, pagetitle="SPB Tickers news")


@app.route("/tickers")
def tickers():
    tickers = get_tickers()
    return render_template('tickers.html', tickers=tickers)


if __name__ == "__main__":
    app.run(debug=True)