from telegram import ParseMode, Bot
import logging
from config import BOT_API_KEY, YF_URL, CHART_FILENAME, CHART_FILEPATH
from flaskr.tickers.calculate_checks import check_graph_and_get_recommendations
from flaskr.user.model import BotUser


class SendingBot(Bot):
    """
    SendingBot class for creating telegram bot.
    """

    def __init__(self):
        super().__init__(BOT_API_KEY)
        self.message = ''

    def send_news(self) -> None:
        """
        Send news, recommendations and a graph to the bot.
        """

        users = BotUser.query.all()
        for user in users:
            self.send_message(chat_id=user.id, text=self.message, parse_mode=ParseMode.HTML)
            logging.info(f"'News was sent to the user {user.name} ({user.id})")

    def format_from_json(self, json) -> None:
        """
        Formatting message from dictionary.
        :param json: dictionary
        """

        self.message = f"<a href='{json['url']}'>{json['title']}</a>\n"
        self.message += f"<b><a href='{YF_URL}{json['ticker']}'>{json['ticker']}</a>: {json['change']}%</b>\n"
        self.message += f"/graph - receive company perspective graph"


sending_bot = SendingBot()
