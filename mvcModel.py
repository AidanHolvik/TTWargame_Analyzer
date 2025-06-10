import sqlite3
import re

SQL_TABLES = [
    """CREATE TABLE IF NOT EXISTS Units(
        name TEXT PRIMARY KEY,
        points_cost INTEGER DEFAULT 0 CHECK(points_cost >= 0)
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

    """CREATE TABLE IF NOT EXISTS AssignedKeywords(
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
    );""",

]

def regexp(x, y, search=re.search):
    return 1 if search(x,y) else 0

try:
    with sqlite3.connect('TTWGAnalyzer.db') as conn:
        conn = sqlite3.connect('TTWGAnalyzer.db')
        print(f'Opened SQLite database with version {sqlite3.sqlite_version}.')
        cursor = conn.cursor()

        # Create tables
        for table in SQL_TABLES:
            print(table, '\n')
            cursor.execute(table)

        # TODO: main code

except sqlite3.OperationalError as e:
    print('Failed:', e)