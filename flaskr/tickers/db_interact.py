from datetime import datetime

from flaskr.db import db_session
from flaskr.tickers.extract_fundamentals import extract_fundamentals
from flaskr.tickers.model import Fundamentals


def get_data_from_bd(ticker):
    """Gets fundamentals from db
    """

    data = Fundamentals.query.filter(Fundamentals.ticker == ticker).first()
    return data.to_json()


def get_fundamentals(ticker):
    """Verifies if record on this day is already in database. If not, extracts this data to db and return it.
    If yes, return it.
    """

    time_now = datetime.today()
    ticker_in_db = Fundamentals.query.filter(Fundamentals.ticker == ticker).first()
    if ticker_in_db:
        is_data_actual = ticker_in_db.date.day == time_now.day
        if is_data_actual:
            # if we have already fundamentals of this ticker for this day
            return get_data_from_bd(ticker)
        else:
            # if we don't have yet fundamentals of this ticker for this day
            data_json = extract_fundamentals(ticker)
            ticker_in_db.update(data_json)
    else:
        # if we don't have this ticker in out DB yet
        data_json = extract_fundamentals(ticker)
        data_to_db_format = Fundamentals(data_json)
        db_session.add(data_to_db_format)
    db_session.commit()

    return data_json
