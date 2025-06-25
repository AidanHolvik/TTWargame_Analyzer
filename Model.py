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
    """CREATE TABLE IF NOT EXISTS units(
        name            TEXT        PRIMARY KEY,
        points_cost     INTEGER     NOT NULL 
                                    DEFAULT 0
                                    CHECK(points_cost >= 0)
    );""",

    """CREATE TABLE IF NOT EXISTS models(
        name        TEXT    PRIMARY KEY,
        toughness   INT     NOT NULL
                            CHECK(toughness > 0),
        save        INT     NOT NULL
                            CHECK(save > 1 AND save <= 7),
        health      INT     NOT NULL
                            CHECK(health > 0),
        invuln      INT     CHECK(invuln > 1 AND invuln < 7)
    );""",

    """CREATE TABLE IF NOT EXISTS Assigned_Models(
        unit        TEXT    NOT NULL,
        model       TEXT    NOT NULL,
        quantity    INT     NOT NULL 
                            DEFAULT 1 
                            CHECK(quantity > 0),
        leader      TEXT    NOT NULL 
                            DEFAULT 'False'
                            CHECK(leader IN ('True','False')),
        enabled     TEXT    NOT NULL
                            DEFAULT 'True'
                            CHECK(enabled in ('True','False')),
                    FOREIGN KEY (unit)
                        REFERENCES units(name),
                    FOREIGN KEY (model)
                        REFERENCES models(name),
                    PRIMARY KEY (unit, model)
    );""",
]

# TODO: class representing the database as a whole, (bound to specific db file, allows easy interaction with DB)

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

    """
    Determines whether a record with the same primary key already exists in the table
    """
    @abstractmethod
    def exists(self, database: str) -> bool:
        pass

    
    # CRUD operations
    """
    Saves the DBRecord in the database as a new record
    """
    @abstractmethod
    def create(self, database: str) -> tuple[bool, str]:
        pass

    """
    Instantiates a new DBRecord object by retrieving the record with the specified primary key from the database
    """
    @abstractmethod
    def read(self, database: str):
        pass
    """
    Updates the corresponding record in the database to match the DBRecord object
    """
    @abstractmethod
    def update(self, database: str) -> tuple[bool, str]:
        pass

    """
    Deletes the record with the specified primary key from the database
    """
    @abstractmethod
    def delete(self, database: str) -> bool:
        pass

class Unit(DBRecord):


