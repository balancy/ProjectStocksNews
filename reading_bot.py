from telegram.ext import Updater, CommandHandler
from config import BOT_API_KEY
from flaskr.db import db_session
from flaskr.user.model import BotUser


def save_bot_user_to_db(user_id, username) -> None:
    """Saving new users ids to the DB
    """

    user_exists = BotUser.query.filter(BotUser.id == user_id).count()
    if not user_exists:
        print(f"User {username} added to Bot users")
        new_user = BotUser(id=user_id, username=username)
        db_session.add(new_user)
        db_session.commit()


def start_reading_bot() -> None:
    """Starting bot which reads all active users ids
    """

    mybot = Updater(BOT_API_KEY, use_context=True)
    dp = mybot.dispatcher

    def read_user_info(update, _context):
        """Reading user's info."""

        id = update["message"]["chat"]["id"]
        username = update["message"]["chat"]["username"]
        save_bot_user_to_db(user_id=id, username=username)
        update.message.reply_text(f"Привет! Мы внесли тебя в базу для рассылки. Как только новости будут появляться, "
                                  f"ты будешь их получать через этот бот!")

    dp.add_handler(CommandHandler("start", read_user_info))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    start_reading_bot()
