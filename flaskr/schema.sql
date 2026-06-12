DROP TABLE IF EXISTS weapon;
DROP TABLE IF EXISTS defense;

CREATE TABLE weapon (
    id INT PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    attacks TEXT NOT NULL,
    skill INT NOT NULL,
    strength INT NOT NULL,
    ap INT NOT NULL,
    damage TEXT NOT NULL
)

CREATE TABLE defense (
    id INT PRIMARY KEY AUTOINCREMENT,
    toughness INT NOT NULL,
    save INT NOT NULL
)