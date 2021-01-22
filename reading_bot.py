import logging
from sqlalchemy import exc
import sys
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram import ParseMode

from config import BOT_API_KEY, DIAGRAM_FILEPATH, DIAGRAM_FILENAME
from flaskr.db import db_session
from flaskr.sending_bot import get_inline_keyboard
from flaskr.stocks.calculate_checks import check_graph_and_get_recommendations
from flaskr.stocks.utils.hist_graph import create_graph
from flaskr.user.model import BotUser


logging.basicConfig(
    filename="reading_bot.log", level=logging.INFO,
    format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def read_user_info(update, _context) -> None:
    """
    Reading user's info and replying to the bot.
    """

    update.message.reply_text(f"Привет! Это бот для рассылки новостей по акциям компаний, торгующихся на Спб бирже.\n\n"
                              f"/subscribe - подписаться на рассылку\n"
                              f"/unsubscribe - отписаться от рассылки")


def save_bot_user_to_db(user_id, username) -> bool:
    """
    Saving new users to the DB.
    :param user_id: user id
    :param username: user username
    """

    user_exists = BotUser.query.filter(BotUser.id == user_id).first()
    if not user_exists:
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
        logging.info(f"User {username} added to DB.")
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
        logging.info(f"User with id={id} deleted from DB.")
        update.message.reply_text(f"Мы убрали тебя из базы для рассылки.")
    else:
        update.message.reply_text(f"Ты еще не подписан на рассылку!")


def send_diagram(update, context, ticker) -> None:
    """
    Sending a diagram to the user.
    """

    _checks, recommendations = check_graph_and_get_recommendations(ticker)
    chat_id = update.effective_chat.id
    filename = f"{DIAGRAM_FILEPATH}{ticker}{DIAGRAM_FILENAME}"

    context.bot.send_message(chat_id=chat_id,
                             text=f"Ticker: <b>{ticker}</b>\nAnalysts recommendation: "
                                  f"<b>{recommendations['Analysts recommendations']}</b>",
                             parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=chat_id,
                           caption=f"{ticker} Perspective Diagram",
                           photo=open(filename, 'rb'),
                           reply_markup=get_inline_keyboard(ticker))
    logging.info(f"{ticker} perspective diagram was sent to User with id={chat_id}.")


def send_chart(update, context, ticker) -> None:
    """
    Функция для обработчика событий отсылает только что созданный граф по тикеру
    """

    filename = create_graph(ticker)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, caption=f"{ticker} History Chart",
                           photo=open(filename, 'rb'),
                           reply_markup=get_inline_keyboard(ticker))
    logging.info(f"{ticker} history chart was sent to User with id={chat_id}.")


def send_diagram_and_chart(update, context) -> None:
    """
    Handles callback from inline keyboard and creates graph or diagram depending on choice
    """
    update.callback_query.answer()
    callback_type, ticker = update.callback_query.data.split("_")
    if callback_type == "diagram":
        send_diagram(update, context, ticker)
    elif callback_type == "chart":
        send_chart(update, context, ticker)


def start_reading_bot() -> None:
    """
    Starting bot which reads all active users.
    """

    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", read_user_info))
    dp.add_handler(CommandHandler("subscribe", user_subscribe))
    dp.add_handler(CommandHandler("unsubscribe", user_unsubscribe))
    dp.add_handler(CallbackQueryHandler(send_diagram_and_chart))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    start_reading_bot()
