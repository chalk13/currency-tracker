import argparse
import logging
import time

import schedule
from gazpacho import get, Soup
from klaxon import klaxonify

from config import (ENDPOINT, DEFAULT_CURRENCY, TODAY, TIMEOUT, NAME, BUY,
                    SALE, NUM)


def argument_parser():
    """Initialize argument parser"""

    description = "Currency tracker is tool which allows user to " \
                  "get currency rates on regular basis"

    parser = argparse.ArgumentParser(description=description)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', type=bool, default=False, nargs='?',
                       choices=[True, False],
                       help='get list of availiable currencies')
    group.add_argument('--rate', type=str, nargs='?', default='hide',
                       choices=['show', 'hide'],
                       help='show notification with current rate')
    group.add_argument('--change', type=str, nargs='?',
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


def get_all_currencies() -> list:
    """Return list of all currencies"""

    rates = get_currencies_rates(ENDPOINT)
    return [currency for currency in rates]


@klaxonify(title=TODAY, output_as_message=True)
def get_specific_currency_info(curr: str = DEFAULT_CURRENCY):
    """Return information for specific currency"""

    rates = get_currencies_rates(ENDPOINT)
    currency_info = rates.get(curr)
    if currency_info:
        return f'Rate for {curr}: {currency_info["buy"]}/{currency_info["sale"]}'
    else:
        return 'Check currency name and try again.'


@klaxonify(title='Check the changes', output_as_message=True)
def show_changed_currency_info(last: dict, new: dict, curr: str = DEFAULT_CURRENCY):
    up = '\u2191'
    down = '\u2193'
    if last['buy'] < new['buy'] or last['sale'] < new['sale']:
        return f'{curr} rate increased:' \
               f'\n{new["buy"]} {up}{round(new["buy"] - last["buy"], 2)} || ' \
               f'{new["sale"]} {down}{round(new["sale"] - last["sale"], 2)}'

    # TODO: implement logic


def every_day_notification(curr: str = DEFAULT_CURRENCY):
    """Send notification with actual rates"""

    result = get_currencies_rates(ENDPOINT)
    get_specific_currency_info(result, curr)


def main():
    """Script entry point"""

    last_currency = None
    args = argument_parser().parse_args()
    argv = vars(args)

    if argv['all']:
        print(get_all_currencies())
    elif argv['rate'] == 'show':
        get_specific_currency_info()

    while True:
        try:
            rates = get_currencies_rates(ENDPOINT)
            value = rates[DEFAULT_CURRENCY]
        except Exception as err:
            logging.exception(err)
        else:
            if last_currency != value:
                show_changed_currency_info(last_currency, value)
                last_currency = value
        finally:
            time.sleep(TIMEOUT)
        # schedule.every().hour.do(every_day_notification, curr=argv['set'])
    # else:
    #     schedule.every().hour.do(every_day_notification)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == '__main__':
    main()
