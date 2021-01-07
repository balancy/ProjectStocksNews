from sqlalchemy import Column, Integer, String, Boolean, DateTime
from flaskr.db import Base


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    summary = Column(String)
    ticker = Column(String(10))
    change = Column(Integer)
    date = Column(DateTime, nullable=False)
    author = Column(String(120))
    is_on_spb = Column(Boolean)

    def __init__(self, json):
        self.id = json['id']
        self.title = json['title']
        self.url = json['url']
        self.summary = json.get('summary', '')
        self.ticker = json.get('ticker', '')
        self.change = json.get('change', '')
        self.date = json['date']
        self.author = json.get('author', '')
        self.is_on_spb = json.get('is_on_spb', '')

    def to_json(self):
        return {'title': self.title, 'url': self.url, 'summary': self.summary,
                'date': self.date, 'ticker': self.ticker, 'change': self.change,
                'author': self.author, 'is_on_spb': self.is_on_spb, 'id': self.id}

    def __repr__(self):
        return f'<News {self.title} {self.url}>'
