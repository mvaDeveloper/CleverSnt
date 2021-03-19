import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments
from logiс.scripts import change_electricity
from view.table_view import view_payments


class UpdatePayment(tk.Toplevel):
    def __init__(self, find_v, number, dao, window, tree):
        super().__init__()
        self.find_v = find_v
        self.number = number
        self.dao = dao
        self.window = window
        self.tree = tree
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.geometry('450x400+400+300')
        self.title('Редактировать позицию')
        title_label(self, 'Изменение платежа', 150, 10)
        x = 220
        self.entry_lot_number = input_payments(self, 'Номер участка:', ttk.Entry(self), x, 35)
        self.entry_cost_payment = input_payments(self, 'Сумма платежа:', ttk.Entry(self), x, 60)
        self.entry_date_payment = input_payments(self, 'Дата:', ttk.Entry(self), x, 85)
        self.entry_target_contribution = input_payments(self, 'Целевой взнос:', ttk.Entry(self), x, 110)
        self.entry_membership_fee = input_payments(self, 'Членский взнос:', ttk.Entry(self), x, 135)
        self.entry_electricity = input_payments(self, 'Элнетричество:', ttk.Entry(self), x, 160)
        self.entry_date_begin = input_payments(self, 'Начальные показания:', ttk.Entry(self), x, 185)
        self.entry_date_end = input_payments(self, 'Конечные показания:', ttk.Entry(self), x, 210)
        self.entry_combobox_status = input_payments(self, 'Статус:', ttk.Combobox(self,
                                                                                  values=[u"Не оплачен",
                                                                                          u"Оплачен частично",
                                                                                          u"Оплачен"]), x, 235)
        self.entry_combobox_type = input_payments(self, 'Тип:', ttk.Combobox(self,
                                                                             values=["Выставленный",
                                                                                     "Выплаченный"]), x, 260)
        button(self, 'Редактировать', self.payment_update, 15, 150, 310)
        self.default_data()

    # заполнение полей ввода исходной информацией
    def default_data(self):
        payment = self.dao.payment.get_by_id(self.number)
        self.entry_lot_number.insert(0, payment[1])
        self.entry_cost_payment.insert(0, payment[2])
        self.entry_date_payment.insert(0, payment[3])
        self.entry_target_contribution.insert(0, payment[4])
        self.entry_membership_fee.insert(0, payment[5])
        self.entry_electricity.insert(0, payment[6])
        self.entry_date_begin.insert(0, payment[7])
        self.entry_date_end.insert(0, payment[8])
        if payment[9] == 'Не оплачен':
            self.entry_combobox_status.current(2)
        elif payment[9] == 'Оплачен частично':
            self.entry_combobox_status.current(1)
        else:
            self.entry_combobox_status.current(0)
        if payment[10] == 'Выставленный':
            self.entry_combobox_type.current(1)
        else:
            self.entry_combobox_type.current(0)

    def payment_update(self):
        payment = change_electricity(self.entry_electricity.get(), self.entry_date_payment.get(),
                                     self.electricity_availability(self.find_v), self.entry_date_end.get(),
                                     self.entry_date_begin.get(), self.entry_cost_payment.get(),
                                     self.information_balance()
                                     )
        self.dao.payment.update(self.find_v, payment[1], self.entry_date_payment.get(),
                                self.entry_target_contribution.get(), self.entry_membership_fee.get(),
                                payment[0], self.entry_date_begin.get(), self.entry_date_end.get(),
                                payment[1], self.entry_combobox_status.get(), self.entry_combobox_type.get(),
                                self.number
                                )
        self.debt_update(self.find_v, payment[1], self.entry_target_contribution.get(),
                         self.entry_membership_fee.get(), payment[0], payment[2]
                         )
        view_payments(self.window, self.tree, self.find_v)
        self.destroy()

    def debt_update(self, lot_number, cost_payment, target_contribution,
                    membership_fee, electricity, balance,
                    ):
        row = list(self.dao.debt.get_by_number(lot_number))
        debt_id = row[1][0]
        debt = self.dao.debt.get_by_id(debt_id)
        self.dao.debt.update(lot_number, debt[2] + float(cost_payment), debt[3] + float(target_contribution),
                             debt[4] + float(membership_fee), debt[5] + float(electricity), balance, debt_id)

    def electricity_availability(self, lot_number):
        row = self.dao.owner.get_by_number(lot_number)
        return row[7]

    def information_balance(self):
        row = self.dao.payment.get_by_id(self.number)
        return row[9]
