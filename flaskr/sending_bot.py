from telegram import ParseMode, Bot
from config import BOT_API_KEY
from models import BotUser


class SendingBot(Bot):
    def __init__(self):
        super().__init__(BOT_API_KEY)
        self.message = ''

    def send_news(self):
        users = BotUser.query.all()
        for user in users:
            self.send_message(chat_id=user.id, text=self.message, parse_mode=ParseMode.HTML)

    def format_from_json(self, json):
        self.message = f"<a href='{json['url']}'>{json['title']}</a>\n"
        self.message += f"<b><a href='https://finance.yahoo.com/quote/{json['ticker']}'>{json['ticker']}</a>: " \
                       f"{json['change']}%</b>"


sending_bot = SendingBot()
