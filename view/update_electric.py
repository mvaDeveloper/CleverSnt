import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments
from logiс.scripts import change_electricity
from view.table_view import view_payments


class UpdateElectric(tk.Toplevel):
    def __init__(self, find_v, number, dao, window, tree):
        super().__init__()
        self.find_v = find_v
        self.number = number
        self.dao = dao
        self.window = window
        self.tree = tree
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.geometry('400x205+350+370')
        self.title('Изменить информацию об электричестве')
        title_label(self, 'Изменение конечных показаний', 70, 15)
        self.entry_date_end = input_payments(self, 'Конечные показания:', ttk.Entry(self), 185, 50)
        self.entry_rate = input_payments(self, 'Тариф:', ttk.Combobox(self, values=[u"2.91"]), 185, 75)
        button(self, 'Редактировать', self.update_electric, 15, 135, 115)

    def update_electric(self):
        row = list(self.dao.debt.get_by_number(self.find_v))
        debt_id = row[0][0]
        debt = self.dao.debt.get_by_id(debt_id)
        payment = self.dao.payment.get_by_id(self.number)
        changes = change_electricity(self.entry_date_end.get(), payment[7], payment[2],
                                     payment[9], self.entry_rate.get(), debt[2]
                                     )
        self.dao.payment.update(payment[1], changes[1], changes[3], payment[4], payment[5], changes[0], payment[7],
                                self.entry_date_end.get(), changes[2], payment[10], payment[11], self.number)
        self.debt_update(payment[1], payment[4], payment[5], changes[0], changes[2])
        view_payments(self.window, self.tree, self.find_v)
        self.destroy()

    def debt_update(self, lot_number, target_contribution,
                    membership_fee, electricity, balance,
                    ):
        row = list(self.dao.debt.get_by_number(lot_number))
        debt_id = row[1][0]
        debt = self.dao.debt.get_by_id(debt_id)
        self.dao.debt.update(lot_number, balance, debt[3] + float(target_contribution),
                             debt[4] + float(membership_fee), debt[5] + float(electricity), balance, debt_id)
