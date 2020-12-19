import yfinance as yf


class Asset:

    def __init__(self, tiker):
        """
        Инициализируем переменную tiker
        """
        self.tiker = yf.Ticker(tiker)

    def get_hist_last_1_day(self):
        """
        Получает исторические данные за 1 день по интервалу 2 минуты для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1d", interval="2m")
        return result["Close"]

    def get_hist_last_5_days(self):
        """
        Получает исторические данные за 5 деней по интервалу 15 минуты для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="5d", interval="15m")
        return result["Close"]

    def get_hist_last_1_month(self):
        """
        Получает исторические данные за 1 месяц по интервалу 1 день для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1mo", interval="1d")
        return result["Close"]

    def get_hist_last_6_months(self):
        """
        Получает исторические данные за 6 месяцев по интервалу 1 день для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="6mo", interval="1d")
        return result["Close"]

    def get_hist_last_1_year(self):
        """
        Получает исторические данные за 1 год по интервалу 5 дней для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1y", interval="5d")
        return result["Close"]

    def get_hist_ytd(self):
        """
        Получает исторические данные с начала текущего года по интервалу 5 дней для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="ytd", interval="5d")
        return result["Close"]

    def get_hist_last_5_years(self):
        """
        Получает исторические данные за 5 лет по интервалу 1 месяц для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="5y", interval="1mo")
        return result["Close"]

    def get_hist_all_time(self):
        """
        Получает исторические данные за все время по интервалу 1 месяц для заданного тикера
        :param tiker: Тикер запрашиваемой котировки
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="max", interval="1mo")
        return result["Close"]

    def __repr__(self):
        return "Объект 'yfinance' с заданным тикером"


if __name__ == "__main__":
    test = Asset("TSLA")

    print(test.get_hist_last_1_day())

    print(test)