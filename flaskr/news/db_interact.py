from datetime import datetime, timedelta
import logging

from flaskr.sending_bot import sending_bot
from flaskr.db import db_session
from flaskr.news.model import News


def send_to_bot(news) -> None:
    """
    Sending news to the bot if flag is_on_spb is True
    :param news: all news
    :return: no return
    """

    if news["is_on_spb"]:
        sending_bot.format_from_json(news)
        sending_bot.send_news()


def save_news_to_db(all_news) -> None:
    """
    Saving news to the DB.
    :param all_news: all news
    :return: no return
    """

    for one_news in all_news:
        first_news_in_db = News.query.filter(News.title == one_news['title']).first()

        if not first_news_in_db:
            logging.info(f"News with title '{one_news['title']}' added to DB.")
            db_session.add(News(one_news))
            send_to_bot(one_news)

        elif one_news['change'] != first_news_in_db.change:
            logging.info(f"The price of {first_news_in_db.ticker} updated")
            first_news_in_db.change = one_news['change']

    db_session.commit()


def get_news_from_db(only_spb=False):
    """
    Gets news from DB.
    :param only_spb: flag, if True, returns only news with this flag
    :return: news from DB
    """

    if only_spb:
        all_news = News.query.filter(News.is_on_spb.is_(True)).order_by(News.date.desc())
    else:
        all_news = News.query.order_by(News.date.desc())
    return all_news


def delete_news_from_db() -> None:
    """
    Deleting news older than 2 days from DB
    :return: no return
    """

    old_news = News.query.filter(News.date < (datetime.now() - timedelta(days=2)))
    num_old_news = old_news.count()
    for one_old_news in old_news:
        db_session.delete(one_old_news)
    db_session.commit()

    logging.info(f"{num_old_news} old news were deleted from the DB.")
