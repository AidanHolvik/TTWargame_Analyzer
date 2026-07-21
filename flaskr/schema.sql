DROP TABLE IF EXISTS model_weapons;
DROP TABLE IF EXISTS unit_models;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS units;

-- TODO: include keywords and abilities?
CREATE TABLE units (
  id INT PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
  -- TODO: add field for faction so users can filter/sort?
);

-- TODO: include keywords and abilities?
CREATE TABLE models (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  movement INT,
  toughness INT,
  save INT,
  invuln_save INT,
  health INT
);

-- TODO: include keywords
CREATE TABLE weapons (
  id INT PRIMARY KEY,
  name TEXT NOT NULL,
  attacks TEXT,
  skill INT,
  strength INT,
  ap INT,
  damage TEXT
);

CREATE TABLE model_weapons (
  model_id INT,
  weapon_id INT UNIQUE,
  quantity INT,   -- TODO: constrain quantity to >= 0

  CONSTRAINT fk_model
  FOREIGN KEY (model_id)
  REFERENCES models (id),

  CONSTRAINT fk_weapon
  FOREIGN KEY (weapon_id)
  REFERENCES weapons (id),

  CONSTRAINT pk PRIMARY KEY (model_id, weapon_id)
);

CREATE TABLE unit_models (
  unit_id INT,
  model_id INT UNIQUE,
  quantity INT,   -- TODO: constrain quantity to >= 0

  FOREIGN KEY (unit_id)
  REFERENCES units (id),

  FOREIGN KEY (model_id)
  REFERENCES models (id),

  CONSTRAINT pk PRIMARY KEY (unit_id, model_id)
);

-- TODO: create query (view) for viewing all weapons & their quantities in a unit
