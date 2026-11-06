INSERT INTO units (id, name)
VALUES
(1, 'Unit 1'),
(2, 'Unit no_models');

INSERT INTO models (id, name, movement, toughness, save, invuln_save, health)
VALUES
(1, "Model 1", 6, 3, 4, 7, 1),
(2, "Model 2", 6, 3, 4, 7, 1);

INSERT INTO unit_models (unit_id, model_id, quantity)
VALUES
(1, 1, 1),
(1, 2, 9);

INSERT INTO weapons (id, name, attacks, skill, strength, ap, damage)
VALUES
(1, "Weapon  1a", 2, 3, 6, 1, 1),
(2, "Weapon 2a", 1, 4, 5, 0, 1),
(3, "Weapon 3", 2, 5, 5, 0, 1),
(4, "Weapon 4a", 1, 5, 3, 0, 1),
(5, "Weapon 1b", 2, 3, 6, 1, 1),
(6, "Weapon 2b", 1, 4, 5, 0, 1),
(7, "Weapon 4b", 1, 5, 3, 0, 1);

INSERT INTO model_weapons (model_id, weapon_id, quantity)
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1),
(1, 4, 1),
(2, 5, 1),
(2, 6, 1),
(2, 7, 1);
