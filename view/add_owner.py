import tkinter as tk
from tkinter import ttk
from view.utilities import input_owners, title_label, button
from view.table_view import view_owners


class AddOwner(tk.Toplevel):
    def __init__(self, dao, window, tree):
        super().__init__()
        self.dao = dao
        self.window = window
        self.tree = tree
        self.title('Добавить собственника')
        self.geometry('400x320+142+30')
        tk.Toplevel.configure(self, bg="#f0eae1")
        title_label(self, 'Добавление собственника', 100, 15)
        x = 70
        self.entry_lot_number = input_owners(self, 'Номер участка:', ttk.Entry(self), x, 50)
        self.entry_second_name = input_owners(self, 'Фамилия:', ttk.Entry(self), x, 75)
        self.entry_first_name = input_owners(self, 'Имя:', ttk.Entry(self), x, 100)
        self.entry_patronymic = input_owners(self, 'Отчество:', ttk.Entry(self), x, 125)
        self.entry_address = input_owners(self, 'Адрес:', ttk.Entry(self), x, 150)
        self.entry_square = input_owners(self, 'Площадь участка:', ttk.Entry(self), x, 175)
        self.combobox_electricity = input_owners(self,
                                                 'Электричество:',
                                                 ttk.Combobox(self, values=["Есть", "Нет"]),
                                                 x,
                                                 200
                                                 )
        button(self, 'Добавить', self.on_save, 15, 140, 240)
        self.grab_set()
        self.focus_set()

    # запись информации о собственнике
    def on_save(self):
        self.dao.owner.insert(
            self.entry_lot_number.get(),
            self.entry_second_name.get(),
            self.entry_first_name.get(),
            self.entry_patronymic.get(),
            self.entry_address.get(),
            self.entry_square.get(),
            self.combobox_electricity.get()
        )
        view_owners(self.window, self.tree)
        self.destroy()
