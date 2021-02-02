import aiohttp
from aiohttp import web


class TelegramAccessor:
    def __init__(self):
        self.token = None
        self.my_chat_id = None

    def setup(self, application: web.Application):
        self.token = application["config"]["telegram"]["token"]
        self.my_chat_id = application["config"]["telegram"]["my_chat_id"]
        application["telegram"] = self

    @staticmethod
    def _generate_message(
        message: str,
        polarity: float,
        subjectivity: float,
        average_polarity: float,
        average_subjectivity: float,
    ) -> str:
        return (
            f"New message: *{message}*"
            f"\n *{'%.2f' % polarity}* polarity."
            f"\n *{'%.2f' % subjectivity}* subjectivity."
            f"\n \n *{'%.2f' % average_polarity}* average polarity "
            f"\n *{'%.2f' % average_subjectivity}* average subjectivity "
        )

    async def send_message(
        self,
        message: str,
        polarity: float,
        subjectivity: float,
        average_polarity: float,
        average_subjectivity: float,
    ) -> None:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(verify_ssl=False)
        ) as session:
            async with session.get(
                f"https://api.telegram.org/"
                f"bot{self.token}/sendMessage?"
                f"parse_mode=markdown&"
                f"chat_id={self.my_chat_id}&"
                f"text={self._generate_message(message, polarity, subjectivity, average_polarity, average_subjectivity)}"
            ):
                pass
