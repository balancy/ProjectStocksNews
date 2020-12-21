import os
basedir = os.path.abspath(os.path.dirname(__file__))

TICKERS_FILENAME = "flaskr/static/data/tickers.json"
RSS_URL = "https://www.marketwatch.com/markets?mod=top_nav"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "flaskr.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
