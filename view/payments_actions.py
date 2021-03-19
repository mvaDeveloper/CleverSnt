from view import diversity_payment, update_payment, receipt
from logiс.scripts import making_payment
import dao


class PaymentsMenuActions:

    @staticmethod
    def diversity_payment(find_v):
        db = dao.DAO()
        diversity_payment.DiversityPayment(find_v, making_payment, db)

    @staticmethod
    def open_update_pay(find_v, number, self, tree):
        db = dao.DAO()
        update_payment.UpdatePayment(find_v, number, db, self, tree)

    @staticmethod
    def receipt(find_v, number):
        db = dao.DAO()
        receipt.ChoiceReceipt(db, find_v, number)
