from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from flaskr.db import Base


class Fundamentals(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String(40), nullable=False)

    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    pb_ratio = Column(Float)
    dividend_yield = Column(Float)
    dividend_volatile = Column(Boolean)
    payout_ratio = Column(Float)
    roe = Column(Float)
    roa = Column(Float)

    # TODO - make 2 new tables
    pe_sector = Column(Float)
    pe_country = Column(Float)
    div_sector = Column(Float)
    div_country = Column(Float)

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
    growth_eps_now = Column(Float)
    growth_eps_5ya = Column(Float)

    eps_now = Column(Float)
    eps_5ya = Column(Float)

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
        return self.__dict__
