from telegram.ext import Updater, CommandHandler
from utils import create_graph


def send_graph(update, context):
    """
    Функция для обработчика событий отсылает только что созданный граф по тикеру
    :param context.tiker: Переменная через которую можно передавать тикер внутри бота
    """
    # Для теста присвоено значение по умолчанию AAPL
    context.tiker = "AAPL"  
    tiker_graph_filename = create_graph(context.tiker)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(tiker_graph_filename, 'rb'))
