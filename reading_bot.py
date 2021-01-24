import logging
from sqlalchemy import exc
import sys
from telegram.ext import CommandHandler, CallbackQueryHandler, Updater
from telegram import ParseMode

from config import BOT_API_KEY, DIAGRAM_FILEPATH, DIAGRAM_FILENAME
from flaskr.db import db_session
from flaskr.sending_bot import get_inline_keyboard
from flaskr.stocks.db_interact import get_stocks_fundamentals
from flaskr.stocks.checks_and_recommendations import check_graph, get_recommendations_for_view
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
            sys.exit("Encountered general SQLAlchemyError during saving user in DB in ReadingBot.")
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
            sys.exit("Encountered general SQLAlchemyError during deleting user from DB in ReadingBot.")
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

    fundamentals = get_stocks_fundamentals(ticker)
    check_graph(ticker, fundamentals)

    chat_id = update.effective_chat.id
    filename = f"{DIAGRAM_FILEPATH}{ticker}{DIAGRAM_FILENAME}"

    if filename:
        context.bot.send_photo(chat_id=chat_id,
                               caption=f"{ticker} Perspective Diagram",
                               photo=open(filename, 'rb'),
                               reply_markup=get_inline_keyboard(ticker))
        logging.info(f"{ticker} perspective diagram was sent to User with id={chat_id}.")
    else:
        logging.error(f"Impossible to create {ticker} perspective diagram. Maybe data is unavailable.")


def send_chart(update, context, ticker) -> None:
    """
    Sending a history chart to the user.
    """

    filename = create_graph(ticker)
    if filename:
        chat_id = update.effective_chat.id
        context.bot.send_photo(chat_id=chat_id, caption=f"{ticker} History Chart",
                               photo=open(filename, 'rb'),
                               reply_markup=get_inline_keyboard(ticker))
        logging.info(f"{ticker} history chart was sent to User with id={chat_id}.")
    else:
        logging.error(f"Impossible to create {ticker} price chart. Maybe data is unavailable.")


def send_recommendations(update, context, ticker) -> None:
    """
    Sending recommendations to the user.
    """

    fundamentals = get_stocks_fundamentals(ticker)
    recommendations = get_recommendations_for_view(fundamentals)
    if recommendations:
        chat_id = update.effective_chat.id
        text = ''.join([f"{every}: <b>{recommendations[every]}</b>\n" for every in recommendations])
        context.bot.send_message(chat_id=chat_id,
                                 text=f"Ticker: <b>{ticker}</b>\n{text}",
                                 reply_markup=get_inline_keyboard(ticker),
                                 parse_mode=ParseMode.HTML)
        logging.info(f"{ticker} recommendations were sent to User with id={chat_id}.")
    else:
        logging.info(f"Impossible to create {ticker} price chart. It's possible that data is unavailable.")


def callback_handling(update, context) -> None:
    """
    Handles callback from inline keyboard and shows recommendations, creates graph or diagram depending on choice
    """

    update.callback_query.answer()
    callback_type, ticker = update.callback_query.data.split("_")
    if callback_type == "diagram":
        send_diagram(update, context, ticker)
    elif callback_type == "chart":
        send_chart(update, context, ticker)
    elif callback_type == "recommendations":
        send_recommendations(update, context, ticker)


def start_reading_bot() -> None:
    """
    Starting bot which reads all active users.
    """

    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", read_user_info))
    dp.add_handler(CommandHandler("subscribe", user_subscribe))
    dp.add_handler(CommandHandler("unsubscribe", user_unsubscribe))
    dp.add_handler(CallbackQueryHandler(callback_handling))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    start_reading_bot()
