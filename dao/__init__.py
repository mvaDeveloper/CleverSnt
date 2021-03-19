import sqlite3
from dao.owner import OwnerDao
from dao.debt import DebtDao
from dao.payment import PaymentDao


class DAO:
    def __init__(self):
        self.connection = sqlite3.connect('snt.db')
        self.cursor = self.connection.cursor()
        self.owner = OwnerDao(self.connection, self.cursor)
        self.payment = PaymentDao(self.connection, self.cursor)
        self.debt = DebtDao(self.connection, self.cursor)
