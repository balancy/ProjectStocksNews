from flask import Flask, render_template
from flaskr.tickers.view import blueprint as fundamentals_blueprint
from flaskr.news.view import blueprint as news_blueprint
from flaskr.tasks import get_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    app.register_blueprint(news_blueprint)
    app.register_blueprint(fundamentals_blueprint)
    get_scheduler(app)

    return app
