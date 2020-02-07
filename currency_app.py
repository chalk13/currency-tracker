import argparse
import logging
import time

import schedule
from gazpacho import get, Soup
from klaxon import klaxonify

from config import ENDPOINT, DEFAULT_CURRENCY, TODAY, NAME, BUY, SALE, NUM


def argument_parser():
    """Initialize argument parser"""

    description = "Currency tracker is tool which allows user to " \
                  "get currency rates on regular basis"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--all', type=bool, default=False, nargs='?',
                        choices=[True, False],
                        help='get list of availiable currencies')
    parser.add_argument('--change', type=str, nargs='?',
                        help='change default currency to desired')

    return parser


def get_currencies_rates(url: str) -> dict:
    """Return dictionary with exchange rates"""

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
        return f'Rate for {curr}: {currency_info["buy"]}/{currency_info["sale"]}'
    else:
        return 'Check currency name and try again.'


def every_day_notification(curr: str = DEFAULT_CURRENCY):
    """Send notification with actual rates"""

    result = get_currencies_rates(ENDPOINT)
    get_specific_currency_info(result, curr)


def main():
    """Script entry point"""

    args = argument_parser().parse_args()
    argv = vars(args)
    if argv['all']:
        result = get_currencies_rates(ENDPOINT)
        print(get_all_currencies(result))

    # scheduler to send notifications every hour
    if argv['change']:
        schedule.every().hour.do(every_day_notification, curr=argv['change'])
    else:
        schedule.every().hour.do(every_day_notification)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
