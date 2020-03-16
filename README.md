## Currency tracker
This console program will help you to track changes for a given currency and receive notifications in case of some changes. You can also check the available currencies and receive immediate notification with the current rate.

### Installation
Clone the repository to your local machine. With virtualenv enviroment activated install requirements:
```
$ pip install -r requirements.txt
```
**How to run**
```
$ python3 currency_app.py --help
usage: currency_app.py [-h] [--all | --rate [RATE] | --run [RUN]]

Currency tracker is tool which allows user to get currency rates on regular
basis

optional arguments:
  -h, --help     show this help message and exit
  --all          get list of availiable currencies
  --rate [RATE]  show notification with current rate
  --run [RUN]    run a currency tracking script
```
**Example commands**:
```
# Get a nofitication with a default rate (USD/UAH)
$ python3 currency_app.py --rate
```
```
# Run a program to track changes in exchange rate (USD/UAH)
$ python3 currency_app.py --run
```
```
# Get the list of available currencies
$ python3 currency_app.py --all
```
```
# Specify the desired currency instead of the default currency
$ python3 currency_app.py --rate EUR/UAH
$ python3 currency_app.py --run EUR/USD
```
