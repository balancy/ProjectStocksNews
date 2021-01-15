import os
basedir = os.path.abspath(os.path.dirname(__file__))

# tickers and rss_url
TICKERS_FILENAME = "flaskr/static/data/tickers.json"
RSS_URL = "https://www.marketwatch.com/markets?mod=top_nav"

# db uri
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "", "flaskr.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# bot
BOT_API_KEY = "your telegram bot api key"
BOT_LINK = "your telegram bot link"

# financial api
FINANCIAL_API_KEY = "your financialmodelingprep api key"
FINANCIAL_BASE_URL = "https://financialmodelingprep.com/api/v3/"

# finviz
FINVIZ_URL_BASE = "https://finviz.com/quote.ashx?t="
FINVIZ_URL_GROUP = "https://finviz.com/groups.ashx?g="
FINVIZ_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88'
                  ' Safari/537.36'
}

# yahoo finance
YF_URL = "https://finance.yahoo.com/quote/"
