import tkinter as tk
from tkinter import ttk
from view.utilities import title_label, button, input_payments


class UpdateElectric(tk.Toplevel):
    def __init__(self, find_v, number, dao, window, tree):
        super().__init__()
        self.find_v = find_v
        self.number = number
        self.dao = dao
        self.window = window
        self.tree = tree
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.geometry('400x180+350+370')
        self.title('Изменить информацию об электричестве')
        title_label(self, 'Изменение конечных показаний', 70, 15)
        self.entry_date_end = input_payments(self, 'Конечные показания:', ttk.Entry(self), 185, 50)
        button(self, 'Редактировать', self.update_electric, 15, 135, 90)

    def update_electric(self):
        pass
