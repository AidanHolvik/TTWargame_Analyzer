import sqlite3
from abc import ABC, abstractmethod
import re

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

class DBRecord(ABC):

    @abstractmethod
    def __eq__(self, that):
        pass

    """
    Generates a tuple which can be used to generate a record matching the DBRecord object
    """
    @abstractmethod
    def record(self):
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