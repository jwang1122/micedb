import sqlite3
from sqlite3 import Error
from pprint import pprint
import uuid
from datetime import datetime


class MiceDB:
    miceFields = (
        'msid', 'gender', 'geno', 'dob',
        'ear', 'mom', 'dad', 'cage',
        'usage', 'date', 'type'
    )
    breedingFields = (
        'dob', 'cage', 'mom',
        'born',  'dad', 'males',
        'females', 'deaths', 'notes'
    )

    def __init__(self, dbname, url=None):
        self.dbname = dbname
        self.url = url

    def getMiceDB(self):
        self.conn = MiceDB.create_connection(self.dbname)
        c = self.conn.cursor()
        return c

    # Retrieve All
    def getMice(self):
        db = self.getMiceDB()
        MiceList = []
        try:
            for row in db.execute('select * from mice'):
                Mouse = self.getMouseFromList(row)
                MiceList.append(Mouse)
        except Exception as e:
            print("micedb-26:", e)

        return MiceList

    # Create One
    def create(self, mouse):
        """
        Create a mouse in database
        """
        print(mouse)
        db = self.getMiceDB()
        value = self.getValueFromMouse(mouse)
        db.execute(
            f"INSERT INTO mice VALUES (?{',?'*len(MiceDB.miceFields)})", value)
        self.conn.commit()
        return mouse.get('id')

    # Create Breeding
    def create_breeding(self, mouse):
        """
        Create a breeding in database
        """
        print(mouse)
        db = self.getMiceDB()
        value = self.getValueFromBreeding(mouse)
        db.execute(
            f"INSERT INTO breeding VALUES (?{',?'*len(MiceDB.breedingFields)})", value)
        count = mouse['males'] + mouse['females']
        print(count)
        self.conn.commit()
        return mouse.get('id')

    # Retrieve one
    def getMouse(self, id):
        """
        Retrieve a mouse from database by id
        """
        db = self.getMiceDB()
        mouse = None
        try:
            value = (id,)
            db.execute('SELECT * FROM mice WHERE id=?', value)
            mouse = self.getMouseFromList(db.fetchone())
        except Exception as e:
            print(e)
        return mouse

    # Update
    def update(self, id, mouse):
        """
        Update one record in database
        """
        # sql = "UPDATE mice SET cage='" + mouse['cage']+"',user='"+mouse['user'] + \
        #     "',date='"+mouse['date']+"',type='" + \
        #     mouse['type']+"' where id='"+id+"'"
        # db = self.getMiceDB()
        # db.execute(sql)
        # self.conn.commit()
        self.delete(id)
        self.create(mouse)
        return id

    # Delete
    def delete(self, mouse_id):
        """
        Delete a mouse by id
        """
        mouse = self.getMouse(mouse_id)
        db = self.getMiceDB()
        db.execute('DELETE FROM mice WHERE id=?', (mouse_id,))
        self.conn.commit()
        return mouse

    def getMouseFromList(self, row):
        mouse = {"id": row[0]}
        for i, field in enumerate(MiceDB.miceFields, 1):
            mouse[field] = row[i]
        return mouse

    def getValueFromMouse(self, mouse):
        value = [uuid.uuid4().hex]
        for field in MiceDB.miceFields:
            value.append(mouse[field])
        return value

    def getValueFromBreeding(self, mouse):
        value = [uuid.uuid4().hex]
        for field in MiceDB.breedingFields:
            value.append(mouse[field])
        return value

    @classmethod
    def create_connection(cls, db_file):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            # print(sqlite3.version)
        except Error as e:
            print(e)
        return conn

    @classmethod
    def create_table(cls, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)


if __name__ == '__main__':
    db = MiceDB("mice.db")
    # test create one
    # user = {
    #     "id":uuid.uuid4().hex,
    #     "name": '14" Wrentch',
    #     "age": 12
    # }
    # print(db.create(mouse))

    # test retrieve many
    mice = db.getMice()

    pprint(mice)

    print("Done.")
