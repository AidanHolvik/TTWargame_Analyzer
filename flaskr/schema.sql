CREATE TABLE IF NOT EXISTS unit (
    id      INT     PRIMARY KEY,
    name    TEXT    UNIQUE
                    NOT NULL,
    cost    INT     NOT NULL
                    DEFAULT 0
                    CHECK(cost >= 0)
);

CREATE TABLE IF NOT EXISTS model(
    id          INT     PRIMARY KEY,
    unit        INT     NOT NULL,
    name        TEXT    NOT NULL,
    quantity    INT     NOT NULL 
                        DEFAULT 1 
                        CHECK(quantity > 0),
    toughness   INT     NOT NULL
                        CHECK(toughness > 0),
    save        INT     NOT NULL
                        CHECK(save > 1 AND save <= 7),
    health      INT     NOT NULL
                        CHECK(health > 0),
    invuln      INT     CHECK(invuln > 1 AND invuln <= 7),
    isLeader    TEXT    NOT NULL
                        DEFAULT 'False'
                        CHECK(isLeader IN ('True','False')),
    enabled     TEXT    NOT NULL
                        DEFAULT 'True'
                        CHECK(enabled in ('True','False')),
                FOREIGN KEY (unit) REFERENCES unit(id),
                CONSTRAINT fingerprint UNIQUE (unit, name)
);