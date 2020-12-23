from telegram import ParseMode, Bot
from flaskr.config import BOT_API_KEY, BOT_USER_ID


class MyBot(Bot):
    def __init__(self):
        super().__init__(BOT_API_KEY)

    def send_news(self, news):
        self.send_message(BOT_USER_ID, news, ParseMode.HTML)


bot = MyBot()
