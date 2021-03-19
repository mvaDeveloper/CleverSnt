import tkinter as tk
from tkinter import ttk
from view.utilities import input_payments, title_label, button


class AddPay(tk.Toplevel):
    def __init__(self, dao, calculation):
        super().__init__()
        self.dao = dao
        #self.callback = callback
        self.calculation = calculation
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.title('Выставление счета')
        self.geometry('450x350+400+300')
        title_label(self, 'Выставление счета', 120, 10)

        x = 220
        self.date_end = 0
        self.date_payment = 'xx.yy.2021'
        self.entry_lot_number = input_payments(self, 'Номер участка:', ttk.Entry(self), x, 40)
        self.entry_date_begin = input_payments(self, 'Начальные показания:', ttk.Entry(self), x, 65)
        self.entry_target_contribution_debt = input_payments(self, 'Долг целевой:', ttk.Entry(self), x, 90)
        self.entry_membership_fee_debt = input_payments(self, 'Долг членский:', ttk.Entry(self), x, 115)
        self.entry_electricity_debt = input_payments(self, 'Долг электричество:', ttk.Entry(self), x, 140)
        self.entry_cost_payment_debt = input_payments(self, 'Долг общий:', ttk.Entry(self), x, 165)
        self.entry_combobox_status = input_payments(self, 'Статус:', ttk.Combobox(self,
                                                                                  values=[u"Не оплачен",
                                                                                          u"Оплачен частично",
                                                                                          u"Оплачен"]), x, 190)
        self.entry_combobox_type = input_payments(self, 'Тип:', ttk.Combobox(self,
                                                                             values=["Выставленный",
                                                                                     "Выплаченный"]), x, 215)

        button(self, 'Добавить', self.performance_add, 15, 255, 260)
        button(self, 'Рассчитать', self.calculation_debt, 15, 65, 260)

        self.grab_set()
        self.focus_set()

    def performance_add(self):
        self.calculation_membership()
        self.dao.debt.check_debt(
            self.entry_lot_number.get(),
            self.entry_cost_payment_debt.get(),
            self.entry_target_contribution_debt.get(),
            self.entry_membership_fee_debt.get(),
            self.entry_electricity_debt.get()
        )
        #self.callback()
        self.destroy()

    def calculation_debt(self):
        cost_payment = float(self.entry_membership_fee_debt.get()) \
                       + float(self.entry_target_contribution_debt.get()) \
                       + float(self.entry_electricity_debt.get())
        self.entry_cost_payment_debt.insert(5, cost_payment)

    def calculation_membership(self):
        owner = self.dao.owner.get_by_number(self.entry_lot_number.get())
        electricity = owner[7]
        square = owner[6]
        calculation_feedback = self.calculation(electricity, square, self.date_payment, self.entry_date_begin.get())
        membership_fee = calculation_feedback[0]
        date_begin = calculation_feedback[1]
        self.dao.payment.insert(
            self.entry_lot_number.get(), membership_fee, self.date_payment, 0,
            membership_fee, 0, date_begin, 0, membership_fee,
            self.entry_combobox_status.get(), self.entry_combobox_type.get()
        )
