import datetime

ENDPOINT = 'https://obmenka24.kiev.ua/ua'
TODAY = f'{datetime.datetime.now().strftime("%A, %d %B")}'
TIMEOUT = 60

# endpoint classes names
NAME = 'currencies__block-name'
BUY = 'currencies__block-buy'
SALE = 'currencies__block-sale'
NUM = 'currencies__block-num'
