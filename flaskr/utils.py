
import logging
import matplotlib.pyplot as plt
import yfinance as yf

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger_handler = logging.FileHandler('utils.log')
# logger_handler.setLevel(logging.WARNING)
logger_handler.setLevel(logging.INFO)
logger_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)


class Asset:

    def __init__(self, tiker):
        """
        Инициализируем переменную tiker
        :param tiker: Тикер запрашиваемой котировки
        """
        self.tiker = yf.Ticker(tiker)
        self.tiker_name = tiker

    def get_hist_last_1_day(self):
        """
        Получает исторические данные за 1 день по интервалу
        2 минуты для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1d", interval="2m")
        return result["Close"]

    def get_hist_last_5_days(self):
        """
        Получает исторические данные за 5 деней по интервалу
        15 минут для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="5d", interval="15m")
        return result["Close"]

    def get_hist_last_1_month(self):
        """
        Получает исторические данные за 1 месяц по интервалу
        1 день для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1mo", interval="1d")
        return result["Close"]

    def get_hist_last_6_months(self):
        """
        Получает исторические данные за 6 месяцев по интервалу
        1 день для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="6mo", interval="1d")
        return result["Close"]

    def get_hist_last_1_year(self):
        """
        Получает исторические данные за 1 год по интервалу
        5 дней для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="1y", interval="5d")
        return result["Close"]

    def get_hist_ytd(self):
        """
        Получает исторические данные с начала текущего года
        по интервалу 5 дней для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="ytd", interval="5d")
        return result["Close"]

    def get_hist_last_5_years(self):
        """
        Получает исторические данные за 5 лет по интервалу
        1 месяц для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="5y", interval="1mo")
        return result["Close"]

    def get_hist_all_time(self):
        """
        Получает исторические данные за все время по интервалу
        1 месяц для заданного тикера
        :return: Возвращает Pandas DataFrame колонка "Close"
        """
        result = self.tiker.history(period="max", interval="1mo")
        return result["Close"]

    def get_trailingPE(self):
        """
        :return: Возвращает значение P/E
        """
        return self.tiker.info['trailingPE']

    def get_enterpriseToEbitda(self):
        """
        :return: Возвращает значение EV/EBITDA
        """
        return self.tiker.info['enterpriseToEbitda']

    def get_priceToBook(self):
        """
        :return: Возвращает значение P/B
        """
        return self.tiker.info['priceToBook']

    def get_forwardEps(self):
        """
        :return: Возвращает значение EPS
        """
        return self.tiker.info['forwardEps']

    def get_priceToSalesTrailing12Months(self):
        """
        :return: Возвращает значение P/S
        """
        return self.tiker.info['priceToSalesTrailing12Months']

    def __repr__(self):
        return f"Объект 'yfinance' с заданным тикером {self.tiker_name}"


def create_graph(tiker):
    """
    Создает последний дневной график с названием <Запрашиваемая_котировка>.png и сохраняет ее в основной каталог.
    График рисуется различным цветом в зависимости от текущей позиции за день.
    :param tiker: Тикер котировки по которой составляется график
    :return: Возвращает название созданной картинки
    """
    logging.info("Выполняется create_graph")
    graph = Asset(tiker).get_hist_last_1_day()

    if graph[0] > graph[-1]:
        plt.plot(graph, color='red')
    else:
        plt.plot(graph, color='green')

    plt.xlabel('Time')
    plt.ylabel('Price')

    try:
        graph_name = str(tiker) + ".png"
        plt.savefig(graph_name)
    except BaseException as ex:
        logger.exception(ex)
        return "Something wrong! Read utils.log"
    return graph_name


if __name__ == "__main__":
    test = Asset("TSLA")

    # print(test.get_hist_last_1_day())
    print(test)
    print(type(test))

    print(test.get_trailingPE())
    print(test.get_enterpriseToEbitda())
    print(test.get_priceToBook())
    print(test.get_forwardEps())
    print(test.get_priceToSalesTrailing12Months())

    print(create_graph("AAPL"))
