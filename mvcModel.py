import sqlite3
from abc import ABC, abstractmethod
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
        unit TEXT NOT NULL,
        model TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
        leader TEXT CHECK(leader IN ('True','False')) NOT NULL DEFAULT 'False',
        enabled TEXT CHECK(enabled in ('True','False')) NOT NULL DEFAULT 'True',
        FOREIGN KEY (unit) REFERENCES Units(name),
        FOREIGN KEY (model) REFERENCES Models(name),
        PRIMARY KEY (unit, model)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Keywords(
        model TEXT NOT NULL,
        keyword TEXT NOT NULL,
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (keyword) REFERENCES Keywords(keyword),
        PRIMARY KEY (model, keyword)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Model_Abilities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        ability TEXT NOT NULL,
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (ability) REFERENCES Model_Abilities(name)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Weapons(
        model TEXT NOT NULL,
        weapon TEXT NOT NULL,
        skill INTEGER NOT NULL CHECK(skill > 1 AND skill < 7),
        quantity INTEGER NOT NULL DEFAULT 1 CHECK(quantity > 0),
        enabled TEXT CHECK(enabled in ('True','False')) NOT NULL DEFAULT 'True',
        FOREIGN KEY (model) REFERENCES Models(name),
        FOREIGN KEY (weapon) REFERENCES Weapons(name),
        PRIMARY KEY (model, weapon)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Weapon_Abilities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        weapon TEXT NOT NULL,
        ability TEXT NOT NULL,
        FOREIGN KEY (weapon) REFERENCES Weapons(name),
        FOREIGN KEY (ability) REFERENCES Weapon_Abilities(name)
    );"""
]


# TODO: add input validation when saving records

class Database():

    def regexp(self, y, x, search=re.search):
        return True if search(x,y) else False

    def __init__(self, dbFile: str):
        self.file = dbFile

                        # TODO: only open db when saving or loading

        try:
            self.con = sqlite3.connect(self.file)
            print(f'Opened SQLite database with version {sqlite3.sqlite_version}.')
            self.con.create_function('REGEXP', 2, self.regexp)
            self.cur = self.con.cursor()
                
            # Create tables
            for table in SQL_TABLES:
                self.cur.execute(table)

            self.units = {}
            self.models = {}
            self.weapons = {}
            self.keywords = {}
            self.load(self.file)

        except sqlite3.OperationalError as e:
            print('Database Error:',e)

    def load(self, dbFile: str): # Set Database object to represent the data in the db file
        
        self.weapons = self.getWeaponList()
        self.keywords = self.getKeywordList()
        self.models = self.getModelList()
        self.units = self.getUnitList()

        for model in self.models:
            # assign keywords to models
            self.cur.execute('SELECT * FROM Assigned_Keywords WHERE model=?', (model.name,))
            table = self.cur.fetchall()
            for assn in table:
                model.keywords.add(assn[1])

            # assign weapons to models
            self.cur.execute('SELECT * FROM Assigned_Weapons WHERE model=?', (model.name,))
            table = self.cur.fetchall()
            for assn in table:
                model.weapons[assn[1]] = AssignedWeapon(assn[0], assn[1], assn[2], assn[3], assn[4])   

        # assign models to units
        for unit in self.units:
            self.cur.execute('SELECT * FROM Assigned_Models WHERE unit=?', (unit.name,))
            table = self.cur.fetchall()
            for assn in table:
                unit.models[assn[1]] = AssignedModel(assn[0], assn[1], assn[2], assn[3], assn[4])

    
    def save(self, dbFile: str): # TODO: save to the db file
        pass

    def getUnitList(self):
        self.cur.execute('SELECT * FROM Units')
        table = self.cur.fetchall()

        units = {}
        for record in table:
            units[record[0]] = Unit(record[0], record[1])
        return units

    def getModelList(self):
        self.cur.execute('SELECT * FROM Models')
        table = self.cur.fetchall()

        models = {}
        for record in table:
            models[record[0]] = Model(record[0], record[1], record[2], record[3], record[4])
        return models

    def getKeywordList(self):
        self.cur.execute('SELECT * FROM Keywords')
        table = self.cur.fetchall()

        keywords = {}
        for record in table:
            keywords[record[0]] = Keyword(record[0])
        return keywords

    def getWeaponList(self):
        self.cur.execute('SELECT * FROM Weapons')
        table = self.cur.fetchall()

        weapons = {}
        for record in table:
            weapons[record[0]] = Weapon(record[0], record[1], record[2], record[3], record[4])
        return weapons

    
    def close(self):
        self.con.close()


class DBRecord(ABC):

    @abstractmethod
    def __eq__(self, that):
        pass

    """
    Determines whether a record with the same primary key already exists in the table
    """
    @abstractmethod
    def exists(self, database: str) -> bool:
        pass

    """
    Instantiates a new DBRecord object by retrieving the record with the specified primary key from the database
    """
    @abstractmethod
    def load(self, database: str):
        pass

    """
    Saves the DBRecord in the database as a new record
    """
    @abstractmethod
    def saveNew(self, database: str) -> tuple[bool, str]:
        pass

    """
    Updates the corresponding record in the database to match the DBRecord object
    """
    @abstractmethod
    def saveUpdate(self, database: str) -> tuple[bool, str]:
        pass

    """
    Deletes the record with the specified primary key from the database
    """
    @abstractmethod
    def delete(self, database: str) -> bool:
        pass

# TODO: property method for assigned modelss

class Unit(DBRecord):
    def __init__(self, name: str = "", cost: int = 0):
        self.name = name
        self.cost = cost
        self.models = {} # dict: key is model name, value is AssignedModel object
    
    def __eq__(self, that):
        return self.name == that.name
    
    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM Units WHERE name=?', (self.name,))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of unit "{name}" in {database}: ', str(e))
            return None

    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Units WHERE name=?', (self.name,))
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
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Units WHERE name=?', (self.name,))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False
    
    def getAssignedModels(self, database: str):
        # TODO: SELECT * FROM Assigned_Models WHERE unit=self.name
        # TODO: convert each to an AssignedModel object, return dict of objects
        pass
        
    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, value: str):
        if value is not None:
            self.name = value

    @property
    def cost(self):
        return self.cost
    @cost.setter
    def cost(self, value: int):
        if value >= 0:
            self.cost = value

# TODO: property method for assigned weapons / keywords

class Model(DBRecord):
    def __init__(self, name: str = '', toughness: int = 1, save: int = 6, health: int = 1, invuln: int = None):
        self.name = name
        self.toughness = toughness
        self.save = save
        self.health = health
        self.invuln = invuln
        self.weapons = {} # dict: key is weapon name, value is AssignedWeapon object
        self.keywords = set() # set of assigned keywords
    
    def __eq__(self, that):
        return self.name == that.name

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM Models WHERE name=?', (self.name,))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of model "{name}" in {database}: ', str(e))
            return None
    
    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Models WHERE name=?', (self.name,))
                    record = cur.fetchone()

                    return Model(record[0], record[1], record[2], record[3], record[4])
            except sqlite3.OperationalError as e:
                return None
    
    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new model "{self.name}" to {database}: Failed to check if such a model already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Models(name,toughness,save,health,invuln) VALUES (?,?,?,?,?)', (self.name, self.toughness, self.save, self.health, self.invuln))
                    conn.commit()
                    return (bool(True), f'New model "{self.name}" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new model "{self.name}" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new model "{self.name}" to {database}: A model with this primary key already exists')

    def saveUpdate(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating model "{self.name}" in {database}: Failed to check if such a model exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Models SET toughness=?, save=?, health=?, invuln=? WHERE name=?', (self.toughness, self.save, self.health, self.invuln, self.name))
                    conn.commit()
                    return (bool(True), f'Updated model "{self.name}" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating model "{self.name}" in {database}:', e)
                return (bool(False), f'Error updating model "{self.name}" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating model "{self.name}" in {database}: No such model exists')
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Models WHERE name=?', (self.name,))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False

    def getAssignedWeapons(self, database: str):
        # TODO: SELECT * FROM Assigned_Weapons WHERE model=self.name
        # TODO: convert each to an AssignedWeapon object, return dict of objects
        pass

    def getAssignedKeywords(self, database: str):
        # TODO: SELECT * FROM Assigned_Keywords WHERE model=self.name
        # TODO: convert each to an AssignedKeyword object, return dict of objects
        pass

    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, value: str):
        if value is not None:
            self.name = value

    @property
    def toughness(self):
        return self.toughness
    @toughness.setter
    def toughness(self, value: int):
        if value > 0:
            self.toughness = value
    
    @property
    def save(self):
        return self.save
    @save.setter
    def save(self, value: int):
        if value > 1 and value <= 7:
            self.save = value
    
    @property
    def health(self):
        return self.health
    @health.setter
    def health(self, value: int):
        if value > 0:
            self.health = value
    
    @property
    def invuln(self):
        return self.invuln
    @invuln.setter
    def invuln(self, value: int):
        if value is None:
            self.invuln = value
        elif value > 1 and value <= 6:
            self.invuln = value


class AssignedModel(DBRecord):
    def __init__(self, unit: str, model: str, quantity: int = 1, isLeader: bool = False, enabled: bool = True):
        self.unit = unit
        self.model = model
        self.quantity = quantity
        self.isLeader = isLeader
        self.enabled = enabled

    def __eq__(self, that):
        return self.unit == that.unit and self.model == that.model

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT unit FROM Assigned_Models WHERE unit=? AND model=?', (self.unit,self.model))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of model "{name}" in {database}: ', str(e))
            return None
    
    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Assigned_Models WHERE unit=? AND model=?', (self.unit, self.model))
                    record = cur.fetchone()

                    return AssignedWeapon(record[0], record[1], record[2], record[3], record[4])
            except sqlite3.OperationalError as e:
                return None
    
    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new model assignment "({self.unit}, {self.model})" to {database}: Failed to check if such an assignment already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Assigned_Models(unit,model,quantity,leader,enabled) VALUES (?,?,?,?,?)', (self.unit, self.model, self.quantity, str(self.isLeader), str(self.enabled)))
                    conn.commit()
                    return (bool(True), f'New model assignment "({self.unit}, {self.model})" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new model assignment "({self.unit}, {self.model})" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new model assignment "({self.unit}, {self.model})" to {database}: This model is already assigned to this unit')

    def saveUpdate(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating model assignment "({self.unit}, {self.model})" in {database}: Failed to check if such an assignment exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Assigned_Models SET quantity=?, leader=?, enabled=? WHERE unit=? AND model=?', (self.quantity, str(self.isLeader), str(self.enabled), self.unit, self.model))
                    conn.commit()
                    return (bool(True), f'Updated model assignment "({self.unit}, {self.model})" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating model assignment "({self.unit}, {self.model})" in {database}:', e)
                return (bool(False), f'Error updating model assignment "({self.unit}, {self.model})" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating model assignment "({self.unit}, {self.model})" in {database}: No such assignment exists')
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Assigned_Models WHERE unit=? AND model=?', (self.unit, self.model))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False
    
    @property
    def unit(self):
        return self.unit
    @unit.setter
    def unit(self, value: str):
        if value is not None:
            self.unit = value
    
    @property
    def model(self):
        return self.model
    @model.setter
    def model(self, value: str):
        if value is not None:
            self.model = value
    
    @property
    def quantity(self):
        return self.quantity
    @quantity.setter
    def quantity(self, value: int):
        if value > 0:
            self.quantity = value
    
    @property
    def isLeader(self):
        return self.isLeader
    @isLeader.setter
    def isLeader(self, value: bool):
        self.isLeader = value
    
    @property
    def enabled(self):
        return self.enabled
    @enabled.setter
    def enabled(self, value: bool):
        self.enabled = value
    

class Keyword(DBRecord):
    def __init__(self, keyword: str = ''):
        self.keyword = keyword
    
    def __eq__(self, that):
        return self.keyword == that.keyword

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT keyword FROM Keywords WHERE keyword=?', (self.keyword,))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of unit "{name}" in {database}: ', str(e))
            return None

    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Keywords WHERE keyword=?', (self.keyword,))
                    record = cur.fetchone()

                    return Keyword(record[0])
            except sqlite3.OperationalError as e:
                return None

    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new keyword "{self.keyword}" to {database}: Failed to check if such a keyword already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Keywords(keyword) VALUES (?)', (self.keyword,))
                    conn.commit()
                    return (bool(True), f'New keyword "{self.keyword}" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new keyword "{self.keyword}" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new keyword "{self.keyword}" to {database}: A keyword with this primary key already exists')

    def saveUpdate(self, database: str):
        pass
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Keywords WHERE keyword=?', (self.keyword,))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False
    
    @property
    def keyword(self):
        return self.keyword
    @keyword.setter
    def keyword(self, keyword: str):
        if keyword is not None:
            self.keyword = keyword


class AssignedKeyword(DBRecord):
    def __init__(self, model: str, keyword: str):
        self.model = model
        self.keyword = keyword

    def __eq__(self, that):
        return self.model == that.model and self.keyword == that.keyword

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT model FROM Assigned_Keywords WHERE model=? AND keyword=?', (self.model, self.keyword))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of unit "{name}" in {database}: ', str(e))
            return None

    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Assigned_Keywords WHERE model=? AND keyword=?', (self.model, self.keyword))
                    record = cur.fetchone()

                    return AssignedKeyword(record[0], record[1])
            except sqlite3.OperationalError as e:
                return None

    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new keyword assignment "({self.model},{self.keyword})" to {database}: Failed to check if such an assignment already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Assigned_Keywords(model,keyword) VALUES (?,?)', (self.model, self.keyword))
                    conn.commit()
                    return (bool(True), f'Keyword "{self.keyword}" assigned to model "{self.model}" in {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new keyword assignment "({self.model}, {self.keyword})" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new keyword assignment "({self.model}, {self.keyword})" to {database}: This keyword has already been assigned to this model')

    def saveUpdate(self, database: str):
        return (bool(True), f'Updated keyword assignment "({self.model}, {self.keyword})" in {database}')
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Assigned_Keywords WHERE model=? AND keyword=?', (self.model, self.keyword))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False

    @property
    def model(self):
        return self.model
    @model.setter
    def model(self, value: str):
        if value is not None:
            self.model = value
    
    @property
    def keyword(self):
        return self.keyword
    @keyword.setter
    def keyword(self, value: str):
        if value is not None:
            self.keyword = value


class Weapon(DBRecord):
    def __init__(self, name: str = "", attacks: int|str = 1, strength: int = 1, ap: int = 0, damage: int|str = 1):
        self.name = name
        self.attacks = str(attacks)
        self.strength = strength
        self.ap = ap
        self.damage = str(damage)
    
    def __eq__(self, that):
        return self.name == that.name

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM Weapons WHERE name=?', (self.name,))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of weapon "{name}" in {database}: ', str(e))
            return None

    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Weapons WHERE name=?', (self.name,))
                    record = cur.fetchone()

                    return Weapon(record[0], record[1], record[2], record[3], record[4])
            except sqlite3.OperationalError as e:
                return None

    # TODO: edit saveNew and saveUpdate to validate format of attacks and damage inputs (int or 'xdy+z')

    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new weapon "{self.name}" to {database}: Failed to check if such a weapon already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Weapons(name,attacks,strength,ap,damage) VALUES (?,?,?,?,?)', (self.name, self.attacks, self.strength, self.ap, self.damage))
                    conn.commit()
                    return (bool(True), f'New weapon "{self.name}" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new weapon "{self.name}" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new weapon "{self.name}" to {database}: A weapon with this primary key already exists')

    def saveUpdate(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating weapon "{self.name}" in {database}: Failed to check if such a weapon exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Weapons SET attacks=?, strength=?, ap=?, damage=? WHERE name=?', (self.attacks, self.strength, self.ap, self.damage, self.name))
                    conn.commit()
                    return (bool(True), f'Updated weapon "{self.name}" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating weapon "{self.name}" in {database}:', e)
                return (bool(False), f'Error updating weapon "{self.name}" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating weapon "{self.name}" in {database}: No such weapon exists')
    
    @staticmethod
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Weapons WHERE name=?', (self.name,))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False

    @property
    def name(self):
        return self.name
    @name.setter
    def name(self, value: str):
        self.name = value
    
    @property
    def attacks(self):
        return str(self.attacks)
    @attacks.setter
    def attacks(self, value: int|str):
        if type(value) == int and value > 0:
            self.attacks = str(value)
        elif re.search('[1-9][0-9]*([dD][1-9][0-9]*)?([+][1-9][0-9]*)?', value):
            self.attacks = value.lower()
    
    @property
    def strength(self):
        return self.strength
    @strength.setter
    def strength(self, value: str):
        if value > 0:
            self.strength = value
    
    @property
    def ap(self):
        return self.ap
    @ap.setter
    def ap(self, value: str):
        if value >= 0:
            self.ap = value
    
    @property
    def damage(self):
        return str(self.damage)
    @damage.setter
    def damage(self, value: int|str):
        if type(value) == int and value > 0:
            self.damage = str(value)
        elif re.search('[1-9][0-9]*([dD][1-9][0-9]*)?([+][1-9][0-9]*)?', value):
            self.damage = value.lower()


class AssignedWeapon(DBRecord):
    # TODO: validate format of parameter 'enabled'
    def __init__(self, model: str, weapon: str, skill: int = 6, quantity: int = 1, enabled: bool = True):
        self.model = model
        self.weapon = weapon
        self.skill = skill
        self.quantity = quantity
        self.enabled = enabled

    def __eq__(self, that):
        return self.model == that.model and self.weapon == that.weapon

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT weapon FROM Assigned_Weapons WHERE model=? AND weapon=?', (self.model,self.weapon))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of model "{name}" in {database}: ', str(e))
            return None
    
    def load(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Assigned_Weapons WHERE model=? AND weapon=?', (self.model, self.weapon))
                    record = cur.fetchone()

                    return AssignedWeapon(record[0], record[1], record[2], record[3], record[4])
            except sqlite3.OperationalError as e:
                return None
    
    def saveNew(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new weapon assignment "({self.model}, {self.weapon})" to {database}: Failed to check if such an assignment already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Assigned_Weapons(model,weapon,skill,quantity,enabled) VALUES (?,?,?,?,?)', (self.model, self.weapon, self.skill, self.quantity, str(self.enabled)))
                    conn.commit()
                    return (bool(True), f'New weapon assignment "({self.model}, {self.weapon})" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new weapon assignment "({self.model}, {self.weapon})" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new weapon assignment "({self.model}, {self.weapon})" to {database}: This weapon is already assigned to this model')

    def saveUpdate(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating weapon assignment "({self.model}, {self.weapon})" in {database}: Failed to check if such an assignment exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Assigned_Weapons SET skill=?, quantity=?, enabled=? WHERE model=? AND weapon=?', (self.skill, self.quantity, str(self.enabled), self.model, self.weapon))
                    conn.commit()
                    return (bool(True), f'Updated weapon assignment "({self.model}, {self.weapon})" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating weapon assignment "({self.model}, {self.weapon})" in {database}:', e)
                return (bool(False), f'Error updating weapon assignment "({self.model}, {self.weapon})" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating weapon assignment "({self.model}, {self.weapon})" in {database}: No such model exists')
    
    def delete(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('DELETE FROM Assigned_Weapons WHERE model=? AND weapon=?', (self.model, self.weapon))
                    conn.commit()

                    return True
            except sqlite3.OperationalError as e:
                return False
        else:
            return False
    
    @property
    def model(self):
        return self.model
    @model.setter
    def model(self, value: str):
        if value is not None:
            self.model = value
    
    @property
    def weapon(self):
        return self.weapon
    @weapon.setter
    def weapon(self, value: str):
        if value is not None:
            self.weapon = value
    
    @property
    def skill(self):
        return self.skill
    @skill.setter
    def skill(self, value: int):
        if value > 1 and value <= 6:
            self.skill = value
    
    @property
    def quantity(self):
        return self.quantity
    @quantity.setter
    def quantity(self, value: int):
        if value > 0:
            self.quantity = value
    
    @property
    def enabled(self):
        return self.enabled
    @enabled.setter
    def enabled(self, value: bool):
        self.enabled = value
