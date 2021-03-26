from PIL import Image, ImageDraw, ImageFont
import qrcode
import datetime


def main(lot_number, cost_payment, date_payment, membership_fee, electricity, date_begin,
         date_end, difference, second_name, patronymic, address, first_name, debt):
    receipt = general(lot_number, cost_payment, second_name, patronymic, address, first_name, date_payment)
    img_receipt = receipt[0]
    draw = receipt[1]
    headline = receipt[2]
    # извещение
    draw.text((3100, 750), str(membership_fee), font=headline)
    draw.text((3100, 860), str(debt), font=headline)
    draw.text((3110, 990), str(electricity), font=headline)
    draw.text((2390, 990), str(difference), font=headline)
    draw.text((2390, 1110), str(date_begin), font=headline)
    draw.text((2390, 1230), str(date_end), font=headline)
    draw.text((1550, 1460), date_payment, font=headline)
    # квитанция
    draw.text((3100, 2300), str(membership_fee), font=headline)
    draw.text((3100, 2410), str(debt), font=headline)
    draw.text((3110, 2540), str(electricity), font=headline)
    draw.text((2390, 2540), str(difference), font=headline)
    draw.text((2390, 2660), str(date_begin), font=headline)
    draw.text((2390, 2780), str(date_end), font=headline)
    draw.text((4000, 2050), lot_number, font=headline)
    draw.text((1550, 3010), date_payment, font=headline)
    show_save(img_receipt, second_name, lot_number, date_payment)


def optional(lot_number, cost_payment, second_name, patronymic, address, first_name):
    today = datetime.datetime.today()
    date_payment = str(today.day) + '.' + str(today.month) + '.' + str(today.year)
    receipt = general(lot_number, cost_payment, second_name, patronymic, address, first_name, date_payment)
    show_save(receipt[0], second_name, lot_number, date_payment)


def general(lot_number, cost_payment, second_name, patronymic, address, first_name, date_payment):
    img_receipt = Image.open('images/snt.jpeg')
    draw = ImageDraw.Draw(img_receipt)
    headline = ImageFont.truetype('arial.ttf', size=100)
    # извещение
    draw.text((3150, 1350), str(cost_payment), font=headline)
    draw.text((4000, 500), lot_number, font=headline)
    draw.text((1920, 500), second_name + " " + first_name + " " + patronymic, font=headline)
    draw.text((1920, 620), address, font=headline)
    draw.text((1550, 1460), date_payment, font=headline)
    # квитанция
    draw.text((3150, 2900), str(cost_payment), font=headline)
    draw.text((4000, 2050), lot_number, font=headline)
    draw.text((1920, 2050), second_name + " " + first_name + " " + patronymic, font=headline)
    draw.text((1920, 2170), address, font=headline)
    draw.text((1550, 3010), date_payment, font=headline)
    # qrcode
    data = "ST00012|Name=Садоводческое некомерческое товарищество\"Приморскре\"|" \
           "PersonalAcc=40703810416020000062|BankName=Центрально-Черназемный филиал ООО \"Экспобанк\"|" \
           "lastName=" + second_name + "|firstName=" + first_name + "|middleName=" + patronymic + \
           "|BIC=043807330|KPP=461101001|PayeeINN=4631011178|Sum=" + str(cost_payment)
    img_qr = qrcode.make(data)
    img_receipt.paste(img_qr, (100, 500))
    img_receipt.paste(img_qr, (100, 2200))
    return [img_receipt, draw, headline]


def show_save(img_receipt, second_name, lot_number, date_payment):
    name_receipt = "receipt/" + second_name + "_" + str(lot_number) + "_" + date_payment + ".png"
    img_receipt.save(name_receipt)
    img_receipt.show()
