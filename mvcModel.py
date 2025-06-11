import sqlite3
import re

SQL_TABLES = [
    """CREATE TABLE IF NOT EXISTS Units(
        name TEXT PRIMARY KEY,
        points_cost INTEGER NOT NULL DEFAULT 0 CHECK(points_cost >= 0)
    );""",

    """CREATE TABLE IF NOT EXISTS Models(
        name TEXT PRIMARY KEY,
        toughness INTEGER NOT NULL CHECK(toughness > 0),
        save INTEGER NOT NULL CHECK(save > 1 AND save <= 7),
        health INTEGER NOT NULL CHECK(health > 0),
        invuln INTEGER CHECK(invuln > 1 AND invuln < 7)
    );""",

    """CREATE TABLE IF NOT EXISTS Keywords(
        keyword TEXT PRIMARY KEY
    );""",

    """CREATE TABLE IF NOT EXISTS Model_Abilities(
        name TEXT PRIMARY KEY,
        conditions TEXT NOT NULL, -- some python statement which returns a boolean value
        effects TEXT NOT NULL, -- some statement to modify rolls, etc. still need to figure out how to do this
        shared TEXT CHECK(shared IN ('True','False')) NOT NULL DEFAULT 'False' 
    );""",

    """CREATE TABLE IF NOT EXISTS Weapons(
        name TEXT PRIMARY KEY,
        attacks TEXT NOT NULL CHECK(attacks REGEXP '[1-9][0-9]*([dD][1-9][0-9]*)?([+][1-9][0-9]*)?'),
        strength INTEGER NOT NULL CHECK(strength > 0),
        ap INTEGER NOT NULL CHECK(ap >= 0),
        damage TEXT NOT NULL CHECK(damage REGEXP '[1-9][0-9]*([dD][1-9][0-9]*)?([+][1-9][0-9]*)?')
    );""",

    """CREATE TABLE IF NOT EXISTS Weapon_Abilities(
        name TEXT PRIMARY KEY,
        conditions TEXT NOT NULL, -- some python statement which returns a boolean value
        effects TEXT NOT NULL -- some statement to modify rolls, etc. still need to figure out how to do this
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Models(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit TEXT NOT NULL,
        model TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
        leader TEXT CHECK(leader IN ('True','False')) NOT NULL DEFAULT 'False',
        enabled TEXT CHECK(enabled in ('True','False')) NOT NULL DEFAULT 'True',
        FOREIGN KEY (unit) REFERENCES Units(name),
        FOREIGN KEY (model) REFERENCES Models(name)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Keywords(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        keyword TEXT NOT NULL,
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (keyword) REFERENCES Keywords(keyword)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Model_Abilities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        ability TEXT NOT NULL,
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (ability) REFERENCES Model_Abilities(name)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Weapons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        weapon TEXT NOT NULL,
        skill INTEGER NOT NULL CHECK(skill > 1 AND skill < 7),
        quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
        enabled TEXT CHECK(enabled in ('True','False')) NOT NULL DEFAULT 'True',
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (weapon) REFERENCES Weapons(name)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Weapon_Abilities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weapon TEXT NOT NULL,
        ability TEXT NOT NULL,
        FOREIGN KEY (weapon) REFERENCES Weapons(name),
        FOREIGN KEY (ability) REFERENCES Weapon_Abilities(name)
    );"""
]


class Database():

    def regexp(self, y, x, search=re.search):
        return True if search(x,y) else False

    def __init__(self):
        try:
            self.con = sqlite3.connect('TTWGAnalyzer.db')
            print(f'Opened SQLite database with version {sqlite3.sqlite_version}.')
            self.con.create_function('REGEXP', 2, self.regexp)
            self.cur = self.con.cursor()
                
            # Create tables
            for table in SQL_TABLES:
                self.cur.execute(table)

        except sqlite3.OperationalError as e:
            print('Database Error:',e)

    def execute(self, sql: str, parameters):
        return self.cur.execute(sql, parameters)
    
    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return self.cur.fetchall()
    
    def commit(self):
        self.con.commit()

    # # Manage Units
    # def addUnit(self, name: str, pointsCost: int = 0):
    #     self.cur.execute('INSERT INTO Units(name,points_cost) VALUES (?,?)', (name, pointsCost))
    #     self.con.commit()
    # def getUnitByName(self, name: str):
    #     self.cur.execute('SELECT * FROM Units WHERE name = ?',(name,))

    
    def close(self):
        self.con.close()

class Unit():
    def __init__(self, name: str = "", cost: int = 0):
        self.name = name
        self.cost = cost

    """
    Determines whether a record with the same primary key already exists in the table
    """
    @staticmethod
    def exists(name: str, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM Units WHERE name=?', (name,))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            print(f'Error verifying existence of unit "{name}" in {database}: ', str(e))
            return None
        

    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, value: str):
        if value != None:
            self.name = value

    @property
    def cost(self):
        return self.cost
    @cost.setter
    def cost(self, value: int):
        if value >= 0:
            self.cost = value
    

    @staticmethod
    def load(name: str, database: str):
        if Unit.exists(name, database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Units WHERE name=?', (name,))
                    record = cur.fetchone()

                    return Unit(record[0], record[1])
            except sqlite3.OperationalError as e:
                return None
        

    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new unit "{self.name}" to {database}: Failed to check if such a unit already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Units(name,points_cost) VALUES (?,?)', (self.name, self.cost))
                    conn.commit()
                    return (bool(True), f'New unit "{self.name}" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new unit "{self.name}" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new unit "{self.name}" to {database}: A unit with this primary key already exists')

    def saveUpdate(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating unit "{self.name}" in {database}: Failed to check if such a unit exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Units SET points_cost=? WHERE name=?', (self.cost, self.name))
                    conn.commit()
                    return (bool(True), f'Updated unit "{self.name}" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating unit "{self.name}" in {database}:', e)
                return (bool(False), f'Error updating unit "{self.name}" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating unit "{self.name}" in {database}: No such unit exists')
    
    @staticmethod
    def delete(name: str, database: str):
        if Unit.exists(name, database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Units WHERE name=?', (name,))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False





        