from datetime import datetime, timedelta
import pandas_market_calendars as mcal
from pytz import timezone
import pytz


class WorkTime:

    def __init__(self, zone):
        """
        Инициализируем переменные
        В этой библиотеке нет календаря на московскую биржу. Не думаю что ее нужно добавлять.
        Допилить москву
        """
        self.stock_market = mcal.get_calendar('NYSE')
        self.start_date = datetime.now()
        self.delta = timedelta(days=5)
        self.end_date = self.start_date + self.delta
        self.fmt = "%H:%M:%S %Z%z"
        self.utc = pytz.utc
        self.zone = zone

    def get_time_closing(self):
        """
        :return: Возвращает ближайшее время закрытия биржи
        """
        self.__to_datetime_close()
        return self.__df_to_time(self.zone)

    def get_time_opening(self):
        """
        :return: Возвращает ближайшее время орткрытия биржи
        """
        self.__to_datetime_open()
        return self.__df_to_time(self.zone)

    def __df_to_time(self, zone):
        """
        Обрабатывает данные и возвращает время
        :param zone: Часовая зона
        :return: Возвращает ближайшее время орткрытия биржи NYSE по указанной часовой зоне
        """
        time = str(self.received_time).replace("+00:00", '')
        self.time_datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.time_utc = self.utc.localize(self.time_datetime)
        self.time = self.__change_tz(timezone(zone))
        return self.time

    def __to_datetime_open(self):
        """
        Получает первый ближайший рабочий день биржи с датой открытия
        """
        self.received_time = self.stock_market.schedule(self.start_date, self.end_date)['market_open'][0]

    def __to_datetime_close(self):
        """
        Получает первый ближайший рабочий день биржи с датой закрытия
        """
        self.received_time = self.stock_market.schedule(self.start_date, self.end_date)['market_close'][0]

    def __change_tz(self, time_zones):
        """
        Преобразует временную зону на полученную.
        :param time_zones: Часовая зона
        :return: Возвращает datetime обект с изменненой временной зоной
        """
        self.time = self.time_utc.astimezone(time_zones)
        return self.time

    def __repr__(self):
        return f"Время работы бири NYSE с {self.get_time_opening()} по {self.get_time_closing()}"


if __name__ == "__main__":
    test = WorkTime('Europe/Moscow')

    print(test.get_time_opening())
    print(test.get_time_closing())
