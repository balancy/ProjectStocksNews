from telegram.ext import Updater, CommandHandler
from time_zone_translation import WorkTime
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


def send_work_time(update, context):
    """
    Функция для обработчика событий отсылает время открытия и закрытия биржи по переданной часовой зоне
    :param context.work_time: Переменная через которую можно передавать тикер внутри бота
    """
    # Для теста присвоено значение по умолчанию 'Europe/Moscow'
    context.work_time = 'Europe/Moscow'
    time = WorkTime(context.work_time)
    open_time = time.get_time_opening()
    close_time = time.get_time_closing()
    update.message.reply_text(
        f"Время открытия биржи NYSE {open_time} время закрытия {close_time}"
    )
