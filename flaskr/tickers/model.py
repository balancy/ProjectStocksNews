from sqlalchemy import Column, Integer, String, Float, DateTime
from flaskr.db import Base


class Fundamentals(Base):
    __tablename__ = "fundamentals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    sector = Column(String(40), nullable=False)
    dcf = Column(Float)

    pe_ratio = Column(Float)
    peg_ratio = Column(Float)
    pb_ratio = Column(Float)

    quick_ratio = Column(Float)
    ps_ratio = Column(Float)

    short_term_liabilities = Column(Integer)
    long_term_liabilities = Column(Integer)
    short_term_assets = Column(Integer)
    long_term_assets = Column(Integer)
    debt_equity_ratio_now = Column(Float)
    debt_equity_ratio_5ya = Column(Float)
    operating_cash_flow = Column(Integer)
    total_debt = Column(Integer)
    interest_coverage = Column(Float)
    debt_growth = Column(Float)

    dividend_yield = Column(Float)
    payout_ratio = Column(Float)
    dps_growth = Column(Float)
    ten_years_dps_growth = Column(Float)

    net_income_growth = Column(Float)
    revenue_growth = Column(Float)

    growth_eps_now = Column(Float)
    growth_eps_5ya = Column(Float)
    eps_now = Column(Float)
    eps_5ya = Column(Float)
    roe = Column(Float)
    roce_now = Column(Float)
    roce_3ya = Column(Float)
    roa = Column(Float)

    analysts_rating = Column(String(5))
    analysts_score = Column(Integer)
    analysts_recommendation = Column(String(20))
    rating_DCF = Column(Integer)
    rating_ROE = Column(Integer)
    rating_ROA = Column(Integer)
    rating_DE = Column(Integer)
    rating_PE = Column(Integer)
    rating_PB = Column(Integer)

    date = Column(DateTime)

    def __init__(self, json):
        for key in json:
            setattr(self, key, json[key])

    def update(self, json):
        for key in json:
            setattr(self, key, json[key])

    def to_json(self):
        return self.__dict__

    # def __repr__(self):
    #     return f'<News {self.title} {self.url}>'
