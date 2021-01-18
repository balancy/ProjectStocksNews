import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode
from config import BOT_API_KEY, CHART_FILEPATH, CHART_FILENAME
from flaskr.db import db_session
from flaskr.user.model import BotUser
from flaskr.tickers.calculate_checks import check_graph_and_get_recommendations


def save_bot_user_to_db(user_id, username) -> None:
    """
    Saving new users to the DB.
    :param user_id: user id
    :param username: user username
    """

    user_exists = BotUser.query.filter(BotUser.id == user_id).count()
    if not user_exists:
        logging.info(f"User {username} added to DB.")
        new_user = BotUser(id=user_id, username=username)
        db_session.add(new_user)
        db_session.commit()


def read_user_info(update, _context) -> None:
    """
    Reading user's info and replying to the bot.
    """

    id = update["message"]["chat"]["id"]
    username = update["message"]["chat"]["username"]
    save_bot_user_to_db(user_id=id, username=username)
    update.message.reply_text(f"Привет! Мы внесли тебя в базу для рассылки. Как только новости будут появляться, "
                              f"ты будешь их получать через этот бот!")


def send_diagram(update, context) -> None:
    """
    Sending a diagram to the user.
    """

    ticker = update.message.text.replace('/diagram_', '')
    chat_id = update.effective_chat.id
    _checks, recommendations = check_graph_and_get_recommendations(ticker)

    filename = f"{CHART_FILEPATH}{ticker}{CHART_FILENAME}"
    context.bot.send_message(chat_id=chat_id,
                             text=f"Ticker: <b>{ticker}</b>\nAnalysts recommendation: "
                                  f"<b>{recommendations['Analysts recommendations']}</b>",
                             parse_mode=ParseMode.HTML)
    context.bot.send_photo(chat_id=chat_id, photo=open(filename, 'rb'))


def start_reading_bot() -> None:
    """
    Starting bot which reads all active users.
    """

    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher

    dp.add_handler(CommandHandler("start", read_user_info))
    dp.add_handler(MessageHandler(Filters.regex('^(/diagram_.*)$'), send_diagram))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    start_reading_bot()
