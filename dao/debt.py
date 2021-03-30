class DebtDao:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS debt
            (id integer primary key, lot_number text, cost_payment real,
             target_contribution real, membership_fee real, electricity real,  
             balance real)''')
        self.connection.commit()

    def insert(self, lot_number, cost_payment, target_contribution, membership_fee, electricity, balance):
        self.cursor.execute(
            '''
            INSERT INTO debt
                (
                    lot_number, cost_payment, target_contribution, 
                    membership_fee, electricity, balance
                ) 
            VALUES 
                (?,?,?,?,?,?)
            ''',
            (lot_number, cost_payment, target_contribution, membership_fee, electricity, balance))
        self.connection.commit()

    def get_by_id(self, id_debt):
        self.cursor.execute('''SELECT * FROM debt WHERE id=?''', (id_debt,))
        return self.cursor.fetchone()

    def update(self, lot_number, cost_payment, target_contribution, membership_fee, electricity, balance, id_debt):
        self.cursor.execute(
            '''
            UPDATE debt SET 
                lot_number=?, cost_payment=?, target_contribution=?, membership_fee=?, electricity=?,balance=? 
            WHERE ID=?
            ''',
            (lot_number, cost_payment, target_contribution, membership_fee, electricity, balance, id_debt))
        self.connection.commit()

    def get_by_number(self, lot_number):
        self.cursor.execute('''SELECT * FROM debt WHERE lot_number LIKE ? order by id''', (lot_number,))
        return self.cursor.fetchall()

    def check_debt(self, lot_number, cost_payment, target_contribution, membership_fee, electricity):
        debt = self.get_by_number(lot_number)
        if not debt:
            self.insert(lot_number, cost_payment, target_contribution, membership_fee, electricity, cost_payment)
            self.insert(lot_number, cost_payment, target_contribution, membership_fee, electricity, cost_payment)
        else:
            id_debt = debt[0][0]
            self.update(
                lot_number, cost_payment, target_contribution,
                membership_fee, electricity, cost_payment, id_debt
            )
            self.update(
                lot_number, cost_payment, target_contribution,
                membership_fee, electricity, cost_payment, id_debt+1
            )
