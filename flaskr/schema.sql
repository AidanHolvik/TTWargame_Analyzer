DROP TABLE IF EXISTS model_weapons;
DROP TABLE IF EXISTS unit_models;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS units;

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

-- TODO: create query (view) for viewing all weapons & their quantities in a unit
