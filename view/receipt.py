import tkinter as tk
from view.utilities import title_label, button
from view.draw_receipt import main, optional


class ChoiceReceipt(tk.Toplevel):
    def __init__(self, dao, find_v, number):
        super().__init__()
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.find_v = find_v
        self.number = number
        self.dao = dao
        self.title('Выбор типа квитанции')
        self.geometry('400x200+100+100')
        title_label(self, 'Выбор типа квитанции', 115, 45)
        button(self, 'Главная', self.choice_first, 16, 40, 120)
        button(self, 'Дополнительная', self.choice_second, 16, 210, 120)

        self.focus_set()

    def choice_first(self):
        self.choice_receipt(1)

    def choice_second(self):
        self.choice_receipt(0)

    def choice_receipt(self, flag):
        row = self.dao.debt.get_by_number(self.find_v)
        if flag:
            debt = self.dao.debt.get_by_id(row[0][0])
            payment = self.dao.payment.get_by_id(self.number)
            owner = self.dao.owner.get_by_number(payment[1])
            main(payment[1], payment[2], payment[3], payment[5], payment[6],
                 payment[7], payment[8], payment[8] - payment[7], owner[3],
                 owner[4], owner[5], owner[2], debt[2])
        else:
            debt = self.dao.debt.get_by_id(row[1][0])
            owner = self.dao.owner.get_by_number(self.find_v)
            optional(debt[1], debt[2], owner[3], owner[4], owner[5], owner[2])
        self.destroy()
