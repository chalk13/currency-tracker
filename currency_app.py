import logging
import datetime
import schedule
import time
from gazpacho import get, Soup
from klaxon import klaxonify

ENDPOINT = 'https://obmenka24.kiev.ua/ua'
DEFAULT_CURRENCY = 'USD/UAH'

# endpoint classes names
NAME = 'currencies__block-name'
BUY = 'currencies__block-buy'
SALE = 'currencies__block-sale'
NUM = 'currencies__block-num'
TODAY = f'{datetime.datetime.now().strftime("%A, %d %B")}'


def get_currency_rates(url: str) -> dict:
    result = {}

    try:
        response = get(url)
        soup = Soup(response)

        currencies = soup.find('span', {'class': NAME})
        buy = soup.find('span', {'class': BUY})
        buy_values = [value.find('div', {'class': NUM}).text for value in buy]
        sale = soup.find('span', {'class': SALE})
        sale_values = [value.find('div', {'class': NUM}).text for value in sale]

        for cur, buy_num, sale_num in zip(currencies, buy_values, sale_values):
            result[cur.text] = {'buy': float(buy_num), 'sale': float(sale_num)}

    except Exception as err:
        logging.exception(err)

    return result


def get_all_currencies(rates: dict) -> list:
    """Return list of all currencies"""

    return [currency for currency in rates]


@klaxonify(title=TODAY, output_as_message=True)
def get_specific_currency_info(rates: dict, curr: str = DEFAULT_CURRENCY):
    """Return information for specific currency"""

    currency_info = rates.get(curr)
    if currency_info:
        return f'Rate for {curr}: {currency_info}'
    else:
        return 'Check currency name and try again.'


def every_day_notification():
    """Send notification with actual rates"""

    result = get_currency_rates(ENDPOINT)
    get_specific_currency_info(result)


# scheduler to send notifications every hour
schedule.every().hour.do(every_day_notification)


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
