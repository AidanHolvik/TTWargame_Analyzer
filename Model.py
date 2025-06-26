import sqlite3
from abc import ABC, abstractmethod
import re

"""
The model is responsible for:
    - Managing data: CRUD (Create, Read, Update, Delete) operations
    - Enforcing business rules
    - Notifying the View and Controller of state changes
"""


SQL_TABLES = [
    # TODO: order by name?
    """CREATE TABLE IF NOT EXISTS units(
        name            TEXT    PRIMARY KEY,
        points_cost     INT     NOT NULL 
                                DEFAULT 0
                                CHECK(points_cost >= 0)
    );""",

    # TODO: order by name?
    """CREATE TABLE IF NOT EXISTS models(
        unit        INT     NOT NULL,
        name        TEXT    NOT NULL,
        quantity    INT     NOT NULL 
                            DEFAULT 1 
                            CHECK(quantity > 0),
        toughness   INT     NOT NULL
                            CHECK(toughness > 0),
        save        INT     NOT NULL
                            CHECK(save > 1 AND save <= 7),
        health      INT     NOT NULL
                            CHECK(health > 0),
        invuln      INT     CHECK(invuln > 1 AND invuln < 7),
        isLeader    TEXT    NOT NULL
                            DEFAULT 'False'
                            CHECK(leader IN ('True','False')),
        enabled     TEXT    NOT NULL
                            DEFAULT 'True'
                            CHECK(enabled in ('True','False')),
                    FOREIGN KEY (unit)
                        REFERENCES units(id),
                    PRIMARY KEY (unit, name)
    );"""
]











class DBRecord(ABC):

    @abstractmethod
    def __eq__(self, that):
        pass

    """
    Generates a tuple which can be used to generate a record matching the DBRecord object
    """
    @abstractmethod
    def asTuple(self):
        pass


class Unit(DBRecord):
    def __init__(self, name: str = "", cost: int = 0):
        self._name = None
        self._cost = None

        self.name = name
        self.cost = cost

    def __init__(self, row: tuple[str, int]):
        self._name = row[0]
        self._cost = row[1]
    
    def __eq__(self, that):
        return self.name == that.name
    
    def asTuple(self):
        return (self.name, self.cost)
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value

    @property
    def cost(self):
        return self._cost
    @cost.setter
    def cost(self, value: int):
        if value >= 0:
            self._cost = value

class Model(DBRecord):
    def __init__(self, unit: int, name: str = '', quantity: int = 1, toughness: int = 1, save: int = 6, health: int = 1, invuln: int = None, isLeader: bool = False, enabled: bool = True):
        self.unit = unit
        self.name = name
        self.quantity = quantity
        self.toughness = toughness
        self.save = save
        self.health = health
        self.invuln = invuln
        self.isLeader = isLeader
        self.enabled = enabled

    # Expects a tuple matching the asTuple output
    def __init__(self, row: tuple[int,str,int,int,int,int,int,str|bool,str|bool]):
        self.unit = row[0]
        self.currName = row[1] # NOTE: this will cause update() to update the last record loaded if you're not careful
        self.name = row[1]
        self.quantity = row[2]
        self.toughness = row[3]
        self.save = row[4]
        self.health = row[5]
        self.invuln = row[6]
        self.isLeader = row[7]
        self.enabled = row[8]
    
    def __eq__(self, that):
        return self.unit == that.unit and self.name == that.name

    def asTuple(self):
        return (self.unit, self.name, self.quantity, self.toughness, self.save, self.health, self.invuln, str(self.isLeader), str(self.enabled))

    def exists(self, database: str):
        try:
            with sqlite3.connect(database) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM Models WHERE name=? AND unit=?', (self.name, self.unit))
                if not cur.fetchone():
                    return False
                else:
                    return True
        except sqlite3.OperationalError as e:
            # print(f'Error verifying existence of model "{name}" in {database}: ', str(e))
            return None
    
    
    
    def create(self, database: str):
        exists = self.exists(database)
        if exists is None: 
            return (bool(False), f'Error saving new model "{self.name}" to {database}: Failed to check if such a model already exists')
        elif not exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('INSERT INTO Models(unit,name,quantity,toughness,save,health,invuln,isLeader,enabled) VALUES (?,?,?,?,?,?,?,?,?)', self.asTuple())
                    conn.commit()
                    return (bool(True), f'New model "{self.name}" added to {database}')
            except sqlite3.OperationalError as e:
                return (bool(False), f'Error saving new model "{self.name}" to {database}: ' + str(e))
        else:
            return (bool(False), f'Error saving new model "{self.name}" to {database}: A model with this primary key already exists')
        
    def read(self, database: str):
        if self.exists(database):
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM Models WHERE name=? AND unit=?', (self.name, self.unit))
                    record = cur.fetchone()

                    return Model(record)
            except sqlite3.OperationalError as e:
                return None

    def update(self, database: str):
        exists = self.exists(database)
        if exists is None:
            return (bool(False), f'Error updating model "{self.currName}" in {database}: Failed to check if such a model exists')
        elif exists:
            try:
                with sqlite3.connect(database) as conn:
                    cur = conn.cursor()
                    cur.execute('UPDATE Models SET name=?, quantity=?, toughness=?, save=?, health=?, invuln=?, isLeader=?, enabled=?  WHERE unit=? AND name=?', (self.name, self.quantity, self.toughness, self.save, self.health, self.invuln, str(self.isLeader), str(self.enabled), self.unit, self.currName))
                    conn.commit()
                    tempName = self.currName
                    self.currName = self.name
                    return (bool(True), f'Updated model "{tempName}" in {database}')
            except sqlite3.OperationalError as e:
                print(f'Error updating model "{self.currName}" in {database}:', e)
                return (bool(False), f'Error updating model "{self.currName}" in {database}: ' + str(e))
        else:
            return (bool(False), f'Error updating model "{self.currName}" in {database}: No such model exists')
    
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

    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, value: int):
        # TODO: verify that the unit exists
        if value is not None:
            self._unit = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value: str):
        if value is not None:
            self._name = value
    
    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value: int):
        if value is not None and value > 0:
            self._quantity = value

    @property
    def toughness(self):
        return self._toughness
    @toughness.setter
    def toughness(self, value: int):
        if value > 0:
            self._toughness = value
    
    @property
    def save(self):
        return self._save
    @save.setter
    def save(self, value: int):
        if value > 1 and value <= 7:
            self._save = value
    
    @property
    def health(self):
        return self._health
    @health.setter
    def health(self, value: int):
        if value > 0:
            self._health = value
    
    @property
    def invuln(self):
        return self._invuln
    @invuln.setter
    def invuln(self, value: int):
        if value is None:
            self._invuln = value
        elif value > 1 and value <= 6:
            self._invuln = value
    
    @property
    def isLeader(self):
        return self._isLeader
    @isLeader.setter
    def isLeader(self, value: bool | str):
        if value is not None:
            if type(value) == bool:
                self._isLeader = value
            elif value.lower() == 'false':
                self._isLeader = False
            elif value.lower() == 'true':
                self._isLeader = True
    
    @property
    def enabled(self):
        return self._enabled
    @enabled.setter
    def enabled(self, value: bool | str):
        if value is not None:
            if type(value) == bool:
                self._enabled = value
            elif value.lower() == 'false':
                self._enabled = False
            elif value.lower() == 'true':
                self._enabled = True




class Database():
    def __init__(self, fileName: str):
        self.db = fileName
    
    # Unit CRUD
    def listUnits(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT name FROM units')
                unitNames = cur.fetchall()

                return unitNames
        except sqlite3.OperationalError as e:
            print('Error reading unit')
            return None

    def createUnit(self, unit: Unit):
        # TODO: handle case where a unit with that name already exists
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO units(name,points_cost) VALUES (?,?)', unit.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error creating unit')
            return False
    
    def readUnit(self, name: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM units WHERE name=?', (name,))
                record = cur.fetchone()
                unit = Unit(record)

                return unit
        except sqlite3.OperationalError as e:
            print('Error reading unit')
            return None
    
    def updateUnit(self, name: str, new: Unit):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute(f'UPDATE units SET name=?, points_cost=? WHERE name={name}', new.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error updating unit')
            return False
    
    def deleteUnit(self, name: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('DELETE FROM units WHERE name=?', (name,))
                conn.commit()

                return True
        except sqlite3.OperationalError as e:
            return False
        
    # Model CRUD
    def listModels(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT unit, name FROM models')
                models = cur.fetchall()

                return models
        except sqlite3.OperationalError as e:
            print('Error reading unit')
            return None
    
    def createModel(self, model: Model):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO models(unit,name,quantity,toughness,save,health,invuln,isLeader,enabled) VALUES (?,?,?,?,?,?,?,?,?)', model.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error creating model')
            return False
    
    def readModel(self, unitName: str, modelName: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM models WHERE unit=? AND name=?', (unitName, modelName))
                record = cur.fetchone()
                model = Model(record)

                return model
        except sqlite3.OperationalError as e:
            print('Error reading Model')
            return None
        
    def updateModel(self, unitName: str, modelName: str, new: Model):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute(f'UPDATE models SET unit=?, name=?, quantity=?, toughness=?, save=?, health=?, invuln=?, isLeader=?, enabled=? WHERE unit={unitName} AND name={modelName}', new.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error updating model')
            return False
        
    def deleteModel(self, unitName: str, modelName: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('DELETE FROM models WHERE unit=? AND name=?', (unitName, modelName))
                conn.commit()

                return True
        except sqlite3.OperationalError as e:
            return False
        
    