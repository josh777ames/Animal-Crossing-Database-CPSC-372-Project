# CPSC-372-Project - Animal Crossing Tracker

Name: Josh Ames

## Description
Being a collecting game at its core, Animal Crossing contains a plethora of things for the player to collect. This tracker allows players to keep track of their in-game collections. These include items, villagers, fish, bugs, sea critters, artwork, flowers, and more. Players can organize their collections, monitor progress on tasks such as completing the museum donations, and find which creatures, items, or interactions are available at any given time based on in-game schedules (fish, bugs, and sea critters are time sensitive and vary from month to month and at different hours of the day).

## Installation
To begin, download the main to your computer and open the file in Pycharm.
In the pycharm project, click on the python interpreter selector and select Add New Interpreter. Select Add Local Interpreter and create the virtual environment.

Then install the required packages with:
pip install pandas flask

With these installed you may now start by running all cells in the animal-crossing-query.ipynb notebook.
This notebook will create the database and seed it with data. It also demonstrates some of the query capabilities of the database.

After doing this you may run the app.py file.
The server will start at http://127.0.0.1:8080

## Use
From here you will be met with the log in screen.
Either use the already seeded user:
Username: ExampleUser
Password: password123
Or create your own user by clicking the sign up.

For those creating a new user, try adding items such as Mona Lisa, Bluegill, Whale Shark, Firefly, Mammoth Torso, or Floral Dress
    - You may also try adding these to the wishlist (view what happens when adding an item to the owned lsit when it already exists in wishlist)
Add villagers such as Raymond, Audie, Sherb, Diana, Julian, or Fang
Try donating items to the museum and view museum progress and item progress at the bottom (view what happens when you donate an item that is in your owned list with a qauntity of 1)
You may also remove things like villagers or items in the wishlist by pressing buttons with a ❌.
Try tracking the number of stones and fossils you hit/dug.

This database has 13 different tables that all interact with each other:
- Items: Differentiated between crafting materials, furniture, clothing, etc.
- Fish: Trackable by season, time of day, and location.
- Bugs: Trackable by season, time of day, and location.
- Sea_Critters: Trackable by season, and time of day.
- Villagers: Track which villagers are on the player's island and whether they have interacted with them on a particular day. (interacting with villagers could become a daily task implementation)
- Flower_Color: trakcs the color of different flowers. Different colors of flowers are tied to the same itemID
    - Example red rose, blue rose, and yellow rose all share the itemid for rose but different composite keys
    - Note: current implementation does not differentiate color due to time constraints, but the table exists for future implementation of viewing.
- Island_Villager: Table containing the user's current villagers on their island
    - Also used to track if the user has interacted with a villager on that day. This column can be reset to 0 for the start of a new day.
- User: Tracks users
- Wishlist: Users can add things that they are actively trying to get. They can specify amounts of certain items that they may want to get (this could be useful for a user who wants specific items to decorate/ plan their island)
- User_Item: track items that have been obtained by the user.
    - When an item is added to this table it decreases the amount of the item in the wishlist (if it exists in the user's wishlist) and deletes the wishlist entry should it reach 0.
- Museum: Tracks donations of fish, bugs, sea critters, artwork, and fossils. (on top of collecting these things players can donate them to complete the in game museum)
    - When an item is donated, the quantity of the item is decreased by 1 (if it exists in the user's user_item table) and deletes the user_item entry should the quantity reach 0.
- Daily_Stone: tracks the stones a user will hit every day. Can be reset to 0 for the start of a new day.
- Daily_Fossil:  tracks the fossils a user will dig up every day. Can be reset to 0 for the start of a new day.

## Technology Stack
- Programming Language: Python
- UI Approach: Web interface
- Database Type: SQLite
- Frameworks: Flask just for a simple web interface

## CRUD Operations
- Create New Data:
Users can add new entries, such as new villagers or new items they've collected through the web interface.
- View/Read Existing Data:
Users can view their collections on the main dashboard. This will show what they have collected so far and what items or creatures are still missing.
- Update Existing Data:
Users can update their collection progress, mark items as donated to the museum, and update daily tasks when they interact with villagers or complete certain things around their island. Also they can update which items from their wishlist they have collected.
- Delete Data:
Users are able to delete or remove items from their wishlist or remove villagers that have left their island.
