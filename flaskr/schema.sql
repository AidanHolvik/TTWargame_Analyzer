DROP TABLE IF EXISTS model_weapons;
DROP TABLE IF EXISTS unit_models;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS abilities;
DROP TABLE IF EXISTS unit_abilities;
DROP TABLE IF EXISTS model_abilities;
DROP TABLE IF EXISTS weapon_abilities;

-- TODO: include keywords and abilities?
CREATE TABLE units (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL
  -- TODO: add field for faction so users can filter/sort?
);

-- TODO: include keywords and abilities?
CREATE TABLE models (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  movement INTEGER,
  toughness INTEGER,
  save INTEGER,
  invuln_save INTEGER,
  health INTEGER
);

-- TODO: include keywords
CREATE TABLE weapons (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  attacks TEXT,
  skill INTEGER,
  strength INTEGER,
  ap INTEGER,
  damage TEXT
);

CREATE TABLE model_weapons (
  model_id INTEGER NOT NULL,
  weapon_id INTEGER NOT NULL,
  quantity INTEGER,   -- TODO: constrain quantity to >= 0

  FOREIGN KEY (model_id)
  REFERENCES models (id)
  ON DELETE CASCADE,

  FOREIGN KEY (weapon_id)
  REFERENCES weapons (id)
  ON DELETE CASCADE,

  PRIMARY KEY (model_id, weapon_id)
);

CREATE TABLE unit_models (
  unit_id INTEGER NOT NULL,
  model_id INTEGER NOT NULL,
  quantity INTEGER,   -- TODO: constrain quantity to >= 0

  FOREIGN KEY (unit_id)
  REFERENCES units (id)
  ON DELETE CASCADE,

  FOREIGN KEY (model_id)
  REFERENCES models (id)
  ON DELETE CASCADE,

  PRIMARY KEY (unit_id, model_id)
);

CREATE TABLE keywords (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE abilities (
  id INTEGER PRIMARY KEY,
  effect TEXT UNIQUE NOT NULL
);

CREATE TABLE unit_abilities (
  unit_id INTEGER NOT NULL,
  ability_id INTEGER NOT NULL,
  name TEXT NOT NULL,   -- TODO: constrain name to be one of the abilities in the game
  value INTEGER,   -- TODO: constrain value to >= 0

  FOREIGN KEY (unit_id)
  REFERENCES units (id)
  ON DELETE CASCADE,

  FOREIGN KEY (ability_id)
  REFERENCES abilities (id)
  ON DELETE CASCADE,

  PRIMARY KEY (unit_id, ability_id)
);

CREATE TABLE model_abilities (
  model_id INTEGER NOT NULL,
  ability_id INTEGER NOT NULL,
  name TEXT NOT NULL,   -- TODO: constrain name to be one of the abilities in the game
  value INTEGER,   -- TODO: constrain value to >= 0

  FOREIGN KEY (model_id)
  REFERENCES models (id)
  ON DELETE CASCADE,

  FOREIGN KEY (ability_id)
  REFERENCES abilities (id)
  ON DELETE CASCADE,

  PRIMARY KEY (model_id, ability_id)
);

CREATE TABLE weapon_abilities (
  weapon_id INTEGER NOT NULL,
  ability_id INTEGER NOT NULL,
  name TEXT NOT NULL,   -- TODO: constrain name to be one of the abilities in the game
  value INTEGER,   -- TODO: constrain value to >= 0
  target_keyword TEXT,   -- TODO: constrain keyword to be one of the keywords in the game

  FOREIGN KEY (weapon_id)
  REFERENCES weapons (id)
  ON DELETE CASCADE,

  FOREIGN KEY (ability_id)
  REFERENCES abilities (id)
  ON DELETE CASCADE,

  FOREIGN KEY (target_keyword)
  REFERENCES keywords (name)
  ON DELETE CASCADE,

  PRIMARY KEY (weapon_id, ability_id)
);

INSERT INTO keywords (name) VALUES
('BATTLELINE'),
('SWARM'),
('INFANTRY'),
('BEAST'),
('MOUNTED'),
('MONSTER'),
('VEHICLE'),
('AIRCRAFT'),
('FRAME'),
('CHARACTER'),
('EPIC HERO'),
('WALKER'),
('TITANIC'),
('TOWERING'),
('FORTIFICATION'),
('PSYKER'),
('ARTILLERY'),
('GRENADES'),
('SMOKE'),
('FLY'),
('TRANSPORT'),
('DEDICATED TRANSPORT'),
('IMPERIUM'),
('CHAOS'),
('DAEMON');

INSERT INTO abilities (effect) VALUES
('Feel No Pain'),
('AP on crit wound'),
('ANTI-'),
('BLAST/CLEAVE'),
('CLOSE QUARTERS'),
('DEVASTATING WOUNDS'),
('INDIRECT FIRE'),
('LETHAL HITS'),
('MELTA'),
('PSYCHIC'),
('RAPID FIRE'),
('SUSTAINED HITS'),
('TORRENT'),
('TWIN-LINKED'),
('CONVERSION');

CREATE VIEW propagated_abilities AS
SELECT
  weapon_id,
  ability_id,
  name,
  value,
  target_keyword
FROM weapon_abilities
UNION
SELECT
  weapons.weapon_id,
  abilities.ability_id,
  abilities.name,
  abilities.value,
  abilities.target_keyword
FROM model_abilities AS abilities
INNER JOIN model_weapons AS weapons ON abilities.model_id = weapons.model_id
UNION
SELECT
  weapons.weapon_id,
  abilities.ability_id,
  abilities.name,
  abilities.value,
  abilities.target_keyword
FROM unit_abilities AS abilities
INNER JOIN unit_models AS models ON abilities.unit_id = models.unit_id
INNER JOIN model_weapons AS weapons ON models.model_id = weapons.model_id;
