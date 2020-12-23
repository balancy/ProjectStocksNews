from flaskr.scripts import get_news, get_tickers
from flaskr.db_entities import db, News
from datetime import datetime, timedelta


def save_news_to_db() -> None:
    """Сохранение новостей в базу данных
    """

    all_news = get_news()
    for one_news in all_news:
        news_exists = News.query.filter(News.title == one_news['title']).count()
        if not news_exists:
            print(f"News with title '{one_news['title']}' added to DB.")
            one_news_to_db_format = News(one_news)
            db.session.add(one_news_to_db_format)
    db.session.commit()


def get_news_from_db(only_spb=False):
    """Извлечение новостей из базы данных
    """

    all_news = News.query.order_by(News.date.desc()).all()
    if only_spb:
        tickers = get_tickers()
        all_news = [elm for elm in all_news if elm.ticker and elm.ticker in tickers]
    return all_news


def delete_news_from_db() -> None:
    """Удаление старых новосте из БД
    """

    old_news = db.session.query(News).filter(News.date < datetime.now() - timedelta(days=2))
    num_old_news = old_news.count()
    old_news.delete()
    db.session.commit()
    print(f"{num_old_news} old news were deleted from the DB.")


if __name__ == "__main__":
    save_news_to_db()
    delete_news_from_db()