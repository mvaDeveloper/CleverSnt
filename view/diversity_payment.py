import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments
from view.table_view import view_payments
from logiс.scripts import debt_calculate_diversity


class DiversityPayment(tk.Toplevel):
    def __init__(self, find_v, making_payment, db, window, tree):
        super().__init__()
        self.find_v = find_v
        self.making_payment = making_payment
        self.db = db
        self.window = window
        self.tree = tree
        self.title('Разнести платеж')
        self.geometry('400x340+350+130')
        tk.Toplevel.configure(self, bg="#f0eae1")
        title_label(self, 'Разнести платеж', 130, 15)
        x = 170
        self.entry_lot_number = input_payments(self, 'Номер участка:', ttk.Entry(self), x, 50)
        self.entry_date_payment = input_payments(self, 'Дата:', ttk.Entry(self), x, 75)
        self.entry_target_contribution = input_payments(self, 'Целевой взнос:', ttk.Entry(self), x, 100)
        self.entry_membership_fee = input_payments(self, 'Членский взнос:', ttk.Entry(self), x, 125)
        self.entry_electricity = input_payments(self, 'Электричество:', ttk.Entry(self), x, 150)
        self.entry_cost_payment = input_payments(self, 'Сумма:', ttk.Entry(self), x, 175)
        self.entry_combobox_status = input_payments(self, 'Статус:', ttk.Combobox(self,
                                                                                  values=[u"Не оплачен",
                                                                                          u"Оплачен частично",
                                                                                          u"Оплачен"]), x, 200)
        self.entry_combobox_type = input_payments(self, 'Тип:', ttk.Combobox(self,
                                                                             values=["Выставленный",
                                                                                     "Выплаченный"]), x, 225)

        button(self, 'Посчитать сумму', self.calculation_cost, 15, 25, 265)
        button(self, 'Разнести', self.performance_add, 15, 235, 265)
        self.entry_lot_number.insert(0, self.find_v)

    def calculation_cost(self):
        cost_payment = float(self.entry_membership_fee.get()) \
                       + float(self.entry_target_contribution.get()) \
                       + float(self.entry_electricity.get())
        self.entry_cost_payment.insert(5, cost_payment)

    def performance_add(self):
        payment = self.db.payment.get_by_id(len(self.db.payment.get_by_number(self.find_v)))
        balance = round(float(payment[9]) - float(self.entry_cost_payment.get()), 2)
        self.db.payment.insert(self.find_v, self.entry_cost_payment.get(), self.entry_date_payment.get(),
                               self.entry_target_contribution.get(), self.entry_membership_fee.get(),
                               self.entry_electricity.get(), 0, 0, balance, self.entry_combobox_status.get(),
                               self.entry_combobox_type.get()
                               )
        self.debt_update()

    def debt_update(self):
        row = list(self.db.debt.get_by_number(self.find_v))
        debt_id = row[1][0]
        debt = self.db.debt.get_by_id(debt_id)
        debt_new = debt_calculate_diversity(self.entry_cost_payment.get(), self.entry_target_contribution.get(),
                                            self.entry_membership_fee.get(), self.entry_electricity.get(),
                                            debt[2], debt[3], debt[4], debt[5])
        self.db.debt.update(self.find_v, debt_new[0], debt_new[1], debt_new[2], debt_new[3], debt_new[4], debt_id)
        view_payments(self.window, self.tree, self.find_v)
        self.destroy()
