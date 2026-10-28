INSERT INTO units (id, name)
VALUES
    (1, 'Breacher Team');

INSERT INTO models (id, name, movement, toughness, save, health)
VALUES
    (1, "Breacher Shas'ui", 6, 3, 4, 7, 1),
    (2, "Breacher Fire Warrior", 6, 3, 4, 7, 1);

INSERT INTO unit_models (unit_id, model_id, quantity)
VALUES
    (1, 1, 1),
    (1, 2, 9);

INSERT INTO weapons (id, name, attacks, skill, strength, ap, damage)
VALUES
    (1, "Pulse Blaster", 2, 3, 6, 1, 1),
    (2, "Pulse Pistol", 1, 4, 5, 0, 1),
    (3, "Support Turret", 2, 5, 5, 0, 1),
    (4, "Close Combat Weapon", 1, 5, 3, 0, 1),
    (5, "Pulse Blaster", 2, 3, 6, 1, 1),
    (6, "Pulse Pistol", 1, 4, 5, 0, 1);

INSERT INTO model_weapons (model_id, weapon_id, quantity)
VALUES
    (1, 1, 1),
    (1, 2, 1),
    (1, 3, 1),
    (1, 4, 1),
    (2, 5, 1),
    (2, 6, 1);
