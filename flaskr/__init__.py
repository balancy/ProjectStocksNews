from flask import Flask, render_template
import logging
from config import BOT_LINK
from flaskr.tickers.view import blueprint as fundamentals_blueprint
from flaskr.news.view import blueprint as news_blueprint
from flaskr.tasks import get_scheduler


def create_app():
    """
    Create flask app
    :return: flask app
    """

    app = Flask(__name__)
    app.config.from_pyfile("../config.py")
    app.register_blueprint(news_blueprint)
    app.register_blueprint(fundamentals_blueprint)
    get_scheduler(app)

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Handling page not found link.
        """

        return render_template('404.html'), 404

    @app.context_processor
    def inject_bot_link():
        """
        Injecting bot url in our base.html template.
        """

        return dict(bot_link=BOT_LINK)

    logging.basicConfig(
        filename="flaskr.log", level=logging.INFO,
        format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    return app
