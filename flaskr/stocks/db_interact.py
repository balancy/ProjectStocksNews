from datetime import datetime
import logging
from sqlalchemy import exc

from flaskr.db import db_session
from flaskr.stocks.extract_fundamentals import extract_fundamentals
from flaskr.stocks.extract_from_finviz import get_finviz_sector_country
from flaskr.stocks.model import Fundamentals, CountryFundamentals, SectorFundamentals


def get_country_sector_from_db(type_, name):
    """
    Gets country or sector record from DB.
    :param type_: 'country' or 'sector'
    :param name: name of 'country' or 'sector'
    :return: DB record
    """

    if type_ == "country":
        data = CountryFundamentals.query.filter(CountryFundamentals.name == name).first()
    else:
        data = SectorFundamentals.query.filter(SectorFundamentals.name == name).first()
    return data


def create_and_get_country_sector_db_record(type_, dict_):
    """
    Creates a country or sector record in DB.
    :param type_: 'country' or 'sector'
    :param dict_: dictionary with all needed fundamentals on country and sector
    :return: added DB record
    """

    time_now = datetime.today()
    data_json = {'name': dict_[type_], 'pe': dict_[f'pe_{type_}'], 'div_yield': dict_[f'div_{type_}'],
                 'date': time_now}
    if type_ == "country":
        record_in_db = CountryFundamentals(data_json)
    else:
        record_in_db = SectorFundamentals(data_json)

    db_session.add(record_in_db)
    try:
        db_session.commit()
        logging.info(f"{type_} {record_in_db.name} was added to DB.")
        return record_in_db
    except exc.SQLAlchemyError:
        logging.info(f"Failed to add {type} fundamentals to DB.")
        return False


def update_and_get_country_sector_db_record(record_in_db, type_, dict_):
    """
    Updates a country or sector record in DB.
    :param record_in_db: record in DB to update
    :param type_: 'country' or 'sector'
    :param dict_: dictionary with all needed fundamentals on country and sector
    :return: updated DB record
    """

    time_now = datetime.today()
    data_json = {'name': dict_[type_], 'pe': dict_[f'pe_{type_}'], 'div_yield': dict_[f'div_{type_}'],
                 'date': time_now}
    record_in_db.update(data_json)
    try:
        db_session.commit()
        logging.info(f"{type_} {record_in_db.name} was updated in DB.")
        return record_in_db
    except exc.SQLAlchemyError:
        logging.info(f"Failed to update {type} fundamentals in DB.")
        return False


def get_actual_country_sector_fundamentals_from_db(type_, dict_):
    """
    Verifies if country or sector records on this day are already in database. If not, add or update this data in db
    and return it. If True, return it.
    :param type_: 'country' or 'sector'
    :param dict_: dictionary with all needed fundamentals on country and sector
    :return: Db record
    """

    time_now = datetime.today()
    record_in_db = get_country_sector_from_db(type_, dict_[type_])

    if record_in_db:
        # if we have a record on country of sector fundamentals in DB
        if record_in_db.date.day != time_now.day:
            # if we don't have country or sector fundamentals in DB for this day
            record_in_db = update_and_get_country_sector_db_record(record_in_db, type_, dict_)
    else:
        record_in_db = create_and_get_country_sector_db_record(type_, dict_)

    return record_in_db


def get_stocks_from_db(ticker):
    """
    Gets stocks record from db.
    :param ticker: stocks ticker such as 'AAPL', 'FB', 'MSFT'
    :return: DB record
    """

    data = Fundamentals.query.filter(Fundamentals.ticker == ticker).first()
    return data


def create_and_get_stocks_db_record(ticker):
    """
    Creates a stocks record in DB.
    :param ticker: stocks ticker
    :return: added DB record
    """

    data_json = extract_fundamentals(ticker)
    ticker_in_db = Fundamentals(data_json)

    country_sector = get_finviz_sector_country(ticker)
    ticker_in_db.country = get_actual_country_sector_fundamentals_from_db("country", country_sector)
    ticker_in_db.sector = get_actual_country_sector_fundamentals_from_db("sector", country_sector)

    db_session.add(ticker_in_db)
    try:
        db_session.commit()
        logging.info(f"Stocks ticker {ticker} was added to DB.")
        return ticker_in_db
    except exc.SQLAlchemyError:
        logging.info(f"Failed to add {ticker} fundamentals to DB.")
        return False


def update_and_get_stocks_db_record(ticker_in_db):
    """
    Updates a stocks record in DB.
    :param ticker_in_db: DB record to update
    :return: updated DB record
    """

    data_json = extract_fundamentals(ticker_in_db.ticker)
    ticker_in_db.update(data_json)

    country_sector = get_finviz_sector_country(ticker_in_db.ticker)
    ticker_in_db.country = get_actual_country_sector_fundamentals_from_db("country", country_sector)
    ticker_in_db.sector = get_actual_country_sector_fundamentals_from_db("sector", country_sector)

    try:
        db_session.commit()
        logging.info(f"Stocks ticker {ticker_in_db.ticker} was updated in DB.")
        return ticker_in_db
    except exc.SQLAlchemyError:
        logging.info(f"Failed to update {ticker_in_db.ticker} fundamentals in DB.")
        return False


def get_stocks_fundamentals(ticker):
    """
    Verifies if stocks record on this day is already in database. If not, add and update this data to db and return it.
    If True, return it.
    :param ticker: stocks ticker
    :return: Db record in form of dictionary
    """

    time_now = datetime.today()
    ticker_in_db = Fundamentals.query.filter(Fundamentals.ticker == ticker).first()

    if ticker_in_db:
        # if we have a record on stocks fundamentals id DB
        if ticker_in_db.date.day != time_now.day:
            # if we don't have stocks fundamentals in DB for this day
            ticker_in_db = update_and_get_stocks_db_record(ticker_in_db)
    else:
        ticker_in_db = create_and_get_stocks_db_record(ticker)

    return ticker_in_db.to_json()
