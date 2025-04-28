-- drop tables if they exist
DROP TABLE IF EXISTS DAILY_STONE;
DROP TABLE IF EXISTS DAILY_FOSSIL;
DROP TABLE IF EXISTS ISLAND_VILLAGER;
DROP TABLE IF EXISTS WISHLIST;
DROP TABLE IF EXISTS USER_ITEM;
DROP TABLE IF EXISTS MUSEUM;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS FLOWER_COLOR;
DROP TABLE IF EXISTS FLOWER;
DROP TABLE IF EXISTS SEA_CRITTER;
DROP TABLE IF EXISTS BUG;
DROP TABLE IF EXISTS FISH;
DROP TABLE IF EXISTS VILLAGER;
DROP TABLE IF EXISTS ITEM;



-- creating item table which stores item names and category
CREATE TABLE ITEM (
    ItemID TEXT PRIMARY KEY,
    Name TEXT NOT NULL,
    Category TEXT CHECK (Category IN ('CRAFTING', 'FURNITURE', 'CLOTHING', 'FLOWER', 'ARTWORK', 'FISH', 'BUG', 'SEA_CRITTER', 'FOSSIL')) NOT NULL
);

-- fish table has itemid foreign key and the information related to fish
CREATE TABLE FISH (
    ItemID TEXT PRIMARY KEY,
    CatchableMonth TEXT,
    CatchableTimeOfDay TEXT,
    Location TEXT,
    ShadowSize TEXT,
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- bug table has itemid foreign key and the information related to bugs
CREATE TABLE BUG (
    ItemID TEXT PRIMARY KEY,
    CatchableMonth TEXT,
    CatchableTimeOfDay TEXT,
    Location TEXT,
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- sea critter table has itemid foreign key and the information related to sea critters
CREATE TABLE SEA_CRITTER (
    ItemID TEXT PRIMARY KEY,
    CatchableMonth TEXT,
    CatchableTimeOfDay TEXT,
    ShadowSize TEXT,
    Behavior TEXT,
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- flower table has itemid foreign key and exists as different colors of flowers are tied to the same itemID
-- example red rose, blue rose, and yellow rose all share the itemid for rose
CREATE TABLE FLOWER_COLOR (
    ItemID TEXT,
    Color TEXT,
    PRIMARY KEY (ItemID, Color),
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- table for villagers containing all the possible villagers
CREATE TABLE VILLAGER (
    VillagerID TEXT PRIMARY KEY,
    Name TEXT NOT NULL,
    Personality TEXT,
    Species TEXT
);

-- user table
CREATE TABLE USER (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL
);

-- user item tracks items owned by the user
CREATE TABLE USER_ITEM (
    UserID INTEGER,
    ItemID TEXT,
    QuantityOwned INTEGER,
    PRIMARY KEY (UserID, ItemID),
    FOREIGN KEY (UserID) REFERENCES USER(UserID),
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- museum tracks the items donated by the user
CREATE TABLE MUSEUM (
    UserID TEXT,
    ItemID TEXT,
    PRIMARY KEY (UserID, ItemID),
    FOREIGN KEY (UserID) REFERENCES USER(UserID),
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- wishlist contains items that the user wants
CREATE TABLE WISHLIST (
    UserID INTEGER,
    ItemID TEXT,
    WishlistQuantity INTEGER,
    PRIMARY KEY (UserID, ItemID),
    FOREIGN KEY (UserID) REFERENCES USER(UserID),
    FOREIGN KEY (ItemID) REFERENCES ITEM(ItemID)
);

-- complicated trigger, but it does two things: lowers the WishlistQuantity when a wishlist item is obtained
-- by the amount obtained, and if the WishlistQuantity goes to 0 or below, the entry is deleted
CREATE TRIGGER WISHLIST_OBTAINED
AFTER INSERT ON USER_ITEM
FOR EACH ROW
BEGIN
    UPDATE WISHLIST
    SET WishlistQuantity = WishlistQuantity - NEW.QuantityOwned
    WHERE UserID = NEW.UserID AND ItemID = NEW.ItemID;
    DELETE FROM WISHLIST
    WHERE UserID = NEW.UserID AND ItemID = NEW.ItemID AND WishlistQuantity <= 0;
END;

-- very similar as above but for updates
CREATE TRIGGER WISHLIST_OBTAINED_UPDATE
AFTER UPDATE OF QuantityOwned ON USER_ITEM
FOR EACH ROW
    -- this line below makes sure we do not subtract from wishlist if the update is actually decreasing in quantity
    WHEN NEW.QuantityOwned > OLD.QuantityOwned
BEGIN
    UPDATE WISHLIST
    SET WishlistQuantity = WishlistQuantity - (NEW.QuantityOwned - OLD.QuantityOwned)
    WHERE UserID = NEW.UserID AND ItemID = NEW.ItemID;
    DELETE FROM WISHLIST
    WHERE UserID = NEW.UserID AND ItemID = NEW.ItemID AND WishlistQuantity <= 0;
END;

-- table for villagers on the user's island
CREATE TABLE ISLAND_VILLAGER (
    VillagerID TEXT,
    UserID INTEGER,
    TalkedToday BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (UserID, VillagerID),
    FOREIGN KEY (UserID) REFERENCES USER(UserID),
    FOREIGN KEY (VillagerID) REFERENCES VILLAGER(VillagerID)
);

-- players are limited to 10 villagers per island
CREATE TRIGGER MAX_VILLAGERS
BEFORE INSERT ON ISLAND_VILLAGER
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN (SELECT COUNT(*) FROM ISLAND_VILLAGER WHERE UserID = NEW.UserID) >= 10
        THEN
            RAISE (IGNORE)
    END;
END;


-- table for daily fossils, must be seeded upon creation of user
CREATE TABLE DAILY_FOSSIL (
    UserID INTEGER,
    FossilNumber INTEGER,
    DugToday BOOLEAN NOT NULL,
    PRIMARY KEY (UserID, FossilNumber),
    FOREIGN KEY (UserID) REFERENCES USER(UserID)
);

-- table for daily stones, must be seeded upon creation of user
CREATE TABLE DAILY_STONE (
    UserID INTEGER,
    StoneNumber INTEGER,
    HitToday BOOLEAN NOT NULL,
    PRIMARY KEY (UserID, StoneNumber),
    FOREIGN KEY (UserID) REFERENCES USER(UserID)
);
