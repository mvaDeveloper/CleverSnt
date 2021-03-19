import tkinter as tk
from view.utilities import button_main_menu, tree
from view.table_view import view_owners


class Owners(tk.Frame):
    def __init__(self, root, menu_actions, db):
        super().__init__(root)
        Menu(self, menu_actions, db)


class Menu(tk.Frame):
    def __init__(self, root, menu_actions, db):
        super().__init__(root, bg='#0099ff', bd=2)
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.db = db
        self.menu_actions = menu_actions
        self.add_img_user = tk.PhotoImage(file="./images/user.png")
        self.add_img_payment = tk.PhotoImage(file="./images/payment.png")
        self.add_img_find = tk.PhotoImage(file="./images/find.png")
        self.add_img_update = tk.PhotoImage(file="./images/update.png")
        self.add_img_delete = tk.PhotoImage(file="./images/delete.png")

        button_main_menu(self, 'Удалить собственника', self.delete, self.add_img_delete)
        button_main_menu(self, 'Обновить', self.selection_for_update, self.add_img_update)
        button_main_menu(self, 'Найти платеж', self.menu_actions.open_find_payment, self.add_img_find)
        button_main_menu(self, 'Выставить счет', self.menu_actions.open_add_payment, self.add_img_payment)
        button_main_menu(self, 'Добавить собственника', self.add_owner, self.add_img_user)

        columns = ['id', 'lot_number', 'second_name', 'first_name', 'patronymic', 'address', 'square', 'electricity']
        widths = [30, 120, 120, 120, 120, 160, 120, 100]
        names = ['id', 'Номер участка', 'Фамилия', 'Имя', 'Отчетчтво', 'Адрес', 'Площадь участка', 'Электричество']
        self.tree = tree(root, columns)
        i = 0
        for width in widths:
            self.tree.column(columns[i], width=width, anchor=tk.CENTER)
            i += 1
        i = 0
        for name in names:
            self.tree.heading(columns[i], text=name)
            i += 1

        self.tree.pack(side=tk.LEFT)
        # скролл
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        view_owners(self, self.tree)

    def add_owner(self):
        self.menu_actions.open_add_owner(self, self.tree)

    def selection_for_update(self):
        owner_id = self.tree.set(self.tree.selection()[0], '#1')
        self.menu_actions.open_update(owner_id, self, self.tree)

    def delete(self):
        owner_id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.owner.delete(owner_id)
        view_owners(self, self.tree)
