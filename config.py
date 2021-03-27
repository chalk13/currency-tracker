import datetime

ENDPOINT: str = "https://obmenka24.kiev.ua/ua"
TODAY: str = f"{datetime.datetime.now().strftime('%A, %d %B')}"
TIMEOUT: int = 60

# endpoint classes names
NAME: str = "currencies__block-name"
BUY: str = "currencies__block-buy"
SALE: str = "currencies__block-sale"
NUM: str = "currencies__block-num"
