from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from flaskr.news.db_interact import save_news_to_db, delete_news_from_db
from flaskr.news.parse import get_news


def get_scheduler(app):
    """
    Task scheduler initialisation.
    :param app: flask app to work with
    :return: task scheduler
    """

    def saving_news_to_db() -> None:
        """
        Task or saving parsed news to DB.
        """

        with app.app_context():
            all_news = get_news()
            save_news_to_db(all_news)

    def deleting_old_news() -> None:
        """
        Task of deleting news from DB.
        """

        with app.app_context():
            delete_news_from_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(saving_news_to_db, 'interval', next_run_time=datetime.now(), minutes=10, id='saving_news_job')
    scheduler.add_job(deleting_old_news, 'interval', next_run_time=datetime.now(), days=2, id='deleting_news_job')
    scheduler.start()

    return scheduler
