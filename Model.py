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
                            CHECK(isLeader IN ('True','False')),
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
    @abstractmethod
    def __lt__(self,that):
        pass
    @abstractmethod
    def __str__(self):
        pass


    """
    Returns a new DBRecord created using the values from row. row is expected to have the same format
    as the output of asTuple.
    """
    @abstractmethod
    def fromTuple(row: tuple):
        pass

    """
    Generates a tuple which represents a record matching the DBRecord object
    """
    @abstractmethod
    def asTuple(self):
        pass


class Unit(DBRecord):
    def __init__(self, name: str = "", cost: int = 0):

        self.name = name
        self.cost = cost
    
    def __str__(self):
        return str(self.asTuple())
    
    @staticmethod
    def fromTuple(row: tuple[str,int]):
        return Unit(row[0],row[1])
    
    def asTuple(self):
        return (self.name, self.cost)
    

    def __eq__(self, that):
        return self.name == that.name
    
    def __lt__(self, that):
        return self.name < that.name
        
    
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
    def __init__(self, unit: int, name: str = '', quantity: int = 1, toughness: int = 1, save: int = 6, health: int = 1, invuln: int = None, isLeader: bool|str = False, enabled: bool|str = True):
        self.unit = unit
        self.name = name
        self.quantity = quantity
        self.toughness = toughness
        self.save = save
        self.health = health
        self.invuln = invuln
        self.isLeader = isLeader
        self.enabled = enabled

    def __str__(self):
        return str(self.asTuple())
    
    @staticmethod
    def fromTuple(row: tuple[int,str,int,int,int,int,int,str|bool,str|bool]):
        return Model(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    
    def asTuple(self):
        return (self.unit, self.name, self.quantity, self.toughness, self.save, self.health, self.invuln, str(self.isLeader), str(self.enabled))


    def __eq__(self, that):
        return self.unit == that.unit and self.name == that.name
    
    def __lt__(self, that):
        if self.unit == that.unit:
            return self.name < that.name
        else:
            return self.unit < that.unit

    
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
        self.db = f'{fileName}.db'

        # Initialize database
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                for table in SQL_TABLES:
                    cur.execute(table)
                conn.commit()
        except sqlite3.OperationalError as e:
            print('Error initializing database: ', e)
    
    # Unit CRUD
    def listUnits(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM units ORDER BY name')
                queryResult = cur.fetchall()

                units = []
                for row in queryResult:
                    units.append(Unit.fromTuple(row))

                return units
        except sqlite3.OperationalError as e:
            print('Error listing units: ', e)
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
            print('Error creating unit: ', e)
            return False
    
    def readUnit(self, name: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM units WHERE name=?', (name,))
                record = cur.fetchone()
                unit = Unit.fromTuple(record)

                return unit
        except sqlite3.OperationalError as e:
            print('Error reading unit: ', e)
            return None
    
    def updateUnit(self, name: str, new: Unit):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute(f'UPDATE units SET name=?, points_cost=? WHERE name="{name}"', new.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error updating unit: ', e)
            return False
    
    def deleteUnit(self, name: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('DELETE FROM units WHERE name=?', (name,))
                conn.commit()

                return True
        except sqlite3.OperationalError as e:
            print('Error deleting unit: ', e)
            return False
        
    # Model CRUD
    def listModels(self):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM models ORDER BY unit, name')
                queryResult = cur.fetchall()

                models = []
                for row in queryResult:
                    models.append(Model.fromTuple(row))

                return models
        except sqlite3.OperationalError as e:
            print('Error listing models: ', e)
            return None
    
    def createModel(self, model: Model):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO models(unit,name,quantity,toughness,save,health,invuln,isLeader,enabled) VALUES (?,?,?,?,?,?,?,?,?)', model.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error creating model: ', e)
            return False
    
    def readModel(self, unitName: str, modelName: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM models WHERE unit=? AND name=?', (unitName, modelName))
                record = cur.fetchone()
                model = Model.fromTuple(record)

                return model
        except sqlite3.OperationalError as e:
            print('Error reading Model: ', e)
            return None
        
    def updateModel(self, unitName: str, modelName: str, new: Model):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute(f'UPDATE models SET unit=?, name=?, quantity=?, toughness=?, save=?, health=?, invuln=?, isLeader=?, enabled=? WHERE unit="{unitName}" AND name="{modelName}"', new.asTuple())
                conn.commit()
                return True
        except sqlite3.OperationalError as e:
            print('Error updating model: ', e)
            return False
        
    def deleteModel(self, unitName: str, modelName: str):
        try:
            with sqlite3.connect(self.db) as conn:
                cur = conn.cursor()
                cur.execute('DELETE FROM models WHERE unit=? AND name=?', (unitName, modelName))
                conn.commit()

                return True
        except sqlite3.OperationalError as e:
            print('Error deleting model: ', e)
            return False
        
    