from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from flaskr.db_handling import save_news_to_db


def get_scheduler(app):
    """Initializing task manager.
    """

    def scheduled_task():
        """Reading from the rss and saving news to db
        """

        print(f"Reading rss: {datetime.now()}")
        with app.app_context():
            save_news_to_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_task, 'interval', seconds=600, id='main_scheduled_job')
    scheduler.start()

    return scheduler
