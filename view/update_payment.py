import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments
from logiс.scripts import check_update_payment, update_debt_diff
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
        self.geometry('400x400+350+130')
        self.title('Редактировать позицию')
        title_label(self, 'Изменение платежа', 135, 15)
        x = 185
        self.entry_lot_number = input_payments(self, 'Номер участка:', ttk.Entry(self), x, 50)
        self.entry_cost_payment = input_payments(self, 'Сумма платежа:', ttk.Entry(self), x, 75)
        self.entry_date_payment = input_payments(self, 'Дата:', ttk.Entry(self), x, 100)
        self.entry_target_contribution = input_payments(self, 'Целевой взнос:', ttk.Entry(self), x, 125)
        self.entry_membership_fee = input_payments(self, 'Членский взнос:', ttk.Entry(self), x, 150)
        self.entry_electricity = input_payments(self, 'Элетричество:', ttk.Entry(self), x, 175)
        self.entry_date_begin = input_payments(self, 'Начальные показания:', ttk.Entry(self), x, 200)
        self.entry_date_end = input_payments(self, 'Конечные показания:', ttk.Entry(self), x, 225)
        self.entry_combobox_status = input_payments(self, 'Статус:', ttk.Combobox(self,
                                                                                  values=[u"Не оплачен",
                                                                                          u"Оплачен частично",
                                                                                          u"Оплачен"]), x, 250)
        self.entry_combobox_type = input_payments(self, 'Тип:', ttk.Combobox(self,
                                                                             values=["Выставленный",
                                                                                     "Выплаченный"]), x, 275)
        button(self, 'Редактировать', self.payment_update, 15, 135, 315)
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
        payment_begin = self.dao.payment.get_by_id(self.number)
        self.debt_update(payment_begin)
        diff = check_update_payment(self.entry_cost_payment.get(), payment_begin[9],
                                    payment_begin[4], payment_begin[5], payment_begin[6],
                                    self.entry_target_contribution.get(),
                                    self.entry_membership_fee.get(), self.entry_electricity.get()
                                    )
        self.dao.payment.update(self.find_v, diff[0], self.entry_date_payment.get(),
                                self.entry_target_contribution.get(), self.entry_membership_fee.get(),
                                self.entry_electricity.get(), self.entry_date_begin.get(), self.entry_date_end.get(),
                                diff[1], self.entry_combobox_status.get(), self.entry_combobox_type.get(),
                                self.number
                                )
        view_payments(self.window, self.tree, self.find_v)
        self.destroy()

    def debt_update(self, payment_begin):
        row = list(self.dao.debt.get_by_number(self.find_v))
        debt_id = row[1][0]
        debt = self.dao.debt.get_by_id(debt_id)
        debt_new = update_debt_diff(payment_begin[2], self.entry_cost_payment.get(), payment_begin[4],
                                    payment_begin[5], payment_begin[6],  self.entry_target_contribution.get(),
                                    self.entry_membership_fee.get(), self.entry_electricity.get(),
                                    debt[2], debt[3], debt[4], debt[5])
        self.dao.debt.update(self.find_v, round(debt_new[0], 2), round(debt_new[1], 2), round(debt_new[2], 2),
                             round(debt_new[3], 2), round(debt_new[4], 2), debt_id)
