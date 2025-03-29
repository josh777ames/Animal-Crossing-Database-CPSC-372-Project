# CPSC-372-Project - Animal Crossing Tracker

Name: Josh Ames

## Description
Being a collecting game at its core, Animal Crossing contains a plethora of things for the player to collect. This tracker allows players to keep track of their in-game collections. These include items, villagers, fish, bugs, sea critters, artwork, flowers, and more. Players can organize their collections, monitor progress on tasks such as breeding flowers or completing the museum donations, and find which creatures, items, or interactions are available at any given time based on in-game schedules (fish, bugs, and sea critters are time sensitive and vary from month to month and at different hours of the day).

## Proposed Entities
Possible entities for this tracker include (and will most likely increase):
- Items: Differentiated between crafting materials, furniture, clothing, etc.
- Fish: Trackable by season, time of day, and location.
- Bugs: Trackable by season, time of day, and location.
- Sea Critters: Trackable by season, and time of day.
    - Fish and sea critters also have different shadow sizes in the water and behaviors that may be beneficial to add for the convenience of the user when trying to catch them.
- Villagers: Track which villagers are on the player's island and whether they have interacted with them on a particular day. (interacting with villagers could become a daily task implementation)
- Daily Tasks: Track things like digging up fossils, hitting stones, lanting the money tree (things that the player does every day).
- Artwork: Monitor what artwork has been collected.
- Flowers: Track what flowers have been or are yet to be bred.
- Museum: Tracks donations of fish, bugs, sea critters, artwork, and fossils. (on top of collecting these things players can donate them to complete the in game museum)
    - I may make this just a boolean inside of the other entities for simplicity
- Completion Status: An aggregate entity tracking the player's progress across all collections.
- Available Creatures: This table will display all fish, bugs, and sea critters available for capture at the current time, based on the current season and time of day.
    - Completion status and available creatures are more like use cases for the above entities 
- Currently tracking/ Wishlist: Users can add things that they are actively trying to get. They can specify amounts of certain items that they may want to get (this could be useful for a user who wants specific items to decorate/ plan their island)

## Proposed Technology Stack
- Programming Language: Python
- UI Approach: Web interface
- Database Type: SQLite
- Frameworks: Flask just for a simple web interface

## CRUD Operations
- Create New Data:
Users will be able to add new entries, such as new villagers or new items they've collected through the web interface. I imagine, just for simplicity, having checkboxes and a search bar for items.
- View/Read Existing Data:
Users can view their collections on the main dashboard. This will show what they have collected so far and what items or creatures are still missing. The available creatures table will show what can be caught at the current time.
- Update Existing Data:
Users will update their collection progress, mark items as donated to the museum, and update daily tasks when they interact with villagers or complete certain things around their island. Also they can update which items from their wishlist they have collected.
- Delete Data:
Users will be able to delete or remove items from their wishlist or remove villagers that have left their island.
