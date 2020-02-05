import argparse
import logging
from gazpacho import get, Soup

ENDPOINT = 'https://obmenka24.kiev.ua/ua'
DEFAULT_CURRENCY = 'USD/UAH'

# endpoint classes names
NAME = 'currencies__block-name'
BUY = 'currencies__block-buy'
SALE = 'currencies__block-sale'
NUM = 'currencies__block-num'


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

if __name__ == '__main__':
    result = get_currency_rates(ENDPOINT)
    print(get_all_currencies(result))
