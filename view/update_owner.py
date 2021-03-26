import tkinter as tk
from tkinter import ttk
from view.utilities import input_owners, title_label, button
from view.table_view import view_owners


class UpdateOwner(tk.Toplevel):
    def __init__(self, dao, owner_id, window, tree):
        super().__init__()
        self.dao = dao
        self.window = window
        self.tree = tree
        self.owner_id = owner_id
        self.title('Редактировать информацию о собственнике')
        self.geometry('400x320+142+328')
        tk.Toplevel.configure(self, bg="#f0eae1")
        title_label(self, 'Редактировать информацию о собственнике', 25, 15)
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
        self.default_data()
        button(self, 'Редактировать', self.on_save, 15, 120, 240)

        self.grab_set()
        self.focus_set()

    # запись информации о собственнике
    def on_save(self):
        self.dao.owner.update(
            self.entry_lot_number.get(),
            self.entry_second_name.get(),
            self.entry_first_name.get(),
            self.entry_patronymic.get(),
            self.entry_address.get(),
            self.entry_square.get(),
            self.combobox_electricity.get(),
            self.owner_id
        )
        view_owners(self.window, self.tree)
        self.destroy()

    def default_data(self):
        owner = self.dao.owner.get_by_id(self.owner_id)
        print(self)
        self.entry_lot_number.insert(0, owner[1])
        self.entry_second_name.insert(0, owner[2])
        self.entry_first_name.insert(0, owner[3])
        self.entry_patronymic.insert(0, owner[4])
        self.entry_address.insert(0, owner[5])
        self.entry_square.insert(0, owner[6])
        if owner[7] != 'Есть':
            self.combobox_electricity.current(1)
        else:
            self.combobox_electricity.current(0)
