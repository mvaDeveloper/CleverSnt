import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, set_place
import view.payments


class FindPayments(tk.Toplevel):
    def __init__(self, db):
        super().__init__()
        self.db = db
        #self.callback = callback
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.title('Найти платеж')
        self.geometry('300x300+100+100')
        title_label(self, 'Поиск платежа по номеру участка', 30, 65)
        self.find = set_place(ttk.Entry(self, width=30), 60, 110)
        button(self, 'Найти', self.performance_find, 10, 100, 150)
        self.grab_set()
        self.focus_set()

    def performance_find(self):
        view.payments.Payments(self.db, self.find.get())
        self.destroy()
