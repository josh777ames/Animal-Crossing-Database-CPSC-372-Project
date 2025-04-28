-- ChatGPT 4o was used for this file for the value entries. Knowledge of Animal crossing
-- and the INSERT lines were given.

-- Seed static data for ITEM
INSERT INTO ITEM (ItemID, Name, Category) VALUES
('art001', 'Mona Lisa', 'ARTWORK'),
('art002', 'Starry Night', 'ARTWORK'),
('art003', 'The Scream', 'ARTWORK'),
('art004', 'The Birth of Venus', 'ARTWORK'),
('art005', 'Girl with a Pearl Earring', 'ARTWORK'),
('art006', 'The Persistence of Memory', 'ARTWORK'),
('art007', 'American Gothic', 'ARTWORK'),
('art008', 'The Great Wave off Kanagawa', 'ARTWORK'),
('art009', 'The Last Supper', 'ARTWORK'),
('art010', 'Vitruvian Man', 'ARTWORK'),
('fish001', 'Bluegill', 'FISH'),
('fish002', 'Tadpole', 'FISH'),
('fish003', 'Football Fish', 'FISH'),
('fish004', 'Golden Trout', 'FISH'),
('fish005', 'Koi', 'FISH'),
('fish006', 'Betta', 'FISH'),
('fish007', 'Whale Shark', 'FISH'),
('fish008', 'Stringfish', 'FISH'),
('fish009', 'Cherry Salmon', 'FISH'),
('fish010', 'Blue Marlin', 'FISH'),
('bug001', 'Common Butterfly', 'BUG'),
('bug002', 'Honeybee', 'BUG'),
('bug003', 'Dung Beetle', 'BUG'),
('bug004', 'Ladybug', 'BUG'),
('bug005', 'Violin Beetle', 'BUG'),
('bug006', 'Firefly', 'BUG'),
('bug007', 'Giant Stag', 'BUG'),
('bug008', 'Dung Beetle (Winter)', 'BUG'),
('bug009', 'Atlas Moth', 'BUG'),
('bug010', 'Bagworm', 'BUG'),
('sea001', 'Sea Urchin', 'SEA_CRITTER'),
('sea002', 'Sea Anemone', 'SEA_CRITTER'),
('sea003', 'Sea Pig', 'SEA_CRITTER'),
('sea004', 'Venus'' Flower Basket', 'SEA_CRITTER'),
('sea005', 'Sea Slug', 'SEA_CRITTER'),
('sea006', 'Vampire Squid', 'SEA_CRITTER'),
('sea007', 'Seaweed', 'SEA_CRITTER'),
('sea008', 'Horseshoe Crab', 'SEA_CRITTER'),
('sea009', 'Oyster', 'SEA_CRITTER'),
('sea010', 'Flatworm', 'SEA_CRITTER'),
('fossil001', 'T. Rex Skull', 'FOSSIL'),
('fossil002', 'Triceratops Skull', 'FOSSIL'),
('fossil003', 'Stegosaurus Tail', 'FOSSIL'),
('fossil004', 'Mammoth Torso', 'FOSSIL'),
('fossil005', 'Sabertooth Skull', 'FOSSIL'),
('fossil006', 'Brachiosaurus Tail', 'FOSSIL'),
('fossil007', 'Ankylosaurus Skull', 'FOSSIL'),
('fossil008', 'Pteranodon Wing', 'FOSSIL'),
('fossil009', 'Dimetrodon Torso', 'FOSSIL'),
('fossil010', 'Ichthyosaur Skull', 'FOSSIL'),
('flower001', 'Rose', 'FLOWER'),
('flower002', 'Tulip', 'FLOWER'),
('flower003', 'Cosmos', 'FLOWER'),
('flower004', 'Hyacinth', 'FLOWER'),
('flower005', 'Lily', 'FLOWER'),
('flower006', 'Mum', 'FLOWER'),
('flower007', 'Windflower', 'FLOWER'),
('flower008', 'Pansy', 'FLOWER'),
('furn001', 'Wooden Chair', 'FURNITURE'),
('furn002', 'Ironwood Table', 'FURNITURE'),
('furn003', 'Simple Bed', 'FURNITURE'),
('furn004', 'Bookshelf', 'FURNITURE'),
('furn005', 'Rattan Wardrobe', 'FURNITURE'),
('cloth001', 'Striped Tee', 'CLOTHING'),
('cloth002', 'Pleather Pants', 'CLOTHING'),
('cloth003', 'Bobby Socks', 'CLOTHING'),
('cloth004', 'Floral Dress', 'CLOTHING'),
('cloth005', 'Woolen Coat', 'CLOTHING'),
('craft001', 'Wood', 'CRAFTING'),
('craft002', 'Iron Nugget', 'CRAFTING'),
('craft003', 'Clay', 'CRAFTING'),
('craft004', 'Stone', 'CRAFTING'),
('craft005', 'Gold Nugget', 'CRAFTING');

-- Seed FISH
INSERT INTO FISH (ItemID, CatchableMonth, CatchableTimeOfDay, Location, ShadowSize) VALUES
('fish001', 'All Year', '9AM-4PM', 'River', 'Small'),      -- Bluegill
('fish002', 'Mar-Jun, Sep-Nov', '4PM-9AM', 'Pond', 'Tiny'),      -- Tadpole
('fish003', 'Dec-Mar', 'All Day', 'Sea', 'Medium'),           -- Football Fish
('fish004', 'Nov-Mar', 'All Day', 'River (Clifftop)', 'Large'), -- Golden Trout
('fish005', 'All Year', 'All Day', 'Pond', 'Large'),        -- Koi
('fish006', 'Apr-Sep', '4PM-9AM', 'River', 'Small'),             -- Betta
('fish007', 'May-Oct', 'All Day', 'Sea', 'Huge'),                -- Whale Shark
('fish008', 'Oct-Mar', 'All Day', 'River', 'Small'),             -- Stringfish
('fish009', 'May-Sep', '9AM-4PM', 'River', 'Medium'),      -- Cherry Salmon
('fish010', 'All Year', 'All Day', 'Pier', 'Huge');              -- Blue Marlin

-- Seed BUG
INSERT INTO BUG (ItemID, CatchableMonth, CatchableTimeOfDay, Location) VALUES
('bug001', 'Mar-Jun, Sep-Nov', '4AM-7PM', 'Flying'),        -- Common Butterfly
('bug002', 'Apr-Aug', '8AM-5PM', 'On Trees'),               -- Honeybee
('bug003', 'Jul-Aug', 'All Day', 'Ground'),                 -- Dung Beetle
('bug004', 'Mar-Oct', 'All Day', 'On Flowers'),             -- Ladybug
('bug005', 'Sep-Nov', 'All Day', 'On Tree Stumps'),         -- Violin Beetle
('bug006', 'May-Sep', '5PM-8AM', 'Near Water'),             -- Firefly
('bug007', 'Jul-Aug', '11PM-8AM', 'Ground'),                -- Giant Stag
('bug008', 'Dec-Feb', 'All Day', 'Snowballs'),              -- Dung Beetle (winter variant)
('bug009', 'Jul-Aug', 'All Day', 'Coconut Trees'),          -- Atlas Moth
('bug010', 'All Year', 'All Day', 'On Trees');              -- Bagworm


-- Seed SEA_CRITTER
INSERT INTO SEA_CRITTER (ItemID, CatchableMonth, CatchableTimeOfDay, ShadowSize, Behavior) VALUES
('sea001', 'Jun-Sep', 'All Day', 'Medium', 'Fast'),           -- Sea Urchin
('sea002', 'All Year', '4PM-9AM', 'Large', 'Slow'),           -- Sea Anemone
('sea003', 'Nov-Feb', 'All Day', 'Small', 'Stationary'),      -- Sea Pig
('sea004', 'Dec-Mar', 'All Day', 'Medium', 'Fast'),           -- Venus' Flower Basket
('sea005', 'May-Sep', 'All Day', 'Small', 'Slow'),            -- Sea Slug
('sea006', 'Jun-Sep', 'All Day', 'Large', 'Very Fast'),       -- Vampire Squid
('sea007', 'All Year', 'All Day', 'Tiny', 'Stationary'),      -- Seaweed
('sea008', 'Jul-Sep', '4PM-9AM', 'Medium', 'Medium'),         -- Horseshoe Crab
('sea009', 'Oct-Dec', '9AM-4PM', 'Tiny', 'Slow'),             -- Oyster
('sea010', 'May-Jul', 'All Day', 'Small', 'Fast');            -- Flatworm


-- Seed FLOWER_COLOR
INSERT INTO FLOWER_COLOR (ItemID, Color) VALUES
('flower001', 'Red'),
('flower001', 'White'),
('flower001', 'Yellow'),
('flower001', 'Blue'),
('flower001', 'Black'),
('flower001', 'Purple'),
('flower002', 'Red'),
('flower002', 'Yellow'),
('flower002', 'White'),
('flower002', 'Pink'),
('flower002', 'Purple'),
('flower003', 'Red'),
('flower003', 'Yellow'),
('flower003', 'White'),
('flower004', 'Blue'),
('flower004', 'Yellow'),
('flower004', 'White'),
('flower005', 'Orange'),
('flower005', 'White'),
('flower005', 'Yellow'),
('flower006', 'Pink'),
('flower006', 'Purple'),
('flower006', 'Green'),
('flower007', 'Orange'),
('flower007', 'White'),
('flower007', 'Blue'),
('flower008', 'Red'),
('flower008', 'Yellow'),
('flower008', 'White');

-- Seed 20 villagers into VILLAGER
INSERT INTO VILLAGER (VillagerID, Name, Personality, Species) VALUES
('vill001', 'Raymond', 'Smug', 'Cat'),
('vill002', 'Audie', 'Peppy', 'Wolf'),
('vill003', 'Sherb', 'Lazy', 'Goat'),
('vill004', 'Judy', 'Snooty', 'Cub'),
('vill005', 'Marshal', 'Smug', 'Squirrel'),
('vill006', 'Ankha', 'Snooty', 'Cat'),
('vill007', 'Stitches', 'Lazy', 'Cub'),
('vill008', 'Beau', 'Lazy', 'Deer'),
('vill009', 'Pietro', 'Smug', 'Sheep'),
('vill010', 'Diana', 'Snooty', 'Deer'),
('vill011', 'Maple', 'Normal', 'Cub'),
('vill012', 'Fauna', 'Normal', 'Deer'),
('vill013', 'Meringue', 'Normal', 'Rhino'),
('vill014', 'Poppy', 'Normal', 'Squirrel'),
('vill015', 'Bob', 'Lazy', 'Cat'),
('vill016', 'Lucky', 'Lazy', 'Dog'),
('vill017', 'Rosie', 'Peppy', 'Cat'),
('vill018', 'Fang', 'Cranky', 'Wolf'),
('vill019', 'Julian', 'Smug', 'Horse'),
('vill020', 'Whitney', 'Snooty', 'Wolf');

-- Seed User information
INSERT INTO USER (Username, Password) VALUES
('ExampleUser', 'password123');


INSERT OR IGNORE INTO USER_ITEM (UserID, ItemID, QuantityOwned) VALUES
('1', 'fish001', 2),
('1', 'bug001', 1),
('1', 'art001', 1),
('1', 'fossil001', 1),
('1', 'flower001', 3),
('1', 'flower002', 5),
('1', 'sea001', 1),
('1', 'sea003', 1),
('1', 'sea005', 2);

INSERT OR IGNORE INTO ISLAND_VILLAGER (VillagerID, UserID) VALUES
('vill011', '1'),
('vill012', '1'),
('vill013', '1');

INSERT OR IGNORE INTO ISLAND_VILLAGER (VillagerID, UserID, TalkedToday) VALUES
('vill014', '1', 1),
('vill015', '1', 1);

INSERT OR IGNORE INTO WISHLIST (UserID, ItemID, WishlistQuantity) VALUES
('1','art001', 2),
('1','art002', 3),
('1','art003', 1),
('1','furn001', 4),
('1','furn002', 4),
('1','furn003', 1),
('1','cloth004', 1),
('1','cloth005', 1),
('1','fossil003', 2),
('1','fossil004', 1),
('1','fossil005', 3),
('1','fossil006', 3),
('1','fossil007', 1),
('1', 'sea008', 1);

INSERT INTO DAILY_STONE (UserID, StoneNumber, HitToday) VALUES
(1, 1, 0),
(1, 2, 0),
(1, 3, 0),
(1, 4, 0),
(1, 5, 0),
(1, 6, 0);

INSERT INTO DAILY_FOSSIL (UserID, FossilNumber, DugToday) VALUES
(1, 1, 0),
(1, 2, 0),
(1, 3, 0),
(1, 4, 0);

