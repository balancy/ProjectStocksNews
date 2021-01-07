from datetime import datetime, timedelta

from flaskr.sending_bot import sending_bot
from flaskr.db import db_session
from flaskr.news.model import News
from flaskr.news.parse import get_news


def send_to_bot(news) -> None:
    """Отправка новости в бот, если она удовлетворяет условиям
    """

    if news["is_on_spb"]:
        sending_bot.format_from_json(news)
        sending_bot.send_news()


def save_news_to_db() -> None:
    """Сохранение новостей в базу данных
    """

    all_news = get_news()
    for one_news in all_news:
        first_news_in_db = News.query.filter(News.id == one_news['id']).first()

        if not first_news_in_db:
            print(f"News with title '{one_news['title']}' added to DB.")
            one_news_to_db_format = News(one_news)
            db_session.add(one_news_to_db_format)

            send_to_bot(one_news)

        elif one_news['change'] != first_news_in_db.change:
            print(f"The price of {first_news_in_db.ticker} updated")
            first_news_in_db.change = one_news['change']

    db_session.commit()


def get_news_from_db(only_spb=False):
    """Извлечение новостей из базы данных
    """

    if only_spb:
        all_news = News.query.filter(News.is_on_spb.is_(True)).order_by(News.date.desc())
    else:
        all_news = News.query.order_by(News.date.desc())
    return all_news


def delete_news_from_db() -> None:
    """Удаление старых новосте из БД
    """

    old_news = News.query.filter(News.date < datetime.now() - timedelta(days=2))
    num_old_news = old_news.count()
    for one_old_news in old_news:
        db_session.delete(one_old_news)
    db_session.commit()
    print(f"{num_old_news} old news were deleted from the DB.")
