from decimal import Decimal

import mysql.connector


class NationalBankRates:
    """

    """

    def __init__(self):
        self.record = None
        self.id = 0
        self.cnx = mysql.connector.connect(user='root', password='root',
                                           host='127.0.0.1',
                                           database='mydb')

    def __del__(self):
        self.cnx.close()

    def get_rate(self, asset, date) -> Decimal:
        """

        :param asset: Currency to PLN
        :param date: Date of NBP rate
        :return: NBP rate, or None if no data in DB
        """
        query = ("""SELECT rate FROM nbp_rates 
                    WHERE currency = %s AND date = %s""")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (asset, date))
        if cursor.rowcount == 1:
            result = cursor.fetchall()[0][0]
            cursor.close()
            return Decimal(str(result))
        else:
            return None

    def insert_rate(self, currency, date, rate):
        query = ("""INSERT INTO nbp_rates (currency, date, rate) 
                    VALUES (%s, %s, %s)""")
        cursor = self.cnx.cursor(buffered=True)
        cursor.execute(query, (currency, date, rate))
        self.cnx.commit()
        cursor.close()
