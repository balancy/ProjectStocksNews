from telegram import ParseMode, Bot
from flaskr.config import BOT_API_KEY, BOT_USER_ID


class MyBot(Bot):
    def __init__(self):
        super().__init__(BOT_API_KEY)
        self.message = ''

    def send_news(self):
        self.send_message(BOT_USER_ID, self.message, ParseMode.HTML)

    def format_from_json(self, json):
        self.message = f"<b>{json['ticker']}: {json['change']}%</b>\n"
        self.message += f"<a href='{json['title']}'>{json['url']}</a>"


bot = MyBot()
