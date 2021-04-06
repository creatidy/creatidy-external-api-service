import datetime

from source_controller.polish_holidays import HolidayCalculator
from client_model.db_client import NationalBankRates
from client_model.api_clients import NbpApiClient
from decimal import Decimal


class FiatCurrencyRates:

    @staticmethod
    def get_rate_pln(currency, transaction_date, only_working_days=False):
        # currency exchange rate on the day before
        date = (transaction_date - datetime.timedelta(days=1)).date()

        if only_working_days:
            date = HolidayCalculator.previous_working_day(date)  # last working day

        nbp = NationalBankRates()
        nbp_rate = nbp.get_rate(currency, date)

        if nbp_rate is None:  # No data in database
            # Get data from public NBP API
            nbp_api = NbpApiClient()
            nbp_rate = nbp_api.get_rate(currency, date)
            if nbp_rate is None:
                # No data from previous day, another trying with last working day
                before_holiday = HolidayCalculator.previous_working_day(date)
                nbp_rate = nbp.get_rate(currency, before_holiday)  # Check if rate is in DB?
                if nbp_rate is None:
                    # No data in DB
                    nbp_rate = nbp_api.get_rate(currency, before_holiday)
                    if nbp_rate is None:
                        raise Exception("No NBP rate")
            else:
                nbp.insert_rate(currency, date, nbp_rate)  # DB OK - update DB with holiday date
        return nbp_rate
