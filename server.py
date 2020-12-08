from flask import Flask, render_template
from parse import get_news

app = Flask(__name__)


@app.route("/")
def stocks_list():
    news = get_news()
    return render_template('index.html', news_list=news)


if __name__ == "__main__":
    app.run(debug=True)