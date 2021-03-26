class PaymentDao:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS payment
            (id integer primary key, lot_number text, cost_payment real, date_payment text,
             target_contribution real, membership_fee real, electricity real, date_begin real, 
             date_end real, balance real,status text, type_payment text)''')

    def insert(
            self, lot_number, cost_payment, date_payment, target_contribution, membership_fee,
            electricity, date_begin, date_end, balance, status, type_payment
    ):
        self.cursor.execute(
            '''
            INSERT INTO payment
                (
                    lot_number, cost_payment, date_payment, target_contribution, 
                    membership_fee, electricity, date_begin, date_end, balance, status, type_payment
                ) 
            VALUES 
                (?,?,?,?,?,?,?,?,?,?,?)
            ''',
            (lot_number, cost_payment, date_payment, target_contribution, membership_fee, electricity, date_begin,
             date_end, balance, status, type_payment))
        self.connection.commit()

    def get_by_number(self, lot_number):
        self.cursor.execute('''SELECT * FROM payment WHERE lot_number LIKE ?''', (lot_number,))
        return self.cursor.fetchall()

    def get_by_id(self, payment_id):
        self.cursor.execute('''SELECT * FROM payment WHERE id=?''', (payment_id,))
        return self.cursor.fetchone()

    def update(
            self, lot_number, cost_payment, date_payment, target_contribution,
            membership_fee, electricity, date_begin, date_end, balance, status, type_payment, number):
        self.cursor.execute(
            '''
            UPDATE payment SET 
                lot_number=?,cost_payment=?, date_payment=?, target_contribution=?, membership_fee=?,
                electricity=?, date_begin=?, date_end=?, balance=?, status=?,type_payment=?
            WHERE ID=?
            ''',
            (lot_number, cost_payment, date_payment, target_contribution, membership_fee,
             electricity, date_begin, date_end, balance, status, type_payment, number[0]))
        self.connection.commit()

    def delete(self, id_payment):
        self.cursor.execute('''DELETE FROM payment WHERE id=?''', (id_payment,))
        self.connection.commit()
