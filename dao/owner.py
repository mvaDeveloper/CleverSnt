class OwnerDao:
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        # создание баз данных если их нет
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS owner 
            (id integer primary key,lot_number text, second_name text, first_name text,
             patronymic text, address text, square real, electricity text)''')

        self.connection.commit()

    # добавление информации в бд
    def insert(self, lot_number, second_name, first_name, patronymic, address, square, electricity):
        self.cursor.execute(
            '''
            INSERT INTO owner
                (lot_number, second_name, first_name, patronymic, address, square, electricity) 
            VALUES 
                (?,?,?,?,?,?,?)
            ''',
            (lot_number, second_name, first_name, patronymic, address, square, electricity))
        self.connection.commit()

    def update(self, lot_number, second_name, first_name, patronymic, address, square, electricity, id_owner):
        self.cursor.execute(
            '''
            UPDATE owner SET 
                lot_number=?, second_name=?, first_name=?, 
                patronymic=?, address=?, square=?, electricity=? 
            WHERE ID=?
            ''',
            (lot_number, second_name, first_name, patronymic, address, square, electricity, id_owner))
        self.connection.commit()

    def list(self):
        self.cursor.execute('''SELECT * FROM owner''')
        return self.cursor.fetchall()

    def delete(self, id_owner):
        self.cursor.execute('''DELETE FROM owner WHERE id=?''', (id_owner,))
        self.connection.commit()

    def get_by_id(self, id_owner):
        self.cursor.execute('''SELECT * FROM owner WHERE id=?''', (id_owner,))
        return self.cursor.fetchone()

    def get_by_number(self, lot_number):
        self.cursor.execute('''SELECT * FROM owner WHERE lot_number=?''', (lot_number,))
        return self.cursor.fetchone()
