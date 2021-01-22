from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from flaskr.db import Base


class Fundamentals(Base):
    """
    Model for stocks fundamentals.
    """

    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    sector_id = Column(Integer, ForeignKey('sector_fundamentals.id'))
    country_id = Column(Integer, ForeignKey('country_fundamentals.id'))

    pe_ratio = Column(Float)
    forward_pe = Column(Float)
    peg_ratio = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    dividend_volatile = Column(Boolean)
    payout_ratio = Column(Float)
    roe = Column(Float)
    roa = Column(Float)

    debt_equity_ratio_now = Column(Float)
    debt_equity_ratio_5ya = Column(Float)
    interest_coverage = Column(Float)
    roce_now = Column(Float)
    roce_3ya = Column(Float)

    debt_growth = Column(Float)
    dps_growth = Column(Float)
    ten_years_dps_growth = Column(Float)
    net_income_growth = Column(Float)
    revenue_growth = Column(Float)
    eps_g_past_5y = Column(Float)
    eps_g_next_5y = Column(Float)
    eps_g_now = Column(Float)

    analysts_rating = Column(String(5))
    analysts_score = Column(Integer)
    analysts_recommendation = Column(String(20))
    rating_DCF = Column(Integer)
    rating_ROE = Column(Integer)
    rating_ROA = Column(Integer)
    rating_DE = Column(Integer)
    rating_PE = Column(Integer)
    rating_PB = Column(Integer)

    dcf = Column(Float)

    short_term_liabilities = Column(Integer)
    long_term_liabilities = Column(Integer)
    short_term_assets = Column(Integer)
    long_term_assets = Column(Integer)
    total_debt = Column(Integer)

    operating_cash_flow = Column(Integer)
    dividends_paid_now = Column(Float)
    dividends_paid_10ya = Column(Float)

    date = Column(DateTime)

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])

    def update(self, json):
        for key in json:
            setattr(self, key, json[key])

    def to_json(self):
        dict_ = self.__dict__
        dict_['pe_sector'] = self.sector.pe
        dict_['div_sector'] = self.sector.div_yield
        dict_['forward_pe_sector'] = self.sector.forward_pe
        dict_['eps_g_next_5y_sector'] = self.sector.eps_g_next_5y
        dict_['eps_g_past_5y_sector'] = self.sector.eps_g_past_5y
        dict_['pe_country'] = self.country.pe
        dict_['div_country'] = self.country.div_yield
        dict_['forward_pe_country'] = self.country.forward_pe
        dict_['eps_g_next_5y_country'] = self.country.eps_g_next_5y
        dict_['eps_g_past_5y_country'] = self.country.eps_g_past_5y
        dict_['sector_name'] = self.sector.name
        return dict_



class SectorFundamentals(Base):
    """
    Model for sector fundamentals.
    """

    __tablename__ = "sector_fundamentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pe = Column(Float)
    div_yield = Column(Float)
    date = Column(DateTime)
    forward_pe = Column(Float)
    eps_g_past_5y = Column(Float)
    eps_g_next_5y = Column(Float)
    stocks = relationship("Fundamentals", backref="sector")

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])

    def update(self, json):
        for key in json:
            setattr(self, key, json[key])

    def to_json(self):
        return self.__dict__


class CountryFundamentals(Base):
    """
    Model for country fundamentals.
    """

    __tablename__ = "country_fundamentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pe = Column(Float)
    div_yield = Column(Float)
    forward_pe = Column(Float)
    eps_g_past_5y = Column(Float)
    eps_g_next_5y = Column(Float)
    date = Column(DateTime)
    stocks = relationship("Fundamentals", backref="country")

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])

    def update(self, json):
        for key in json:
            setattr(self, key, json[key])

    def to_json(self):
        return self.__dict__
