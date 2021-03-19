import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont
import dao
import qrcode


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        # картинки для основного меню
        self.tree = ttk.Treeview(
            self,
            columns=(
                'id', 'lot_number', 'second_name', 'first_name',
                'patronymic', 'address', 'square', 'electricity'
            ),
            heigh=32,
            show='headings'
        )
        self.add_img_user = tk.PhotoImage(file="C:/Users/2malu/PycharmProjects/pythonProject1/images/user.png")
        self.add_img_payment = tk.PhotoImage(file="C:/Users/2malu/PycharmProjects/pythonProject1/images/payment.png")
        self.add_img_find = tk.PhotoImage(file="C:/Users/2malu/PycharmProjects/pythonProject1/images/find.png")
        self.add_img_update = tk.PhotoImage(file="C:/Users/2malu/PycharmProjects/pythonProject1/images/update.png")
        self.add_img_delete = tk.PhotoImage(file="C:/Users/2malu/PycharmProjects/pythonProject1/images/delete.png")

        self.tool()
        self.main_table()
        self.db = db
        self.view_owners()

    # основное меню
    def tool(self):
        toolbar = tk.Frame(bg='#0099ff', bd=2)
        toolbar.pack(side=tk.LEFT, fill=tk.Y)

        btn_delete = tk.Button(
            toolbar,
            text='Удалить собственника',
            command=self.delete_owners,
            bg='#3399ff',
            bd=0,
            compound=tk.TOP,
            activebackground='#3399ff',
            image=self.add_img_delete
        )
        btn_delete.pack(side=tk.BOTTOM)

        btn_update = tk.Button(
            toolbar,
            text='Изменить',
            command=self.open_update_dialog,
            bg='#3399ff',
            bd=0,
            compound=tk.TOP,
            activebackground='#3399ff',
            image=self.add_img_update
        )
        btn_update.pack(side=tk.BOTTOM)

        btn_owner = tk.Button(
            toolbar,
            text='Добавить собственника',
            command=self.open_dialog_owner,
            bg='#3399ff',
            bd=0,
            compound=tk.TOP,
            activebackground='#3399ff',
            image=self.add_img_user
        )
        btn_owner.pack(side=tk.BOTTOM)

        btn_payment = tk.Button(
            toolbar,
            text='Выставить счет',
            command=self.open_dialog_payment,
            bg='#3399ff',
            bd=0,
            compound=tk.TOP,
            activebackground='#3399ff',
            image=self.add_img_payment
        )
        btn_payment.pack(side=tk.BOTTOM)

        btn_find = tk.Button(
            toolbar,
            text='Найти платеж',
            command=self.open_dialog_find,
            bg='#3399ff',
            bd=0,
            compound=tk.TOP,
            activebackground='#3399ff',
            image=self.add_img_find
        )
        btn_find.pack(side=tk.BOTTOM)

    # таблица в которую выводится информация о собственниках
    def main_table(self):
        # величина столбцов
        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('lot_number', width=120, anchor=tk.CENTER)
        self.tree.column('second_name', width=120, anchor=tk.CENTER)
        self.tree.column('first_name', width=120, anchor=tk.CENTER)
        self.tree.column('patronymic', width=120, anchor=tk.CENTER)
        self.tree.column('address', width=160, anchor=tk.CENTER)
        self.tree.column('square', width=120, anchor=tk.CENTER)
        self.tree.column('electricity', width=100, anchor=tk.CENTER)
        # название столбцов
        self.tree.heading('id', text='id')
        self.tree.heading('lot_number', text='Номер участка')
        self.tree.heading('second_name', text='Фамилия')
        self.tree.heading('first_name', text='Имя')
        self.tree.heading('patronymic', text='Отчетчтво')
        self.tree.heading('address', text='Адрес')
        self.tree.heading('square', text='Площадь участка')
        self.tree.heading('electricity', text='Электричество')

        self.tree.pack(side=tk.LEFT)
        # скролл
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # обновление информации о собственнике
    def update_owner(self, lot_number, second_name, first_name, patronymic, address, square, electricity):
        owner_id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.update_owner(lot_number, second_name, first_name, patronymic, address, square, electricity, owner_id)
        self.view_owners()

    # вывод информации о пользователе в таблицу
    def view_owners(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=owner) for owner in self.db.owners()]

    # удаление информаци о пользователе
    def delete_owners(self):
        for selection_item in self.tree.selection():
            id_owner = self.tree.set(selection_item, '#1')
            self.db.delete_owner(id_owner)
        self.view_owners()

    def record_payment(self, lot_number, cost_payment, date_payment, target_contribution, membership_fee, electricity,
                       date_begin, date_end, balance, status, type_payment):
        self.db.insert_payment(lot_number, cost_payment, date_payment, target_contribution, membership_fee, electricity,
                               date_begin, date_end, balance, status, type_payment)

    @staticmethod
    def open_dialog_owner():
        Owners()

    @staticmethod
    def open_dialog_payment():
        AddPay()

    @staticmethod
    def open_dialog_find():
        FindP()

    @staticmethod
    def open_update_dialog():
        Update()


class Owners(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(
            self,
            text='Добавить',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        # поля ввода
        self.combobox = ttk.Combobox(self, values=[u"Есть", u"Нет"])
        self.entry_square = ttk.Entry(self)
        self.entry_address = ttk.Entry(self)
        self.entry_patronymic = ttk.Entry(self)
        self.entry_first_name = ttk.Entry(self)
        self.entry_second_name = ttk.Entry(self)
        self.entry_lot_number = ttk.Entry(self)
        self.label_owners = tk.Label(
            self,
            bg="#f0eae1",
            text='Добавление собственника',
            font="/fonts/7454.ttf 13"
        )
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.db = db
        self.add_owner()
        self.view = app

    def add_owner(self):
        self.title('Добавить собственника')
        self.geometry('500x320+400+300')

        self.label_owners.place(x=130, y=10)
        # названия полей ввода
        label_lot_number = tk.Label(self, text='Номер участка:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_lot_number.place(x=100, y=35)
        label_second_name = tk.Label(self, text='Фамилия:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_second_name.place(x=100, y=60)
        label_first_name = tk.Label(self, text='Имя:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_first_name.place(x=100, y=85)
        label_patronymic = tk.Label(self, text='Отчество:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_patronymic.place(x=100, y=110)
        label_address = tk.Label(self, text='Адрес:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_address.place(x=100, y=135)
        label_square = tk.Label(self, text='Площадь участка:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_square.place(x=100, y=160)
        label_electricity = tk.Label(self, text='Электричество:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_electricity.place(x=100, y=185)
        # расположение полей ввода
        self.entry_lot_number.place(x=230, y=35)
        self.entry_second_name.place(x=230, y=60)
        self.entry_first_name.place(x=230, y=85)
        self.entry_patronymic.place(x=230, y=110)
        self.entry_address.place(x=230, y=135)
        self.entry_square.place(x=230, y=160)
        self.combobox.current(0)
        self.combobox.place(x=230, y=185)
        # кнопка добавления пользователя в бд
        self.btn_ok.place(x=170, y=230)
        self.btn_ok.bind('<Button-1>', lambda event: self.records_owners(
            self.entry_lot_number.get(),
            self.entry_second_name.get(),
            self.entry_first_name.get(),
            self.entry_patronymic.get(),
            self.entry_address.get(),
            self.entry_square.get(),
            self.combobox.get()), add="+"
                         )
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

        self.grab_set()
        self.focus_set()

    # запись информации о собственнике
    def records_owners(self, lot_number, second_name, first_name, patronymic, address, square, electricity):
        self.db.insert_owner(lot_number, second_name, first_name, patronymic, address, square, electricity)
        self.view.view_owners()


# изменение информации о пользователе
class Update(Owners):
    def __init__(self):
        super().__init__()
        self.btn_edit = tk.Button(
            self,
            text='Редактировать',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        self.change_owner()
        self.view = app
        self.db = db
        self.default_data()

    def change_owner(self):
        self.title('Редактировать позицию')
        self.label_owners.destroy()
        label_owners_updates = tk.Label(
            self,
            bg="#f0eae1",
            text='Редактирование информации',
            font="/fonts/7454.ttf 13"
        )
        label_owners_updates.place(x=115, y=10)
        # кнопка изменения информации о пользователе в бд
        self.btn_edit.place(x=170, y=230)
        self.btn_edit.bind('<Button-1>', lambda event: self.view.update_owner(
            self.entry_lot_number.get(),
            self.entry_second_name.get(),
            self.entry_first_name.get(),
            self.entry_patronymic.get(),
            self.entry_address.get(),
            self.entry_square.get(),
            self.combobox.get()), add="+")
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    # добавление изначальной информации в поля ввода
    def default_data(self):
        id_owner = self.view.tree.set(self.view.tree.selection()[0], '#1')
        row = self.db.get_owner_id(id_owner)
        self.entry_lot_number.insert(0, row[1])
        self.entry_second_name.insert(0, row[2])
        self.entry_first_name.insert(0, row[3])
        self.entry_patronymic.insert(0, row[4])
        self.entry_address.insert(0, row[5])
        self.entry_square.insert(0, row[6])
        if row[7] != 'Есть':
            self.combobox.current(1)


# добавление платежа
class AddPay(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.btn_ok = tk.Button(
            self,
            text='Добавить',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        self.btn_calculation = tk.Button(
            self,
            text='Рассчитать',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )

        # переменные для записи в бд
        self.date_end = 0
        self.date_payment = 'xx.yy.2021'
        # поля ввода
        self.combobox_type = ttk.Combobox(self, values=[u"Выставленный", u"Выплаченный"])
        self.combobox = ttk.Combobox(self, values=[u"Не оплачен", u"Оплачен частично", u"Оплачен"])
        self.entry_membership_fee_debt = ttk.Entry(self)
        self.entry_cost_payment_debt = ttk.Entry(self)
        self.entry_electricity_debt = ttk.Entry(self)
        self.entry_target_contribution_debt = ttk.Entry(self)
        self.entry_date_begin = ttk.Entry(self)
        self.entry_lot_number = ttk.Entry(self)
        # название полей ввода
        self.label_type_payment = tk.Label(self, text='Тип:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_status = tk.Label(self, text='Статус:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_membership_fee_debt = tk.Label(self, text='Долг членский:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_cost_payment_debt = tk.Label(self, text='Долг общий:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_electricity_debt = tk.Label(self, text='Долг электричество:', bg="#f0eae1",
                                               font="/fonts/7454.ttf 11")
        self.label_target_contribution_debt = tk.Label(self, text='Долг целевой:', bg="#f0eae1",
                                                       font="/fonts/7454.ttf 11")
        self.label_date_begin = tk.Label(self, text='Начальные показания:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_payment = tk.Label(
            self,
            bg="#f0eae1",
            text='Выставление счета',
            font="/fonts/7454.ttf 13"
        )

        tk.Toplevel.configure(self, bg="#f0eae1")
        self.init_child_payment()
        self.view_payment = app
        self.db = db

    def init_child_payment(self):
        self.title('Выставление счета')
        self.geometry('450x350+400+300')

        self.label_payment.place(x=120, y=10)

        # название полей ввода
        label_lot_number = tk.Label(self, text='Номер участка:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_lot_number.place(x=60, y=40)
        self.label_date_begin.place(x=60, y=65)
        self.label_membership_fee_debt.place(x=60, y=90)
        self.label_target_contribution_debt.place(x=60, y=115)
        self.label_electricity_debt.place(x=60, y=140)
        self.label_cost_payment_debt.place(x=60, y=165)
        self.label_status.place(x=60, y=190)
        self.label_type_payment.place(x=60, y=215)
        # поля ввода
        self.entry_lot_number.place(x=220, y=40)
        self.entry_date_begin.place(x=220, y=65)
        self.entry_membership_fee_debt.place(x=220, y=90)
        self.entry_target_contribution_debt.place(x=220, y=115)
        self.entry_electricity_debt.place(x=220, y=140)
        self.entry_cost_payment_debt.place(x=220, y=165)
        self.combobox.current(0)
        self.combobox.place(x=220, y=190)
        self.combobox_type.current(0)
        self.combobox_type.place(x=220, y=215)

        self.btn_ok.place(x=255, y=260)
        # автоматический рассчет невведенных
        self.btn_ok.bind('<Button-1>', lambda event1: self.calculation(
            self.entry_lot_number.get(),
            self.date_payment,
            self.entry_date_begin.get(),
            self.date_end,
            self.combobox.get(),
            self.combobox_type.get()), add="+")
        self.btn_ok.bind('<Button-1>', lambda event2: self.update_debt(
            self.entry_lot_number.get(),
            self.entry_cost_payment_debt.get(),
            self.entry_target_contribution_debt.get(),
            self.entry_membership_fee_debt.get(),
            self.entry_electricity_debt.get()), add="+")
        self.btn_ok.bind('<Button-1>', lambda event3: self.destroy(), add='+')
        self.btn_calculation.bind('<Button-1>',
                                  lambda event: self.calculation_debt(
                                      self.entry_membership_fee_debt.get(),
                                      self.entry_target_contribution_debt.get(),
                                      self.entry_electricity_debt.get()), add="+")
        self.btn_calculation.place(x=65, y=260)
        self.grab_set()
        self.focus_set()

    def calculation_debt(self, membership_fee, target_contribution, electricity):
        cost_payment = float(membership_fee) + float(target_contribution) + float(electricity)
        self.entry_cost_payment_debt.insert(5, cost_payment)

    # автоматический рассчет невведенных
    def calculation(self, lot_number, date_payment, date_begin, date_end, status, type_payment):
        target_contribution = 0
        year = int(date_payment[-2] + date_payment[-1])
        row = self.db.get_owner_number(lot_number)
        electricity = row[7]
        square = row[6]
        # если введено пустое значение преобразовать его в 0
        if date_begin == "":
            date_begin = 0
        else:
            date_begin = float(date_begin)
        # проверка наличия электричества
        if electricity == "Есть":
            flag = 1
        else:
            flag = 0
        # рассчет членского взноса исходя из года и коэфициента
        if year == 20:
            if flag == 1:
                membership_fee = square * 4.50
            else:
                membership_fee = square * 4
        else:
            if flag == 1:
                membership_fee = square * 5
            else:
                membership_fee = square * 4.5
        # так как нам не известны конечные показания
        electricity = 0
        cost_payment = target_contribution + membership_fee + electricity
        balance = cost_payment

        self.view_payment.record_payment(lot_number, cost_payment, date_payment, target_contribution, membership_fee,
                                         electricity, date_begin, date_end, balance, status, type_payment)

    def update_debt(self, lot_number, cost_payment, target_contribution, membership_fee, electricity):

        row = self.db.get_debt_number(lot_number)

        if row == []:
            self.record_debt(lot_number, cost_payment, target_contribution, membership_fee, electricity, cost_payment)
            self.record_debt(lot_number, cost_payment, target_contribution, membership_fee, electricity, cost_payment)
        else:
            id_debt = row[0]
            self.db.update_debt(lot_number, cost_payment, target_contribution,
                                membership_fee, electricity, cost_payment, id_debt)

    def record_debt(self, lot_number, cost_payment, target_contribution, membership_fee, electricity, balance):
        self.db.insert_debt(lot_number, cost_payment, target_contribution, membership_fee, electricity, balance)


# поиск платежей по номеру участка
class FindP(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.find = ttk.Entry(
            self,
            width=30
        )
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.find_payment()

    def find_payment(self):
        self.title('Найти платеж')
        self.geometry('300x300+100+100')

        label_find = tk.Label(
            self,
            bg="#f0eae1",
            text='Поиск платежа по номеру участка',
            font="/fonts/7454.ttf 11"
        )
        label_find.place(x=30, y=65)

        self.find.place(x=60, y=110)

        btn_find = tk.Button(
            self,
            text='Найти',
            width=10,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        btn_find.place(x=100, y=150)
        btn_find.bind('<Button-1>', lambda event: self.open_dialog_pay(self.find.get()), add='+')
        btn_find.bind('<Button-1>', lambda event: self.destroy(), add='+')

        # self.grab_set()
        self.focus_set()

    @staticmethod
    def open_dialog_pay(find_v):
        Payments(find_v)


# личная карточка платежей собственника
class Payments(tk.Toplevel):
    def __init__(self, find_v):
        super().__init__(root)
        # название колонок в таблице
        self.tree = ttk.Treeview(
            self,
            columns=('id', 'cost_payment', 'date_payment', 'target_contribution', 'membership_fee',
                     'electricity', 'date_begin', 'date_end', 'balance', 'status', 'type_payment'),
            heigh=30,
            show='headings'
        )
        # кновка удаление платежа
        self.btn_delete = tk.Button(
            self,
            text='Удалить платеж',
            width=25, height=6,
            activebackground='#3399ff',
            background="#0099ff"
        )
        # кнопка изменения платежа
        self.btn_change = tk.Button(
            self,
            text='Изменить платеж',
            width=25, height=6,
            background="#0099ff",
            activebackground='#3399ff'
        )
        # кнопка добавления оплаченного платежа
        self.btn_diversity = tk.Button(
            self,
            text='Разнести платеж',
            width=25, height=6,
            background="#0099ff",
            activebackground='#3399ff'
        )
        # кнопка формирования квитанции
        self.btn_receipt = tk.Button(
            self,
            text='Сформировать квитанцию',
            width=25, height=6,
            background="#0099ff",
            activebackground='#3399ff'
        )
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.find_v = find_v
        self.menu()
        self.table_pay()
        self.db = db
        self.view_payment_information()

    def menu(self):
        # кнопка формирования квитанции
        self.btn_receipt.place(x=1, y=30)
        self.btn_receipt.bind('<Button-1>', lambda event: self.open_choice_rec(self.find_v), add="+")
        # кнопка добавления оплаченного платежа
        self.btn_diversity.place(x=1, y=150)
        self.btn_diversity.bind('<Button-1>', lambda event: self.open_diversity_pay(self.find_v), add="+")
        self.btn_diversity.bind('<Button-1>', lambda event: self.destroy(), add="+")
        # кнопка изменения платежа
        self.btn_change.place(x=1, y=270)
        self.btn_change.bind('<Button-1>', lambda event: self.open_update_pay(self.find_v))
        self.btn_change.bind('<Button-1>', lambda event: self.destroy(), add="+")
        # кнопка удаления платежа
        self.btn_delete.place(x=1, y=390)
        self.btn_delete.bind('<Button-1>', lambda event: self.delete_owners_pay(), add="+")

    # таблица с платежами
    def table_pay(self):
        self.title('Квитанции участка № ' + str(self.find_v))
        self.geometry('1500x520+10+300')
        # ширина столбцов
        self.tree.column('id', width=40, anchor=tk.CENTER)
        self.tree.column('cost_payment', width=110, anchor=tk.CENTER)
        self.tree.column('date_payment', width=110, anchor=tk.CENTER)
        self.tree.column('target_contribution', width=110, anchor=tk.CENTER)
        self.tree.column('membership_fee', width=100, anchor=tk.CENTER)
        self.tree.column('electricity', width=130, anchor=tk.CENTER)
        self.tree.column('date_begin', width=130, anchor=tk.CENTER)
        self.tree.column('date_end', width=130, anchor=tk.CENTER)
        self.tree.column('balance', width=80, anchor=tk.CENTER)
        self.tree.column('status', width=130, anchor=tk.CENTER)
        self.tree.column('type_payment', width=90, anchor=tk.CENTER)
        # скролл
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        # название столбцов
        self.tree.heading('id', text='id')
        self.tree.heading('cost_payment', text='Сумма платежа')
        self.tree.heading('date_payment', text='Дата платежа')
        self.tree.heading('target_contribution', text='Целевой взнос')
        self.tree.heading('membership_fee', text='Членский взнос')
        self.tree.heading('electricity', text='Плата электричество')
        self.tree.heading('date_begin', text='Начальные показания')
        self.tree.heading('date_end', text='Конечные показания')
        self.tree.heading('balance', text='Сальдо')
        self.tree.heading('status', text='Статус')
        self.tree.heading('type_payment', text='Тип')

        self.tree.pack(side=tk.RIGHT)

    # вывод платежей в таблицу
    def view_payment_information(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        i = 0
        for debt in self.db.get_debt_number(self.find_v):
            i += 1
            debt_list = list(debt)
            del debt_list[1]
            debt_list.insert(2, '')
            debt_list.insert(6, '')
            debt_list.insert(7, '')
            debt_list.insert(9, '')
            debt_list.insert(10, 'Долг')
            self.tree.insert('', 'end', values=debt_list)
            if i == 1:
                for payment in self.db.get_payment_number(self.find_v):
                    payment_list = list(payment)
                    del payment_list[1]
                    self.tree.insert('', 'end', values=payment_list)

    # запись изменений информации о платежах
    def payment_update(
            self, lot_number, cost_payment, date_payment, target_contribution,
            membership_fee, electricity, date_begin, date_end, balance, status, type_payment, number):
        self.db.update_payment(lot_number, cost_payment, date_payment, target_contribution, membership_fee, electricity,
                               date_begin, date_end, balance, status, type_payment, number)
        self.view_payment_information()

    # уделение информации о платежах
    def delete_owners_pay(self):
        for selection_item in self.tree.selection():
            self.db.delete_payment((self.tree.set(selection_item, '#1'),))
        self.view_payment_information()

    # вызов класса изменения информации о платежах
    def open_update_pay(self, find_v):
        UpdatePayment(find_v, (self.tree.set(self.tree.selection()[0], '#1'),))

    # вызов класса добавления оплаченных платежей
    @staticmethod
    def open_diversity_pay(find_v):
        DiversityP(find_v)

    # выбор типа квитанции
    def open_choice_rec(self, find_v):
        ChoiceReceipt(find_v, (self.tree.set(self.tree.selection()[0], '#1'),))


# выбор типа квитанции
class ChoiceReceipt(tk.Toplevel):
    def __init__(self, find_v, number):
        super().__init__(root)
        tk.Toplevel.configure(self, bg="#f0eae1")
        self.find_v = find_v
        self.number = number
        self.db = db
        self.choice()

    def choice(self):
        self.title('Выбор типа квитанции')
        self.geometry('400x200+100+100')

        label_find = tk.Label(
            self,
            bg="#f0eae1",
            text='Выбор типа квитанции',
            font="/fonts/7454.ttf 11"
        )
        label_find.place(x=115, y=45)

        btn_main = tk.Button(
            self,
            text='Главная',
            width=16,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        btn_main.place(x=40, y=120)
        btn_main.bind('<Button-1>', lambda event: self.choice_receipt(1), add='+')
        btn_main.bind('<Button-1>', lambda event: self.destroy(), add='+')

        btn_indebt = tk.Button(
            self,
            text='Дополнительная',
            width=16,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        btn_indebt.place(x=210, y=120)
        btn_indebt.bind('<Button-1>', lambda event: self.choice_receipt(0), add='+')
        btn_indebt.bind('<Button-1>', lambda event: self.destroy(), add='+')

        # self.grab_set()
        self.focus_set()

    # выбор типа квитанции
    def choice_receipt(self, flag):

        if flag:
            payment = self.db.get_payment_id(self.number[0])
            owner = self.db.get_owner_number(payment[1])
            self.draw_receipt_main(payment[1], payment[2], payment[3], payment[5], payment[6],
                                   payment[7], payment[8], payment[8] - payment[7], owner[3],
                                   owner[4], owner[5], owner[2])
        else:
            row = self.db.get_debt_number(self.find_v)
            debt = self.db.get_debt_id(row[1][0])
            owner = self.db.get_owner_number(self.find_v)
            self.draw_receipt_optional(debt[1], debt[2], owner[3], owner[4], owner[5], owner[2])

    # создание квитанции

    @staticmethod
    def draw_receipt_main(lot_number, cost_payment, date_payment, membership_fee, electricity, date_begin,
                          date_end, difference, second_name, patronymic, address, first_name):
        img_receipt = Image.open('images/snt.jpeg')
        idraw = ImageDraw.Draw(img_receipt)
        headline = ImageFont.truetype('arial.ttf', size=100)

        # извещение
        idraw.text((3150, 1350), str(cost_payment), font=headline)
        idraw.text((3100, 750), str(membership_fee), font=headline)
        idraw.text((3110, 990), str(electricity), font=headline)
        idraw.text((2390, 990), str(difference), font=headline)
        idraw.text((2390, 1110), str(date_begin), font=headline)
        idraw.text((2390, 1230), str(date_end), font=headline)
        idraw.text((4000, 500), lot_number, font=headline)
        idraw.text((1550, 1460), date_payment, font=headline)
        idraw.text((1920, 500), second_name + " " + first_name + " " + patronymic, font=headline)
        idraw.text((1920, 620), address, font=headline)
        # квитанция
        idraw.text((3150, 2900), str(cost_payment), font=headline)
        idraw.text((3100, 2300), str(membership_fee), font=headline)
        idraw.text((3110, 2540), str(electricity), font=headline)
        idraw.text((2390, 2540), str(difference), font=headline)
        idraw.text((2390, 2660), str(date_begin), font=headline)
        idraw.text((2390, 2780), str(date_end), font=headline)
        idraw.text((4000, 2050), lot_number, font=headline)
        idraw.text((1550, 3010), date_payment, font=headline)
        idraw.text((1920, 2050), second_name + " " + first_name + " " + patronymic, font=headline)
        idraw.text((1920, 2170), address, font=headline)

        # qrcode
        data = "ST00012|Name=Садоводческое некомерческое товарищество\"Приморскре\"|" \
               "PersonalAcc=40703810416020000062|BankName=Центрально-Черназемный филиал ООО \"Экспобанк\"|" \
               "lastName=" + second_name + "|firstName=" + first_name + "|middleName=" + patronymic + \
               "|BIC=043807330|KPP=461101001|PayeeINN=4631011178|Sum=" + str(cost_payment)
        img_qr = qrcode.make(data)
        img_receipt.paste(img_qr, (100, 500))
        img_receipt.paste(img_qr, (100, 2200))

        name_receipt = "receipt/" + second_name + "_" + str(lot_number) + "_" + date_payment + ".png"

        img_receipt.show()
        img_receipt.save(name_receipt)

    @staticmethod
    def draw_receipt_optional(lot_number, cost_payment, second_name, patronymic, address, first_name, ):
        img_receipt = Image.open('images/snt.jpeg')
        idraw = ImageDraw.Draw(img_receipt)
        headline = ImageFont.truetype('arial.ttf', size=100)

        # извещение
        idraw.text((3150, 1350), str(cost_payment), font=headline)

        idraw.text((4000, 500), lot_number, font=headline)
        idraw.text((1920, 500), second_name + " " + first_name + " " + patronymic, font=headline)
        idraw.text((1920, 620), address, font=headline)
        # квитанция
        idraw.text((3150, 2900), str(cost_payment), font=headline)
        idraw.text((4000, 2050), lot_number, font=headline)
        idraw.text((1920, 2050), second_name + " " + first_name + " " + patronymic, font=headline)
        idraw.text((1920, 2170), address, font=headline)

        # qrcode
        data = "ST00012|Name=Садоводческое некомерческое товарищество\"Приморскре\"|" \
               "PersonalAcc=40703810416020000062|BankName=Центрально-Черназемный филиал ООО \"Экспобанк\"|" \
               "lastName=" + second_name + "|firstName=" + first_name + "|middleName=" + patronymic + \
               "|BIC=043807330|KPP=461101001|PayeeINN=4631011178|Sum=" + str(cost_payment)
        img_qr = qrcode.make(data)
        img_receipt.paste(img_qr, (100, 500))
        img_receipt.paste(img_qr, (100, 2200))

        name_receipt = "receipt/" + second_name + "_" + str(lot_number) + "_" + ".png"

        img_receipt.show()
        img_receipt.save(name_receipt)


# обновление данных платежа
class UpdatePayment(AddPay):
    def __init__(self, find_v, number):
        super().__init__()
        self.btn_edit = tk.Button(
            self,
            text='Редактировать',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        # поля ввода
        self.entry_date_end = ttk.Entry(self)
        self.entry_cost_payment = ttk.Entry(self)
        self.entry_electricity = ttk.Entry(self)
        self.entry_membership_fee = ttk.Entry(self)
        self.entry_target_contribution = ttk.Entry(self)
        self.entry_date_payment = ttk.Entry(self)
        # название полей ввода
        self.label_cost_payment = tk.Label(self, text='Сумма:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_electricity = tk.Label(self, text='Электричество:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_date_end = tk.Label(self, text='Конечные показания:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_payment_edit = tk.Label(
            self,
            bg="#f0eae1",
            text='Изменение платежа',
            font="/fonts/7454.ttf 13"
        )
        self.find_v = find_v
        self.number = number
        self.view = Payments(find_v)
        self.vi = app
        self.change_payment()
        self.db = db
        self.default_data()

    def change_payment(self):
        self.geometry('450x400+400+300')
        self.title('Редактировать позицию')

        self.entry_cost_payment_debt.destroy()
        self.entry_electricity_debt.destroy()
        self.entry_membership_fee_debt.destroy()
        self.entry_target_contribution_debt.destroy()
        self.label_cost_payment_debt.destroy()
        self.label_membership_fee_debt.destroy()
        self.label_electricity_debt.destroy()
        self.label_target_contribution_debt.destroy()
        self.btn_calculation.destroy()
        self.btn_ok.destroy()

        self.label_payment.destroy()
        self.label_payment_edit.place(x=170, y=10)

        # название полей ввода
        label_date_payment = tk.Label(self, text='Дата платежа:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_date_payment.place(x=60, y=65)
        self.label_date_end.place(x=60, y=115)
        label_target_contribution = tk.Label(self, text='Целевой взнос:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_target_contribution.place(x=60, y=140)
        label_membership_fee = tk.Label(self, text='Членский взнос:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_membership_fee.place(x=60, y=165)
        self.label_electricity.place(x=60, y=190)
        self.label_cost_payment.place(x=60, y=215)
        self.label_date_begin.place(x=60, y=90)
        self.label_type_payment.place(x=60, y=240)
        self.label_status.place(x=60, y=265)

        # поля ввода
        self.entry_date_payment.place(x=220, y=65)
        self.entry_date_begin.place(x=220, y=90)
        self.entry_date_end.place(x=220, y=115)
        self.entry_target_contribution.place(x=220, y=140)
        self.entry_membership_fee.place(x=220, y=165)
        self.entry_electricity.place(x=220, y=190)
        self.entry_cost_payment.place(x=220, y=215)
        self.combobox_type.place(x=220, y=240)
        self.combobox.place(x=220, y=265)

        self.btn_edit.place(x=150, y=315)
        # обновление информации о платеже
        self.btn_edit.bind('<Button-1>', lambda event: self.change_electricity(
            self.entry_lot_number.get(),
            self.entry_cost_payment.get(),
            self.entry_date_payment.get(),
            self.entry_target_contribution.get(),
            self.entry_membership_fee.get(),
            self.entry_electricity.get(),
            self.entry_date_begin.get(),
            self.entry_date_end.get(),
            self.combobox.get(),
            self.combobox_type.get(),
            self.number), add="+")
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add="+")
        self.btn_ok.destroy()

    # заполнение полей ввода исходной информацией
    def default_data(self):
        row = self.db.get_payment_id(self.number[0])
        self.entry_lot_number.insert(0, row[1])
        self.entry_cost_payment.insert(0, row[2])
        self.entry_date_payment.insert(0, row[3])
        self.entry_target_contribution.insert(0, row[4])
        self.entry_membership_fee.insert(0, row[5])
        self.entry_electricity.insert(0, row[6])
        self.entry_date_begin.insert(0, row[7])
        self.entry_date_end.insert(0, row[8])

        if row[9] != 'Не оплачен':
            if row[9] != 'Оплачен частично':
                self.combobox.current(2)
            if row[9] != 'Оплачен':
                self.combobox.current(1)
        if row[9] == 'Не оплачен':
            self.combobox.current(0)

    def change_electricity(
            self, lot_number, cost_payment, date_payment, target_contribution,
            membership_fee, electricity, date_begin, date_end, status, type_payment, number):
        if self.information_electricity_end() == 0:
            year = int(date_payment[-2] + date_payment[-1])
            rate_kvt = 2.91
            if self.electricity_availability(lot_number) == "Есть":
                flag = 1
            else:
                flag = 0
            if flag:
                if year == 20 or year == 21:
                    electricity = (float(date_end) - float(date_begin)) * rate_kvt
                else:
                    electricity = -1
            else:
                electricity = 0

            cost_payment = float(cost_payment) + electricity
            balance = self.information_balance() + electricity
        else:
            balance = self.information_balance()
        self.debt_update(lot_number, cost_payment, date_payment, target_contribution, membership_fee, electricity,
                         date_begin, date_end, balance, status, type_payment, number)

    def debt_update(self, lot_number, cost_payment, date_payment, target_contribution,
                    membership_fee, electricity, date_begin, date_end, balance,
                    status, type_payment, number):
        row = list(self.db.get_debt_number(lot_number))
        debt_id = row[1][0]
        debt = self.db.get_debt_id(debt_id)
        self.db.update_debt(lot_number, debt[2] + float(cost_payment), debt[3] + float(target_contribution),
                            debt[4] + float(membership_fee), debt[5] + float(electricity), balance, debt_id)
        self.view.payment_update(lot_number, cost_payment, date_payment, target_contribution,
                                 membership_fee, electricity, date_begin, date_end, balance,
                                 status, type_payment, number)

    def information_electricity_end(self):
        row = self.db.get_payment_id(self.number[0])
        return row[8]

    def electricity_availability(self, lot_number):
        row = self.db.get_owner_number(lot_number)
        return row[7]

    def information_balance(self):
        row = self.db.get_payment_id(self.number[0])
        return row[9]


# добавление информации об оплаченном платеже
class DiversityP(AddPay):
    def __init__(self, find_v):
        super().__init__()
        self.btn_calculation_cost = tk.Button(
            self,
            text='Посчитать сумму',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        self.btn_diversity = tk.Button(
            self,
            text='Разнести',
            width=15,
            height=2,
            background="#0099ff",
            font="/fonts/7454.ttf 11"
        )
        # поля ввода
        self.entry_cost_payment = ttk.Entry(self)
        self.entry_electricity = ttk.Entry(self)
        self.entry_target_contribution = ttk.Entry(self)
        self.entry_membership_fee = ttk.Entry(self)
        self.entry_date_payment = ttk.Entry(self)
        # название полей ввода
        self.label_cost_payment = tk.Label(self, text='Сумма:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_electricity = tk.Label(self, text='Электричество:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_target_contribution = tk.Label(self, text='Целевой взнос:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_membership_fee = tk.Label(self, text='Членский взнос:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        self.label_diversity_edit = tk.Label(
            self,
            bg="#f0eae1",
            text='Разнести платеж',
            font="/fonts/7454.ttf 13"
        )
        self.find_v = find_v
        self.view = Payments(find_v)
        self.vi = app
        self.init_edit()
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Разнести платеж')
        self.geometry('450x350+400+300')

        # убирает ненужные элемены
        self.label_payment.destroy()
        self.label_date_begin.destroy()
        self.entry_date_begin.destroy()
        self.entry_cost_payment_debt.destroy()
        self.entry_electricity_debt.destroy()
        self.entry_membership_fee_debt.destroy()
        self.entry_target_contribution_debt.destroy()
        self.label_cost_payment_debt.destroy()
        self.label_membership_fee_debt.destroy()
        self.label_electricity_debt.destroy()
        self.label_target_contribution_debt.destroy()
        self.btn_calculation.destroy()
        self.btn_ok.destroy()
        # название полей ввода
        self.label_diversity_edit.place(x=170, y=10)
        label_date_payment = tk.Label(self, text='Дата платежа:', bg="#f0eae1", font="/fonts/7454.ttf 11")
        label_date_payment.place(x=60, y=65)
        self.label_membership_fee.place(x=60, y=90)
        self.label_target_contribution.place(x=60, y=115)
        self.label_electricity.place(x=60, y=140)
        self.label_cost_payment.place(x=60, y=165)
        self.label_status.destroy()
        self.label_type_payment.destroy()
        # поля ввода
        self.entry_date_payment.place(x=220, y=65)
        self.entry_membership_fee.place(x=220, y=90)
        self.entry_target_contribution.place(x=220, y=115)
        self.entry_electricity.place(x=220, y=140)
        self.entry_cost_payment.place(x=220, y=165)
        self.combobox.destroy()
        self.combobox_type.destroy()
        self.btn_diversity.place(x=255, y=255)
        # создание платежа
        self.btn_diversity.bind('<Button-1>', lambda event: self.making_payment(
            self.entry_date_payment.get(),
            self.entry_membership_fee.get(),
            self.entry_target_contribution.get(),
            self.entry_electricity.get(),
            self.entry_cost_payment.get()), add="+")
        self.btn_diversity.bind('<Button-1>', lambda event: self.destroy(), add="+")
        # вычисление суммы платежа
        self.btn_calculation_cost.bind('<Button-1>', lambda event: self.calculation_cost(
            self.entry_membership_fee.get(),
            self.entry_target_contribution.get(),
            self.entry_electricity.get()), add="+")
        self.btn_calculation_cost.place(x=65, y=255)

        self.btn_ok.destroy()

    # изначальная информация о номере участке
    def default_data(self):
        self.entry_lot_number.insert(0, self.find_v)

    # вычисление суммы платежа
    def calculation_cost(self, entry_membership_fee, entry_target_contribution, entry_electricity):
        cost_payment = float(entry_membership_fee) + float(entry_target_contribution) + float(entry_electricity)
        self.entry_cost_payment.insert(5, cost_payment)

    # нахождение id последнего платежа
    def find_last_payment(self):
        row = self.db.get_payment_number(self.find_v)
        return len(row)

    # создание платежа
    def making_payment(self, date_payment, membership_fee, target_contribution, electricity, cost_payment):
        row = self.db.get_payment_id(self.find_last_payment())
        balance = round(float(row[9]), 2)
        status = 'Оплачен'
        type_payment = 'Выплаченный'
        # сальдо = начальное сальдо - сумма платежа
        balance = round(balance - float(cost_payment), 2)
        self.vi.record_payment(self.find_v, cost_payment, date_payment, target_contribution,
                               membership_fee, electricity, 0, 0, balance, status, type_payment)
        self.debt_update(cost_payment, target_contribution, membership_fee, electricity, balance)
        self.view.view_payment_information()

    def debt_update(self, cost_payment, target_contribution,
                    membership_fee, electricity, balance,
                    ):
        row = list(self.db.get_debt_number(self.find_v))
        debt_id = row[1][0]
        debt = self.db.get_debt_id(debt_id)
        self.db.update_debt(self.find_v, debt[2] - float(cost_payment), debt[3] - float(target_contribution),
                            debt[4] - float(membership_fee), debt[5] - float(electricity), balance, debt_id)


if __name__ == "__main__":
    root = tk.Tk()
    db = dao.DB()
    app = Main(root)
    app.pack()
    root.title("Clever SNT")
    root.geometry("1050x650+250+100")
    root.mainloop()
