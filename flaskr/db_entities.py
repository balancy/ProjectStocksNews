from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    ticker = db.Column(db.String)
    change = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)
    author = db.Column(db.String)
    is_on_spb = db.Column(db.Boolean)

    def __init__(self, json):
        self.title = json['title']
        self.url = json['url']
        self.summary = json['summary']
        self.ticker = json['ticker']
        self.change = json['change']
        self.date = json['date']
        self.author = json['author']
        self.is_on_spb = json['is_on_spb']

    def to_json(self):
        return {'title': self.title, 'url': self.url, 'summary': self.summary,
                'date': self.date, 'ticker': self.ticker, 'change': self.change,
                'author': self.author, 'is_on_spb': self.is_on_spb}

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)
