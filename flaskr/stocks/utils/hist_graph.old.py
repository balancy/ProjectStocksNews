import logging
import matplotlib.pyplot as plt
import yfinance as yf
from config import CHART_FILEPATH, CHART_FILENAME


class Asset:
    def __init__(self, ticker):
        """
        Инициализируем переменную ticker
        :param ticker: Тикер запрашиваемой котировки
        """
        self.ticker = yf.Ticker(ticker)
        self.ticker_name = ticker

    def get_hist_last_1_day(self):
        """
        Получает исторические данные за 1 день по интервалу
        2 минуты для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="1d", interval="2m")
        return result["Close"]

    def get_hist_last_5_days(self):
        """
        Получает исторические данные за 5 деней по интервалу
        15 минут для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="5d", interval="15m")
        return result["Close"]

    def get_hist_last_1_month(self):
        """
        Получает исторические данные за 1 месяц по интервалу
        1 день для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="1mo", interval="1d")
        return result["Close"]

    def get_hist_last_6_months(self):
        """
        Получает исторические данные за 6 месяцев по интервалу
        1 день для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="6mo", interval="1d")
        return result["Close"]

    def get_hist_last_1_year(self):
        """
        Получает исторические данные за 1 год по интервалу
        5 дней для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="1y", interval="5d")
        return result["Close"]

    def get_hist_ytd(self):
        """
        Получает исторические данные с начала текущего года
        по интервалу 5 дней для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="ytd", interval="5d")
        return result["Close"]

    def get_hist_last_5_years(self):
        """
        Получает исторические данные за 5 лет по интервалу
        1 месяц для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="5y", interval="1mo")
        return result["Close"]

    def get_hist_all_time(self):
        """
        Получает исторические данные за все время по интервалу
        1 месяц для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.ticker.history(period="max", interval="1mo")
        return result["Close"]

    def __repr__(self):
        return f"Объект 'yfinance' с заданным тикером {self.ticker_name}"


def create_graph(ticker):
    """
    Создает последний дневной график с названием
    <Запрашиваемая_котировка>.png и сохраняет ее в основной каталог.
    График рисуется различным цветом в зависимости от текущей позиции за день.
    :param ticker: Тикер котировки по которой составляется график
    :return: Возвращает название созданной картинки
    """

    graph = Asset(ticker).get_hist_last_1_year()

    if graph[0] > graph[-1]:
        plt.plot(graph, color='red')
    else:
        plt.plot(graph, color='green')

    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.title(ticker)

    try:
        graph_name = f"{CHART_FILEPATH}{ticker}{CHART_FILENAME}"
        plt.savefig(graph_name)
    except BaseException as ex:
        logging.exception(ex)
        return "Something wrong! Read utils.log"
    return graph_name
