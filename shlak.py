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
        self.title('Квитанции участка № '+str(self.find_v))
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
        #скролл
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
        for selection_item in self.tree.selection_for_update():
            self.db.delete_payment((self.tree.set(selection_item, '#1'),))
        self.view_payment_information()

    # вызов класса изменения информации о платежах
    def open_update_pay(self, find_v):
        UpdatePayment(find_v, (self.tree.set(self.tree.selection_for_update()[0], '#1'),))

    # вызов класса добавления оплаченных платежей
    @staticmethod
    def open_diversity_pay(find_v):
        DiversityP(find_v)

    # выбор типа квитанции
    def open_choice_rec(self, find_v):
        ChoiceReceipt(find_v, (self.tree.set(self.tree.selection_for_update()[0], '#1'),))


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
        self.db.update_debt(lot_number, debt[2]+float(cost_payment), debt[3]+float(target_contribution),
                            debt[4]+float(membership_fee), debt[5]+float(electricity), balance, debt_id)
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



    #обновление информации о собственнике
    def update_owner(self, lot_number, second_name, first_name, patronymic, address, square, electricity):
        owner_id = self.tree.set(self.tree.selection_for_update()[0], '#1')
        self.db.update_owner(lot_number, second_name, first_name, patronymic, address, square, electricity, owner_id)
        self.view_owners()

    # вывод информации о пользователе в таблицу
    def view_owners(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=owner) for owner in self.db.owners()]

    # удаление информаци о пользователе
    def delete_owners(self):
        for selection_item in self.tree.selection_for_update():
            id_owner = self.tree.set(selection_item, '#1')
            self.db.delete_owner(id_owner)
        self.view_owners()


    def open_dialog_owner(self):
        AddOwner(self.db, self.view_owners)

    @staticmethod
    def open_dialog_payment():
        AddPay()

    @staticmethod
    def open_dialog_find():
        FindP()
        #после выполнения файнд вызывается класс пэйментс
        Payments(find_v)


    def open_update_dialog(self):
        id_owner = self.tree.set(self.tree.selection_for_update()[0], '#1')
        Update()


