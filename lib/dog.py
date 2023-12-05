import sqlite3
import os

current_working_directory = os.getcwd()
cwd = os.path.dirname(current_working_directory)

full_path = cwd + "/lib/dog.db"

print("cwd", full_path)
CONN = sqlite3.connect(full_path)
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed
    
    @staticmethod
    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
    
    @staticmethod
    def drop_table():
        sql = """
            DROP TABLE IF EXISTS dogs
        """    
        CURSOR.execute(sql)   

    def save(self):
        if self.id is None:
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """
            CURSOR.execute(sql, (self.name, self.breed))
            self.id = CURSOR.lastrowid
            CONN.commit()
        else:
            # Update if the dog already exists in the database
            sql = """
                UPDATE dogs
                SET name = ?, breed = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod      
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_by_id(cls, _id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        CURSOR.execute(sql, (_id,))
        row = CURSOR.fetchone()
        return cls.new_from_db(row) if row else None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)
    
    @classmethod
    def new_from_db(cls, row):
        if row:
            dog = cls(row[1], row[2])
            dog.id = row[0]
            return dog
        return None

    def update(self):
        if self.id:
            self.save()

# Usage example:
Dog.create_table()
joey = Dog.create('joey', 'cocker spaniel')

retrieved_dog = Dog.find_by_name('joey')
print((retrieved_dog.id, retrieved_dog.name, retrieved_dog.breed))


