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
    group.add_argument('--all', action='store_true',
                       help='get list of availiable currencies')
    group.add_argument('--rate',  const='USD/UAH', type=str, nargs='?',
                       help='show notification with current rate')
    group.add_argument('--run', type=bool, const=True, nargs='?',
                       help='run a currency tracking script')

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

    if last['buy'] < new['buy']:
        buy_value = f"\n{new['buy']} {up}{round(new['buy'] - last['buy'], 2)}"
    elif last['buy'] > new['buy']:
        buy_value = f"\n{new['buy']} {down}{round(last['buy'] - new['buy'], 2)}"
    else:
        buy_value = f"\n{new['buy']}"

    if last['sale'] < new['sale']:
        sale_value = f"{new['sale']} {up}{round(new['sale'] - last['sale'], 2)}"
    elif last['sale'] > new['sale']:
        sale_value = f"{new['sale']} {down}{round(last['sale'] - new['sale'], 2)}"
    else:
        sale_value = f"{new['sale']}"

    return f'{curr} rate changes: {buy_value} || {sale_value}'


def run_track_script():
    """Currency tracking script"""

    last_currency = None

    while True:
        schedule.run_pending()
        time.sleep(1)

        try:
            rates = get_currencies_rates(ENDPOINT)
            value = rates[DEFAULT_CURRENCY]
        except Exception as err:
            logging.exception(err)
        else:
            if last_currency is None:
                last_currency = value
            elif last_currency != value:
                show_changed_currency_info(last_currency, value)
                last_currency = value
        finally:
            time.sleep(TIMEOUT)


def main():
    """Script entry point"""

    args = argument_parser().parse_args()
    argv = vars(args)
    currencies = get_all_currencies()

    if argv['all']:
        print(currencies)
    elif argv['rate']:
        if argv['rate'] in currencies:
            get_specific_currency_info(argv['rate'])
        else:
            print('You entered the wrong currency.\n'
                  'Check --all option to see availiable currencies')
    elif argv['run']:
        schedule.every().day.at("10:00").do(get_specific_currency_info)
        run_track_script()


if __name__ == '__main__':
    main()
