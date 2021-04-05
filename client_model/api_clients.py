import json
from decimal import Decimal

import requests


class NbpApiClient:
    """
    NBP Web API currency exchange rates client
    """

    def __init__(self):
        self._url = 'http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/{date}?format={format}'
        self.table = "a"  # table A of middle exchange rates of foreign currencies
        self.format = "json"

    def get_rate(self, code, full_date):
        """
        Exchange rate of currency {code} from the exchange rate table of type {table} published on {date} (or lack
        of data)

        :param code: a three-letter currency code (ISO 4217 standard)
        :param full_date: a date in the YYYY-MM-DD format (ISO 8601 standard)
        :return: exchange rate of particular currency, or 0 if no data
        """
        date = full_date.strftime('%Y-%m-%d')
        response = requests.get(self._url.format(table=self.table, code=code, date=date, format=self.format))
        if response.ok:
            j_data = json.loads(response.text)
            return Decimal(j_data['rates'][0]['mid'])
        else:
            return None  # no data
