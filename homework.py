import datetime as dt

date_format = '%d.%m.%Y'
moment = dt.datetime.strptime('12.06.2021', date_format)
day = moment.date()
now = dt.datetime.now()


class Record:

    def __init__(self, amount, comment, date=None):
        if date is None:
            self.date = now.date()
        else:
            date_for_else = dt.datetime.strptime(date, date_format)
            self.date = date_for_else.date()
        self.amount = amount
        self.comment = comment


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self):
        total_amount_today = 0
        for each_record in self.records:
            if each_record.date == now.date():
                total_amount_today += each_record.amount
        return total_amount_today

    def get_week_stats(self):
        total_amount_over_7days = 0
        a_week_ago = dt.datetime.now() - dt.timedelta(days=7)
        for each_record in self.records:
            if a_week_ago.date() < each_record.date <= now.date():
                total_amount_over_7days += each_record.amount
        return total_amount_over_7days


class CaloriesCalculator(Calculator):

    def get_today_stats(self):
        calories_eaten_today = super().get_today_stats()
        return f'Калорий сегодня съедено (кКал): {calories_eaten_today}'

    def get_week_stats(self):
        calories_over_7days = super().get_week_stats()
        return (
            'Калорий за последние 7 дней съедено '
            f'(кКал): {calories_over_7days}'
        )

    def get_calories_remained(self):
        calories_eaten_today = super().get_today_stats()
        calories_allowed_today = self.limit - calories_eaten_today
        if calories_eaten_today < self.limit:
            return (
                'Сегодня можно съесть что-нибудь ещё, но с общей '
                f'калорийностью не более {calories_allowed_today} кКал'
            )
        else:
            return 'Хватит есть!'


calories_calculator = CaloriesCalculator(2400)

record_food_1 = Record(amount=150, comment='сырок')
record_food_2 = Record(amount=350, comment='кура с гречей', date='13.06.2021')
record_food_3 = Record(amount=200, comment='йогурт', date='01.12.1998')
record_food_4 = Record(amount=333, comment='Choya Classic')

calories_calculator.add_record(record_food_1)
calories_calculator.add_record(record_food_2)
calories_calculator.add_record(record_food_3)
calories_calculator.add_record(record_food_4)


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.345
    EURO_RATE = 88.164

    def get_today_stats(self):
        cash_spent_today = super().get_today_stats()
        return f'Денег сегодня потрачено (руб.): {cash_spent_today}'

    def get_week_stats(self):
        cash_spent_over_7days = super().get_week_stats()
        return (
            'Денег за последние 7 дней потрачено (руб.): '
            f'{cash_spent_over_7days}'
        )

    def get_today_cash_remained(self, currency):
        currencies_dict = {'rub': [self.RUB_RATE, 'руб'],
                           'usd': [self.USD_RATE, 'USD'],
                           'eur': [self.EURO_RATE, 'Euro']}
        limit = self.limit
        cash_spent_today = super().get_today_stats()
        currency_rate = currencies_dict[currency][0]
        currency_name = currencies_dict[currency][1]
        cash_remainder_unrnd = ((limit - cash_spent_today) / currency_rate)
        cash_remainder = round((cash_remainder_unrnd), 2)
        cash_remainder_absolute = abs(cash_remainder)

        if cash_remainder < 0:
            return (
                'Денег нет, держись: твой долг - '
                f'{cash_remainder_absolute} {currency_name}'
            )
        elif cash_remainder == 0:
            return 'Денег нет, держись'
        elif cash_remainder > 0:
            return f'На сегодня осталось {cash_remainder} {currency_name}'


cash_calculator = CashCalculator(30)

record_cash_1 = Record(3550, 'линзы', '13.06.2021')
record_cash_2 = Record(7900, 'сумка', '10.07.2017')
record_cash_3 = Record(255, '"Тройка"')

cash_calculator.add_record(record_cash_1)
cash_calculator.add_record(record_cash_2)
cash_calculator.add_record(record_cash_3)
