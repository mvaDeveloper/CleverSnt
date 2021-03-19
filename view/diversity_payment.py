import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments


class DiversityPayment(tk.Toplevel):
    def __init__(self, find_v, making_payment, db):
        super().__init__()
        self.find_v = find_v
        self.making_payment = making_payment
        self.db = db
        self.title('Разнести платеж')
        self.geometry('450x340+400+300')
        tk.Toplevel.configure(self, bg="#f0eae1")
        title_label(self, 'Разнести платеж', 170, 10)
        x = 220
        self.entry_lot_number = input_payments(self, 'Номер участка:', ttk.Entry(self), x, 40)
        self.entry_date_payment = input_payments(self, 'Дата:', ttk.Entry(self), x, 65)
        self.entry_target_contribution = input_payments(self, 'Целевой взнос:', ttk.Entry(self), x, 90)
        self.entry_membership_fee = input_payments(self, 'Членский взнос:', ttk.Entry(self), x, 115)
        self.entry_electricity = input_payments(self, 'Электричество:', ttk.Entry(self), x, 140)
        self.entry_cost_payment = input_payments(self, 'Сумма:', ttk.Entry(self), x, 165)
        self.entry_combobox_status = input_payments(self, 'Статус:', ttk.Combobox(self,
                                                                                  values=[u"Не оплачен",
                                                                                          u"Оплачен частично",
                                                                                          u"Оплачен"]), x, 190)
        self.entry_combobox_type = input_payments(self, 'Тип:', ttk.Combobox(self,
                                                                             values=["Выставленный",
                                                                                     "Выплаченный"]), x, 215)

        button(self, 'Посчитать сумму', self.calculation_cost, 15, 65, 245)
        button(self, 'Разнести', self.performance_add, 15, 255, 245)
        self.default_data()

    def default_data(self):
        self.entry_lot_number.insert(0, self.find_v)

    def calculation_cost(self):
        cost_payment = float(self.entry_membership_fee.get()) \
                       + float(self.entry_target_contribution.get()) \
                       + float(self.entry_electricity.get())
        self.entry_cost_payment.insert(5, cost_payment)

    def find_last_payment(self):
        row = self.db.payment.get_by_number(self.find_v)
        return len(row)

    def performance_add(self):
        payment = self.db.payment.get_by_id(self.find_last_payment())
        balance = self.making_payment(round(float(payment[9]), 2), self.entry_cost_payment.get())
        self.db.payment.insert(self.find_v, self.entry_cost_payment.get(), self.entry_date_payment.get(),
                               self.entry_target_contribution.get(), self.entry_membership_fee.get(),
                               self.entry_electricity.get(), 0, 0, balance, self.entry_combobox_status.get(),
                               self.entry_combobox_type.get()
                               )
        self.debt_update(self.entry_cost_payment.get(), self.entry_target_contribution.get(),
                         self.entry_membership_fee.get(), self.entry_electricity.get(), balance
                         )

    def debt_update(self, cost_payment, target_contribution,
                    membership_fee, electricity, balance,
                    ):
        row = list(self.db.get_debt_number(self.find_v))
        debt_id = row[1][0]
        debt = self.db.debt.get_by_id(debt_id)
        self.db.debt.update(self.find_v, debt[2] - float(cost_payment), debt[3] - float(target_contribution),
                            debt[4] - float(membership_fee), debt[5] - float(electricity), balance, debt_id)
