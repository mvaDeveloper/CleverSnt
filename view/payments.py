import tkinter as tk
from view.table_view import view_payments
from view.utilities import button_menu, tree
from view.payments_actions import PaymentsMenuActions


class Payments(tk.Toplevel):
    def __init__(self, db, find_v):
        super().__init__()
        self.find_v = find_v
        self.db = db
        self.title('Квитанции участка № ' + str(self.find_v))
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.geometry('1410x670+110+0')
        Menu(self, find_v, self.db)


class Menu:
    def __init__(self, root, find_v, db):
        self.db = db
        self.action = PaymentsMenuActions
        self.btn_receipt = button_menu(root, 'Сформировать квитанцию', self.receipt, find_v, 1, 0)
        self.btn_diversity = button_menu(root, 'Разнести платеж', self.action.diversity_payment, find_v, 1, 120)
        self.btn_change = button_menu(root, 'Изменить платеж', self.update, find_v, 1, 240)
        self.btn_delete = button_menu(root, 'Удалить платеж', self.delete, find_v, 1, 360)

        columns = ['id', 'cost_payment', 'date_payment', 'target_contribution', 'membership_fee', 'electricity',
                   'date_begin', 'date_end', 'balance', 'status', 'type_payment']
        widths = [30, 110, 110, 110, 100, 130, 130, 130, 80, 130, 90]
        names = ['id', 'Сумма платежа', 'Дата платежа', 'Целевой взнос', 'Членский взнос', 'Плата электричество',
                 'Начальные показания', 'Конечные показания', 'Сальдо', 'Статус', 'Тип']
        self.tree = tree(root, columns)
        i = 0
        for width in widths:
            self.tree.column(columns[i], width=width, anchor=tk.CENTER)
            i += 1
        i = 0
        for name in names:
            self.tree.heading(columns[i], text=name)
            i += 1
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side=tk.RIGHT)
        view_payments(self, self.tree, find_v)

    def delete(self, find_v):
        payment_id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.payment.delete(payment_id)
        view_payments(self, self.tree, find_v)

    def update(self, find_v):
        payment_id = self.tree.set(self.tree.selection()[0], '#1')
        self.action.open_update_pay(find_v, payment_id, self, self.tree)

    def receipt(self, find_v):
        payment_id = self.tree.set(self.tree.selection()[0], '#1')
        self.action.receipt(find_v, payment_id)
