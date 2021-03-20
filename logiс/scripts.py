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


def change_electricity(electricity, date_payment, electricity_availability,
                       date_end, date_begin, cost_payment, information_balance):
    if electricity == "0.0":
        print(electricity)
        year = int(date_payment[-2] + date_payment[-1])
        rate_kvt_2021 = 2.91
        if electricity_availability == "Есть":
            flag = 1
        else:
            flag = 0
        if flag:
            if year == 20 or year == 21:
                electricity = (float(date_end) - float(date_begin)) * rate_kvt_2021
            else:
                electricity = -1
        else:
            electricity = 0
        cost_payment = float(cost_payment) + electricity
        balance = information_balance + electricity
    else:
        balance = information_balance
    return [electricity, cost_payment, balance]
