from datetime import datetime, timedelta

from flaskr.bot import bot
from flaskr.db_entities import db, News
from flaskr.parse_news import get_news


def send_to_bot(news) -> None:
    """Отправка новости в бот, если она удовлетворяет условиям
    """

    if news["is_on_spb"]:
        bot.format_from_json(news)
        bot.send_news()


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

            send_to_bot(one_news)
    db.session.commit()


def get_news_from_db(only_spb=False):
    """Извлечение новостей из базы данных
    """

    if only_spb:
        all_news = News.query.filter(News.is_on_spb.is_(True)).order_by(News.date.desc()).all()
    else:
        all_news = News.query.order_by(News.date.desc()).all()
    return all_news


def delete_news_from_db() -> None:
    """Удаление старых новосте из БД
    """

    old_news = db.session.query(News).filter(News.date < datetime.now() - timedelta(days=2))
    num_old_news = old_news.count()
    old_news.delete()
    db.session.commit()
    print(f"{num_old_news} old news were deleted from the DB.")
