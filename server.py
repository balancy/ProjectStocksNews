from flask import Flask, render_template
from parse import get_news

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def stocks_list():
    news = get_news()
    return render_template('index.html', news_list=news)

@app.route("/tickers")
def stocks_list_spb():
    news = list()
    return render_template('index.html', news_list=news)



if __name__ == "__main__":
    app.run(debug=True)