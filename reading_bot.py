import logging
from sqlalchemy import exc
import sys
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

from config import BOT_API_KEY, DIAGRAM_FILEPATH, DIAGRAM_FILENAME
from flaskr.db import db_session
from flaskr.user.model import BotUser
from flaskr.stocks.calculate_checks import check_graph_and_get_recommendations
from flaskr.stocks.utils.hist_graph import create_graph
from flaskr.stocks.utils.time_zone_translation import WorkTime


def save_bot_user_to_db(user_id, username) -> bool:
    """
    Saving new users to the DB.
    :param user_id: user id
    :param username: user username
    """

    user_exists = BotUser.query.filter(BotUser.id == user_id).first()
    if not user_exists:
        logging.info(f"User {username} added to DB.")
        new_user = BotUser(id=user_id, username=username)
        db_session.add(new_user)
        try:
            db_session.commit()
            return True
        except exc.SQLAlchemyError:
            logging.info(f"Failed to add user {username} to DB.")
            sys.exit("Encountered general SQLAlchemyError in ReadingBot.")
    else:
        return False


def delete_bot_user_from_db(user_id) -> bool:
    """
    Deleting users from the DB.
    :param user_id: user id
    """

    user_exists = BotUser.query.filter(BotUser.id == user_id).first()
    if user_exists:
        logging.info(f"User with id={user_id} deleted from DB.")
        db_session.delete(user_exists)
        try:
            db_session.commit()
            return True
        except exc.SQLAlchemyError:
            logging.info(f"Failed to delete user with id={user_id} from DB.")
            sys.exit("Encountered general SQLAlchemyError in ReadingBot.")
    else:
        return False


def user_subscribe(update, _context) -> None:
    """
    Subscribing user to the bot.
    """

    id = update["message"]["chat"]["id"]
    username = update["message"]["chat"]["username"]
    is_positive = save_bot_user_to_db(user_id=id, username=username)
    if is_positive:
        update.message.reply_text(f"Мы внесли тебя в базу для рассылки. Как только новости будут появляться, "
                                  f"ты будешь их получать через этот бот!")
    else:
        update.message.reply_text(f"Ты уже в нашей базе для рассылки!")


def user_unsubscribe(update, _context) -> None:
    """
    Unsubscribing user from the bot.
    """

    id = update["message"]["chat"]["id"]
    is_positive = delete_bot_user_from_db(user_id=id)
    if is_positive:
        update.message.reply_text(f"Мы убрали тебя из базы для рассылки.")
    else:
        update.message.reply_text(f"Ты еще не подписан на рассылку!")


def send_diagram(update, context) -> None:
    """
    Sending a diagram to the user.
    """

    ticker = update.message.text.replace('/diagram_', '')
    chat_id = update.effective_chat.id
    _checks, recommendations = check_graph_and_get_recommendations(ticker)

    filename = f"{DIAGRAM_FILEPATH}{ticker}{DIAGRAM_FILENAME}"
    context.bot.send_message(chat_id=chat_id,
                             text=f"Ticker: <b>{ticker}</b>\nAnalysts recommendation: "
                                  f"<b>{recommendations['Analysts recommendations']}</b>",
                             parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))


def send_chart(update, context) -> None:
    """
    Функция для обработчика событий отсылает только что созданный граф по тикеру
    """
    ticker = update.message.text.replace('/chart_', '')
    filename = create_graph(ticker)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))


def send_work_time(update, context) -> None:
    """
    Функция для обработчика событий отсылает время открытия и закрытия биржи по переданной часовой зоне
    """
    # Для теста присвоено значение по умолчанию 'Europe/Moscow'
    context.work_time = 'Europe/Moscow'
    time = WorkTime(context.work_time)
    open_time = time.get_time_opening()
    close_time = time.get_time_closing()
    update.message.reply_text(
        f"Время открытия биржи NYSE {open_time} время закрытия {close_time}"
    )


def start_reading_bot() -> None:
    """
    Starting bot which reads all active users.
    """

    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("subscribe", user_subscribe))
    dp.add_handler(CommandHandler("unsubscribe", user_unsubscribe))
    dp.add_handler(MessageHandler(Filters.regex('^(/diagram_.*)$'), send_diagram))
    dp.add_handler(MessageHandler(Filters.regex('^(/chart_.*)$'), send_chart))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    start_reading_bot()
