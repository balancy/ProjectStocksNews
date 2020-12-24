from apscheduler.schedulers.background import BackgroundScheduler

from flaskr.db_handling import save_news_to_db, delete_news_from_db


def get_scheduler(app):
    """Инициализация менеджера задач
    """

    def saving_news_to_db():
        """Чтение новостей из rss ленты и сохранение их в базу данных
        """

        with app.app_context():
            save_news_to_db()

    def deleting_old_news():
        """Удаление старых новостей из базы данных
        """

        with app.app_context():
            delete_news_from_db()

    scheduler = BackgroundScheduler()
    scheduler.add_job(saving_news_to_db, 'interval', minutes=10, id='saving_job')
    scheduler.add_job(deleting_old_news, 'interval', days=2, id='deleting_job')
    scheduler.start()

    return scheduler
