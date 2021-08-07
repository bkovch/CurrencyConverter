import json
import requests
from flask import Flask

app = Flask(__name__)

currencies = ['USD', 'GBP', 'EUR']
url = 'https://freecurrencyapi.net/api/v1/rates'
api_key = '9b485480-f700-11eb-a346-bbfda717d0e3'


@app.route('/get_currency_rate/<string:base_currency>/<string:quote_currency>', methods=['GET'])
def get_currency_rate(base_currency, quote_currency):
    ''' Get currency rate
        Returns the conversion rate from base_currency to quote_currency as a floating point number.
        The rate is value of 1 unit of base_currency in quote_currency.
        The return value is a JSON object restating the currencies and the rate. '''

    if base_currency not in currencies:
        raise('Currency {} not supported.'.format(base_currency))
    if quote_currency not in currencies:
        raise('Currency {} not supported.'.format(quote_currency))

    parameters = (('apikey', api_key), ('base_currency', base_currency))
    response = requests.get(url, params = parameters)
    content = json.loads(response.content.decode())
    date_key = next(iter(content['data']))
    rate = content['data'][date_key][quote_currency]
    
    result = {}
    result['base_currency'] = base_currency
    result['quote_currency'] = quote_currency
    result['rate'] = rate

    return result

@app.route('/convert_amount/<string:base_currency>/<string:quote_currency>/<string:amount>', methods=['GET'])
def convert_amount(base_currency, quote_currency, amount):
    ''' Converts a value (amount) in one currency to another
        Returns an amount in base_currency, converted to an amount in quote_currency.
        The return value is a JSON object restating the currencies and the converted amount.
        All results are rounded to 2 decimal points. '''

    currency_rate = get_currency_rate(base_currency, quote_currency)
    rate = currency_rate['rate']
    
    result = {}
    result['base_currency'] = base_currency
    result['quote_currency'] = quote_currency
    result['amount'] = round(float(amount) * rate, 2)

    return result
