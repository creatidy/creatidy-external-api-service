import datetime


class HolidayCalculator(object):
    @staticmethod
    def is_holiday(date):
        if date.weekday() == 5 or date.weekday() == 6:  # 6 = Sunday
            return True
        if date.month == 1 and date.day == 1:
            return True  # Nowy Rok
        if date.month == 1 and date.day == 6 and date.year >= 2011:
            return True  # Trzech Króli (od 2011)
        if date.month == 5 and date.day == 1:
            return True  # 1 maja
        if date.month == 5 and date.day == 3:
            return True  # 3 maja
        if date.month == 8 and date.day == 15:
            return True  # Wniebowzięcie Najświętszej Marii Panny, Święto Wojska Polskiego
        if date.month == 11 and date.day == 1:
            return True  # Dzień Wszystkich Świętych
        if date.month == 11 and date.day == 11:
            return True  # Dzień Niepodległości
        if date.month == 12 and date.day == 25:
            return True  # Boże Narodzenie
        if date.month == 12 and date.day == 26:
            return True  # Boże Narodzenie

        a = date.year % 19
        b = date.year % 4
        c = date.year % 7
        d = (a * 19 + 24) % 30
        e = (2 * b + 4 * c + 6 * d + 5) % 7
        if d == 29 and e == 6:
            d -= 7
        if d == 28 and e == 6 and a > 10:
            d -= 7
        easter = datetime.datetime(date.year, 3, 22) + datetime.timedelta(days=d + e)
        if date + datetime.timedelta(days=-1) == easter:
            return True  # Wielkanoc(poniedziałek)
        if date + datetime.timedelta(days=-60) == easter:
            return True  # Boże Ciało
        return False

    @staticmethod
    def previous_working_day(date):
        checked_date = date
        while HolidayCalculator.is_holiday(checked_date):
            checked_date = checked_date - datetime.timedelta(days=1)
        return checked_date
