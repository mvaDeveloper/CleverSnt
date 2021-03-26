import datetime


def calculation(electricity, square, date_begin):
    today = datetime.datetime.today()
    if date_begin == "":
        date_begin = 0
    else:
        date_begin = float(date_begin)

    if electricity == "Есть":
        flag = 1
    else:
        flag = 0

    if today.year == 20:
        if flag == 1:
            membership_fee = square * 4.50
        else:
            membership_fee = square * 4
    else:
        if flag == 1:
            membership_fee = square * 5
        else:
            membership_fee = square * 4.5
    return [membership_fee, date_begin, today.year]


def making_payment(balance, cost_payment):
    balance = round(balance - float(cost_payment), 2)
    return balance


def change_electricity(date_end, date_begin, cost_payment, balance, rate_kvt, debt_cost_payment):
    today = datetime.datetime.today()
    date_payment = str(today.day) + '.' + str(today.month) + '.' + str(today.year)
    electricity = (float(date_end) - float(date_begin)) * float(rate_kvt)
    cost_payment = float(cost_payment) + electricity + debt_cost_payment
    balance = balance + electricity + debt_cost_payment
    return [electricity, cost_payment, balance, date_payment]


def calculation_diff(target_contribution_begin, membership_fee_begin, electricity_begin,
                     target_contribution_end, membership_fee_end, electricity_end):
    target_contribution_diff = float(target_contribution_end) - float(target_contribution_begin)
    membership_fee_diff = float(membership_fee_end) - float(membership_fee_begin)
    electricity_diff = float(electricity_end) - float(electricity_begin)
    diff = target_contribution_diff + membership_fee_diff + electricity_diff
    return [target_contribution_diff, membership_fee_diff, electricity_diff, diff]


def check_update_payment(cost_payment, balance, target_contribution_begin, membership_fee_begin, electricity_begin,
                         target_contribution_end, membership_fee_end, electricity_end):
    difference = calculation_diff(target_contribution_begin, membership_fee_begin, electricity_begin,
                                  target_contribution_end, membership_fee_end, electricity_end)
    diff = difference[3]
    cost_payment = float(cost_payment) + diff
    balance = float(balance) + diff
    return [cost_payment, balance]


def update_debt_diff(cost_payment_begin, cost_payment_end, target_contribution_begin,
                     membership_fee_begin, electricity_begin, target_contribution_end, membership_fee_end,
                     electricity_end, cost_payment_debt, target_contribution_debt, membership_fee_debt,
                     electricity_debt, balance_debt):
    difference = calculation_diff(target_contribution_begin, membership_fee_begin, electricity_begin,
                                  target_contribution_end, membership_fee_end, electricity_end)
    cost_payment_debt = float(cost_payment_end) - float(cost_payment_begin) + float(cost_payment_debt) + difference[3]
    target_contribution_debt = target_contribution_debt + difference[0]
    membership_fee_debt = membership_fee_debt + difference[1]
    electricity_debt = electricity_debt + difference[2]
    balance_debt = float(balance_debt) + float(cost_payment_end) - float(cost_payment_begin) + difference[3]
    return [cost_payment_debt, target_contribution_debt, membership_fee_debt, electricity_debt, balance_debt]


def debt_calculate_diversity(cost_payment, target_contribution, membership_fee, electricity, cost_payment_debt,
                             target_contribution_debt, membership_fee_debt, electricity_debt):
    cost_payment_debt = cost_payment_debt - float(cost_payment)
    target_contribution_debt = target_contribution_debt - float(target_contribution)
    membership_fee_debt = membership_fee_debt - float(membership_fee)
    electricity_debt = electricity_debt - float(electricity)
    balance_debt = cost_payment_debt
    return [cost_payment_debt, target_contribution_debt, membership_fee_debt, electricity_debt, balance_debt]
