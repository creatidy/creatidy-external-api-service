import datetime

from source_controller.polish_holidays import HolidayCalculator
from client_model.db_client import NationalBankRates
from client_model.api_clients import NbpApiClient
from decimal import Decimal


class FiatCurrencyRates:

    @staticmethod
    def get_rate_pln(currency, transaction_date, only_working_days=False):
        # currency exchange rate on the day before
        date = HolidayCalculator.previous_working_day(transaction_date)  # last working day

        nbp = NationalBankRates()
        nbp_rate = nbp.get_rate(currency, date)

        if nbp_rate is None:  # No data in database
            # Get data from public NBP API
            nbp_api = NbpApiClient()
            test_date = date
            nbp_rate = nbp_api.get_rate(currency, test_date)
            while nbp_rate is None:
                # No data from previous day, another trying with last working day
                test_date = HolidayCalculator.previous_working_day(test_date)
                nbp_rate = nbp.get_rate(currency, test_date)  # Check if rate is in DB?
            nbp.insert_rate(currency, date, nbp_rate)  # DB OK - update DB with holiday date
        return nbp_rate
