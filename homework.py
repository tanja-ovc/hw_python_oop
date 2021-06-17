import datetime as dt


class Record:

    def __init__(self, amount, comment, date=None):
        if date is None:
            self.date = dt.date.today()
        else:
            date_to_be = dt.datetime.strptime(date, '%d.%m.%Y')
            self.date = date_to_be.date()
        self.amount = amount
        self.comment = comment


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        total_amount_today = sum(
            [each_record.amount for each_record in self.records
             if each_record.date == today]
        )
        return total_amount_today

    def what_is_left_today(self):
        spent_today = self.get_today_stats()
        leftover_today = self.limit - spent_today
        return leftover_today

    def get_week_stats(self):
        today = dt.date.today()
        a_week_ago = today - dt.timedelta(days=7)
        total_amount_over_7days = sum(
            each_record.amount for each_record in self.records
            if a_week_ago < each_record.date <= today
        )
        return total_amount_over_7days


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        leftover_today = self.what_is_left_today()
        if leftover_today > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {leftover_today} кКал'
            )
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.345
    EURO_RATE = 88.164

    def get_today_cash_remained(self, currency):
        currencies_and_rates = {'rub': [self.RUB_RATE, 'руб'],
                                'usd': [self.USD_RATE, 'USD'],
                                'eur': [self.EURO_RATE, 'Euro']}

        if currency not in currencies_and_rates:
            raise ValueError(f'Валюта "{currency}" не распознана')

        leftover_today = self.what_is_left_today()

        if leftover_today == 0:
            return 'Денег нет, держись'

        currency_rate, currency_name = currencies_and_rates[currency]
        leftover_today_converted = (leftover_today / currency_rate)
        leftover_today_rounded = round((leftover_today_converted), 2)
        leftover_today_absolute = abs(leftover_today_rounded)

        if leftover_today > 0:
            return (
                'На сегодня осталось '
                f'{leftover_today_rounded} {currency_name}'
            )
        elif leftover_today < 0:
            return (
                'Денег нет, держись: твой долг - '
                f'{leftover_today_absolute} {currency_name}'
            )


if __name__ == "__main__":
    record_food_1 = Record(amount=150, comment='сырок', date='13.06.2021')
    record_food_2 = Record(amount=350, comment='кура с гречей')
    record_food_3 = Record(amount=200, comment='йогурт', date='01.12.1998')
    record_food_4 = Record(amount=333, comment='Choya Classic')

    record_cash_1 = Record(3550, 'линзы', '13.06.2021')
    record_cash_2 = Record(7900, 'сумка', '10.07.2017')
    record_cash_3 = Record(255, '"Тройка"')

    calories_calculator = CaloriesCalculator(2400)

    cash_calculator = CashCalculator(45)

    calories_calculator.add_record(record_food_1)
    calories_calculator.add_record(record_food_2)
    calories_calculator.add_record(record_food_3)
    calories_calculator.add_record(record_food_4)

    cash_calculator.add_record(record_cash_1)
    cash_calculator.add_record(record_cash_2)
    cash_calculator.add_record(record_cash_3)

    print(calories_calculator.get_today_stats())
    print(calories_calculator.get_week_stats())
    print(calories_calculator.get_calories_remained())

    print(cash_calculator.get_today_stats())
    print(cash_calculator.get_week_stats())
    print(cash_calculator.get_today_cash_remained('eur'))
