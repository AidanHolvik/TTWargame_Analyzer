DROP TABLE IF EXISTS model_loadouts;
DROP TABLE IF EXISTS unit_models;
DROP TABLE IF EXISTS weapons;
DROP TABLE IF EXISTS models;
DROP TABLE IF EXISTS units;

-- TODO: include keywords and abilities?
CREATE TABLE units (
  id INT PRIMARY KEY,
  name TEXT UNIQUE
  -- TODO: add field for faction so users can filter/sort?
);

-- TODO: include keywords and abilities?
CREATE TABLE models (
  id INT PRIMARY KEY,
  name TEXT,
  movement INT,
  toughness INT,
  save INT,
  invuln_save INT,
  health INT
);

-- TODO: include keywords
CREATE TABLE weapons (
  id INT PRIMARY KEY,
  name TEXT,
  attacks TEXT,
  skill INT,
  strength INT,
  ap INT,
  damage TEXT
);

CREATE TABLE model_loadouts (
  model_id INT,
  weapon_id INT UNIQUE,
  quantity INT,   -- TODO: constrain quantity to >= 1 (or maybe >= 0)

  CONSTRAINT fk_model
  FOREIGN KEY (model_id)
  REFERENCES models.id,

  CONSTRAINT fk_weapon
  FOREIGN KEY (weapon_id)
  REFERENCES weapons.id,

  CONSTRAINT pk PRIMARY KEY (model_id, weapon_id)
);

CREATE TABLE unit_models (
  unit_id INT,
  model_id INT UNIQUE,
  quantity INT,   -- TODO: constrain quantity to >= 1 (or maybe >= 0)

  CONSTRAINT fk_unit
  FOREIGN KEY (unit_id)
  REFERENCES units.id,

  CONSTRAINT fk_model
  FOREIGN KEY (model_id)
  REFERENCES models.id,

  CONSTRAINT pk PRIMARY KEY (fk_unit, fk_model)
);
