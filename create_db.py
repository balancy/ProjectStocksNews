from flaskr.db import Base, engine
from flaskr.tickers.model import Fundamentals, CountryFundamentals, SectorFundamentals
from flaskr.news.model import News
from flaskr.user.model import BotUser


Base.metadata.create_all(bind=engine)