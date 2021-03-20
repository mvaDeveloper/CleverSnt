import datetime


def calculation(electricity, square, date_payment, date_begin):
    year = int(date_payment[-2] + date_payment[-1])
    # если введено пустое значение преобразовать его в 0
    if date_begin == "":
        date_begin = 0
    else:
        date_begin = float(date_begin)
    # проверка наличия электричества
    if electricity == "Есть":
        flag = 1
    else:
        flag = 0
    # рассчет членского взноса исходя из года и коэфициента
    if year == 20:
        if flag == 1:
            membership_fee = square * 4.50
        else:
            membership_fee = square * 4
    else:
        if flag == 1:
            membership_fee = square * 5
        else:
            membership_fee = square * 4.5
    # так как нам не известны конечные показания
    return [membership_fee, date_begin]


def making_payment(balance, cost_payment):
    balance = round(balance - float(cost_payment), 2)
    return balance


def change_electricity(date_end, date_begin, cost_payment, balance, rate_kvt):
    today = datetime.datetime.today()
    date_payment = str(today.day) + '.' + str(today.month) + '.' + str(today.year)
    electricity = (float(date_end) - float(date_begin)) * float(rate_kvt)
    cost_payment = float(cost_payment) + electricity
    balance = balance + electricity
    return [electricity, cost_payment, balance, date_payment]


def check_update_payment(cost_payment, balance, target_contribution_begin, membership_fee_begin, electricity_begin,
                         target_contribution_end, membership_fee_end, electricity_end):
    target_contribution_diff = float(target_contribution_end) - float(target_contribution_begin)
    membership_fee_diff = float(membership_fee_end) - float(membership_fee_begin)
    electricity_diff = float(electricity_end) - float(electricity_begin)
    diff = target_contribution_diff + membership_fee_diff + electricity_diff
    cost_payment = float(cost_payment) + diff
    balance = float(balance) + diff
    return [cost_payment, balance]
