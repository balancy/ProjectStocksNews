from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
import logging
from config import BOT_API_KEY, YF_URL
from flaskr.user.model import BotUser


def get_inline_keyboard(ticker):
    keyboard = [
        [
            InlineKeyboardButton('Perspective graph', callback_data=f"diagram_{ticker}"),
            InlineKeyboardButton('History chart', callback_data=f"chart_{ticker}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


class SendingBot(Bot):
    """
    SendingBot class for creating telegram bot.
    """

    def __init__(self):
        super().__init__(BOT_API_KEY)
        self.message = ''
        self.ticker = ''

    def send_news(self) -> None:
        """
        Send news, recommendations and a graph to the bot.
        """

        users = BotUser.query.all()
        for user in users:
            self.send_message(chat_id=user.id, text=self.message, parse_mode=ParseMode.HTML,
                              reply_markup=get_inline_keyboard(self.ticker))
            logging.info(f"'News was sent to the user {user.username} ({user.id})")

    def format_from_json(self, json) -> None:
        """
        Formatting message from dictionary.
        :param json: dictionary
        """

        self.ticker = json['ticker']
        self.message = f"<a href='{json['url']}'>{json['title']}</a>\n"
        self.message += f"<b><a href='{YF_URL}{json['ticker']}'>{json['ticker']}</a>: {json['change']}%</b>\n"


sending_bot = SendingBot()
