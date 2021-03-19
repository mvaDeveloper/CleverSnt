import tkinter as tk
from view.utilities import title_label, button
from PIL import Image, ImageDraw, ImageFont
import qrcode


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
        self.destroy()

    def choice_second(self):
        self.choice_receipt(0)
        self.destroy()

    # выбор типа квитанции
    def choice_receipt(self, flag):
        if flag:
            payment = self.dao.payment.get_by_id(self.number[0])
            owner = self.dao.owner.get_by_number(payment[1])
            self.draw_receipt_main(payment[1], payment[2], payment[3], payment[5], payment[6],
                                   payment[7], payment[8], payment[8] - payment[7], owner[3],
                                   owner[4], owner[5], owner[2])
        else:
            row = self.dao.debt.get_by_number(self.find_v)
            debt = self.dao.debt.get_by_id(row[1][0])
            owner = self.dao.get_by_number(self.find_v)
            self.draw_receipt_optional(debt[1], debt[2], owner[3], owner[4], owner[5], owner[2])

    # создание квитанции
    @staticmethod
    def draw_receipt_main(lot_number, cost_payment, date_payment, membership_fee, electricity, date_begin,
                          date_end, difference, second_name, patronymic, address, first_name):
        img_receipt = Image.open('images/snt.jpeg')
        draw = ImageDraw.Draw(img_receipt)
        headline = ImageFont.truetype('arial.ttf', size=100)
        # извещение
        draw.text((3150, 1350), str(cost_payment), font=headline)
        draw.text((3100, 750), str(membership_fee), font=headline)
        draw.text((3110, 990), str(electricity), font=headline)
        draw.text((2390, 990), str(difference), font=headline)
        draw.text((2390, 1110), str(date_begin), font=headline)
        draw.text((2390, 1230), str(date_end), font=headline)
        draw.text((4000, 500), lot_number, font=headline)
        draw.text((1550, 1460), date_payment, font=headline)
        draw.text((1920, 500), second_name + " " + first_name + " " + patronymic, font=headline)
        draw.text((1920, 620), address, font=headline)
        # квитанция
        draw.text((3150, 2900), str(cost_payment), font=headline)
        draw.text((3100, 2300), str(membership_fee), font=headline)
        draw.text((3110, 2540), str(electricity), font=headline)
        draw.text((2390, 2540), str(difference), font=headline)
        draw.text((2390, 2660), str(date_begin), font=headline)
        draw.text((2390, 2780), str(date_end), font=headline)
        draw.text((4000, 2050), lot_number, font=headline)
        draw.text((1550, 3010), date_payment, font=headline)
        draw.text((1920, 2050), second_name + " " + first_name + " " + patronymic, font=headline)
        draw.text((1920, 2170), address, font=headline)

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
    def draw_receipt_optional(lot_number, cost_payment, second_name, patronymic, address, first_name,):
        img_receipt = Image.open('images/snt.jpeg')
        draw = ImageDraw.Draw(img_receipt)
        headline = ImageFont.truetype('arial.ttf', size=100)

        # извещение
        draw.text((3150, 1350), str(cost_payment), font=headline)

        draw.text((4000, 500), lot_number, font=headline)
        draw.text((1920, 500), second_name + " " + first_name + " " + patronymic, font=headline)
        draw.text((1920, 620), address, font=headline)
        # квитанция
        draw.text((3150, 2900), str(cost_payment), font=headline)
        draw.text((4000, 2050), lot_number, font=headline)
        draw.text((1920, 2050), second_name + " " + first_name + " " + patronymic, font=headline)
        draw.text((1920, 2170), address, font=headline)

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
