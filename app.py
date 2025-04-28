import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session


# initialize the flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# connect to database
def get_db_connection():
    return sqlite3.connect('./acnh.db')

# login
@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM USER WHERE Username = ? AND Password = ?', (username,password))
        user = cursor.fetchone()

        conn.close()

        # i personally struggle with front ends and needed assistance with sessions and so ChatGPT 4o
        # helped produce this if-else statement
        if user:
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

# signup
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('INSERT INTO USER (Username, Password) VALUES (?, ?)', (username, password))

            # Chatgpt 4o assisted in this line below as i was unsure how to access
            # the new autoincremented UserID
            user_id = cursor.lastrowid

            # daily stones and fossils require a UserID which means we must seed them when a new user is created
            for stone_number in range(1, 7):
                cursor.execute('INSERT INTO DAILY_STONE (UserID, StoneNumber, HitToday) VALUES (?, ?, 0)',
                               (user_id, stone_number))
            for fossil_number in range(1, 5):
                cursor.execute('INSERT INTO DAILY_FOSSIL (UserID, FossilNumber, DugToday) VALUES (?, ?, 0)',
                               (user_id, fossil_number))
            conn.commit()
            conn.close()

            # below is technically ChatGPT 4o? however i just followed the pattern from the signup
            # this time without using the if-else
            session['user_id'] = user_id
            session['username'] = username

            return redirect(url_for('home'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('signup.html', error="Username already taken.")

    return render_template('signup.html')

# logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


# home route - when i started this i wanted to just fit everything on the home page
# because having separate pages for simple tasks seemed redundant. i deeply regretted that decision as
# time went on. this home function is far too long and messy
@app.route("/home", methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session['user_id']

    # displaying daily tasks such as number of fossils founds, rocks hit, and villagers talked to
    cursor.execute('SELECT COUNT(*) FROM DAILY_STONE WHERE UserID = ? AND HitToday = 1', (user_id,))
    stones_hit = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM DAILY_FOSSIL WHERE UserID = ? AND DugToday = 1', (user_id,))
    fossils_dug = cursor.fetchone()[0]
    cursor.execute('''
        SELECT v.Name, iv.TalkedToday, v.VillagerID
        FROM ISLAND_VILLAGER iv
        JOIN VILLAGER v ON iv.VillagerID = v.VillagerID
        WHERE iv.UserID = ?
    ''', (user_id,))
    villagers = cursor.fetchall()

    # displaying user items
    # this list can get pretty long but i wanted to be able to show everything a user has, so
    # i asked chatgpt 4o if it could assist in creating a table showing 10 items at a time
    # it recommended this page and OFFSET set up. I made the rest of the query
    page = int(request.args.get('page', 0)) #

    cursor.execute('''
            SELECT i.Name, ui.QuantityOwned, i.Category
            FROM USER_ITEM ui
            JOIN ITEM i ON ui.ItemID = i.ItemID
            WHERE ui.UserID = ?
            LIMIT 10 OFFSET ?
        ''', (user_id, page * 10))
    user_items = cursor.fetchall()

    # search for villagers
    query = request.args.get('search')
    villager_search_results = None
    if query:
        cursor.execute('''
            SELECT Name, Species, VillagerID
            FROM VILLAGER
            WHERE Name LIKE ?
            AND VillagerID NOT IN (SELECT VillagerID FROM ISLAND_VILLAGER WHERE UserID = ?)
        ''', ('%' + query + '%', user_id))
        villager_search_results = cursor.fetchall()

    # search for items, not limited by what is owned so that finding items when updating quantity is easier
    item_query = request.args.get('item_search')
    item_search_results = None
    if item_query:
        cursor.execute('''
            SELECT Name, Category, ItemID
            FROM ITEM
            WHERE Name LIKE ?
        ''', ('%' + item_query + '%',))
        item_search_results = cursor.fetchall()

    # displaying wishlist
    cursor.execute('''
        SELECT i.Name, w.WishlistQuantity, i.ItemID
        FROM WISHLIST w
        JOIN ITEM i ON w.ItemID = i.ItemID
        WHERE w.UserID = ?
    ''', (user_id,))
    wishlist_items = cursor.fetchall()


    # these next few queries are for the tables showing things that have not been donated to the museum.
    # they use a lot of the same logic and i probably could have created a separate function for them all
    # rather than rewriting the code

    # fish
    cursor.execute('''
        SELECT i.Name, f.CatchableMonth, f.CatchableTimeOfDay, f.Location, f.ShadowSize, i.ItemID
        FROM ITEM i
        JOIN FISH f ON f.ItemID = i.ItemID
        WHERE i.Category = 'FISH'
        AND i.ItemID NOT IN (SELECT ItemID FROM MUSEUM WHERE UserID = ?)
    ''', (user_id,))
    undonated_fish = cursor.fetchall()

    # bugs
    cursor.execute('''
            SELECT i.Name, b.CatchableMonth, b.CatchableTimeOfDay, b.Location, i.ItemID
            FROM ITEM i
            JOIN BUG b ON b.ItemID = i.ItemID
            WHERE i.Category = 'BUG'
            AND i.ItemID NOT IN (SELECT ItemID FROM MUSEUM WHERE UserID = ?)
        ''', (user_id,))
    undonated_bug = cursor.fetchall()

    # sea critters
    cursor.execute('''
            SELECT i.Name, s.CatchableMonth, s.CatchableTimeOfDay, s.ShadowSize, s.Behavior, i.ItemID
            FROM ITEM i
            JOIN SEA_CRITTER s ON s.ItemID = i.ItemID
            WHERE i.Category = 'SEA_CRITTER'
            AND i.ItemID NOT IN (SELECT ItemID FROM MUSEUM WHERE UserID = ?)
        ''', (user_id,))
    undonated_sea_critter = cursor.fetchall()

    # fossils
    cursor.execute('''
            SELECT Name, ItemID
            FROM ITEM
            WHERE Category = 'FOSSIL'
            AND ItemID NOT IN (SELECT ItemID FROM MUSEUM WHERE UserID = ?)
        ''', (user_id,))
    undonated_fossil = cursor.fetchall()

    # artwork
    cursor.execute('''
            SELECT Name, ItemID
            FROM ITEM
            WHERE Category = 'ARTWORK'
            AND ItemID NOT IN (SELECT ItemID FROM MUSEUM WHERE UserID = ?)
        ''', (user_id,))
    undonated_artwork = cursor.fetchall()


    # lastly these are for completion progress percentages

    # museum progress
    # we loop through the categories of items that can be donated to get the total for museum and then fin what is stored in museum
    # we save this to a dictionary for later use where we find the percentage progress
    museum_categories = ['FISH', 'BUG', 'SEA_CRITTER', 'ARTWORK', 'FOSSIL']
    museum_progress = {}
    for category in museum_categories:
        cursor.execute('''
            SELECT COUNT(*)
            FROM ITEM
            WHERE Category = ?
        ''', (category,))
        total = cursor.fetchone()[0]

        cursor.execute('''
            SELECT COUNT(*)
            FROM MUSEUM m
            JOIN ITEM i ON m.ItemID = i.ItemID
            WHERE m.UserID = ?
            AND i.Category = ?
        ''', (user_id, category))
        donated = cursor.fetchone()[0]

        museum_progress[category] = {'donated': donated, 'total': total}


    # overall item progress similar to museum except we dont limit ITEM by category
    cursor.execute('''
        SELECT COUNT(*)
        FROM ITEM
    ''')
    total_items = cursor.fetchone()[0]

    cursor.execute('''
        SELECT COUNT(*)
        FROM USER_ITEM
        WHERE UserID = ?
        AND QuantityOwned > 0
    ''', (user_id,))
    owned_items = cursor.fetchone()[0]

    overall_progress = {'owned': owned_items, 'total': total_items}

    conn.close()

    return render_template("home.html",
                           username=session['username'],
                           stones_hit=stones_hit,
                           fossils_dug=fossils_dug,
                           villagers=villagers,
                           user_items=user_items,
                           items_current_page=page,
                           villager_search_results=villager_search_results,
                           item_search_results=item_search_results,
                           wishlist_items=wishlist_items,
                           undonated_fish=undonated_fish,
                           undonated_bug = undonated_bug,
                           undonated_sea_critter = undonated_sea_critter,
                           undonated_fossil = undonated_fossil,
                           undonated_artwork = undonated_artwork,
                           museum_progress=museum_progress,
                           overall_progress=overall_progress)


# this sets a villager as talked to
@app.route("/toggle_talked/<villager_id>", methods=['POST'])
def toggle_talked(villager_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE ISLAND_VILLAGER
        SET TalkedToday = CASE WHEN TalkedToday = 1 THEN 0 ELSE 1 END
        WHERE UserID = ? AND VillagerID = ?
    ''', (session['user_id'], villager_id))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# this sets a stone as hit
@app.route("/hit_stone", methods=['POST'])
def hit_stone():
    conn = get_db_connection()
    cursor = conn.cursor()

    # we limit by 1 to find the first stone to hit as the order does not matter
    cursor.execute('''
        SELECT StoneNumber
        FROM DAILY_STONE
        WHERE UserID = ? AND HitToday = 0
        ORDER BY StoneNumber
        LIMIT 1
    ''', (session['user_id'],))
    result = cursor.fetchone()

    # with that found we update the table
    if result:
        stone_number = result[0]
        cursor.execute('''
            UPDATE DAILY_STONE
            SET HitToday = 1
            WHERE UserID = ? AND StoneNumber = ?
        ''', (session['user_id'], stone_number))
        conn.commit()

    conn.close()
    return redirect(url_for('home'))

# this sets a fossil as being dug similar logic to hit_stone
@app.route("/dug_fossil", methods=['POST'])
def dug_fossil():
    conn = get_db_connection()
    cursor = conn.cursor()

    # liek with stones we limit by 1 as order doesnt matter
    cursor.execute('''
        SELECT FossilNumber
        FROM DAILY_FOSSIL
        WHERE UserID = ? AND DugToday = 0
        ORDER BY FossilNumber
        LIMIT 1
    ''', (session['user_id'],))
    result = cursor.fetchone()

    # with that found we set the fossil as dug
    if result:
        fossil_number = result[0]
        cursor.execute('''
            UPDATE DAILY_FOSSIL
            SET DugToday = 1
            WHERE UserID = ? AND FossilNumber = ?
        ''', (session['user_id'], fossil_number))
        conn.commit()

    conn.close()
    return redirect(url_for('home'))

# rather than overcomplicate the project with a clock that has to run a keep track of when days start we just let the user
# manage the new day by allowing them to reset villager interactions, hitting stones, and digging fossils to 0
@app.route("/reset_daily_tasks", methods=['POST'])
def reset_daily_tasks():
    conn = get_db_connection()
    cursor = conn.cursor()

    # reset all stones
    cursor.execute('''
        UPDATE DAILY_STONE
        SET HitToday = 0
        WHERE UserID = ?
    ''', (session['user_id'],))

    # reset all fossils
    cursor.execute('''
        UPDATE DAILY_FOSSIL
        SET DugToday = 0
        WHERE UserID = ?
    ''', (session['user_id'],))

    # reset all villager interactions
    cursor.execute('''
        UPDATE ISLAND_VILLAGER
        SET TalkedToday = 0
        WHERE UserID = ?
    ''', (session['user_id'],))

    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# adding villagers to user's island
@app.route("/add_villager/<villager_id>", methods=['POST'])
def add_villager(villager_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # we add a try block in case a villager is attempted to be added when it already exists
    try:
        cursor.execute('''
            INSERT INTO ISLAND_VILLAGER (VillagerID, UserID, TalkedToday)
            VALUES (?, ?, 0)
        ''', (villager_id, session['user_id']))
        conn.commit()
    except sqlite3.IntegrityError:
        pass

    conn.close()

    # there was an annoying thing with html that reloaded the page every time we submit a change. we use redirection anchors
    # which do a decent enough job at resolving this but it is still far from perfect and jarring when submitting
    return redirect(url_for('home') + "#villagers")

# deleting villagers from a user's island
@app.route("/remove_villager/<villager_id>", methods=['POST'])
def remove_villager(villager_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM ISLAND_VILLAGER
        WHERE UserID = ? AND VillagerID = ?
    ''', (session['user_id'], villager_id))

    conn.commit()
    conn.close()

    return redirect(url_for('home') + "#villagers")

# adding items to user items
@app.route("/add_item/<item_id>", methods=['POST'])
def add_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # we pull the quantity to increase by from the form
    quantity = int(request.form.get('quantity', 1))

    # we try an insert but if it already exists we instead update
    try:
        cursor.execute('''
            INSERT INTO USER_ITEM (UserID, ItemID, QuantityOwned)
            VALUES (?, ?, ?)
        ''', (session['user_id'], item_id, quantity))
        conn.commit()
    except sqlite3.IntegrityError:
        # updating we add the inputted quantity to the quantityowned to get the final quantityowned
        cursor.execute('''
            UPDATE USER_ITEM
            SET QuantityOwned = QuantityOwned + ?
            WHERE UserID = ? AND ItemID = ?
        ''', (quantity, session['user_id'], item_id))
        conn.commit()

    conn.close()
    return redirect(url_for('home') + "#myitems")

# users are able to decrease oe increase the quantity of items simply by looking at them in their items table
# we add this function to allow them to do preform those updates
@app.route("/update_item_quantity/<item_name>/<action>", methods=['POST'])
def update_item_quantity(item_name, action):
    conn = get_db_connection()
    cursor = conn.cursor()

    # first we get itemid from the name
    cursor.execute('SELECT ItemID FROM ITEM WHERE Name = ?', (item_name,))
    item_row = cursor.fetchone()

    # we check that teh query wasnt empty
    if item_row:
        item_id = item_row[0]

        # update for increasing quantity
        if action == 'increase':
            cursor.execute('''
                UPDATE USER_ITEM
                SET QuantityOwned = QuantityOwned + 1
                WHERE UserID = ? AND ItemID = ?
            ''', (session['user_id'], item_id))
        elif action == 'decrease':
            # update for decreasing quantity
            cursor.execute('''
                UPDATE USER_ITEM
                SET QuantityOwned = QuantityOwned - 1
                WHERE UserID = ? AND ItemID = ?
            ''', (session['user_id'], item_id))

            # if the quantity ever goes to 0 we delete the entry
            cursor.execute('''
                DELETE FROM USER_ITEM
                WHERE UserID = ? AND ItemID = ? AND QuantityOwned <= 0
            ''', (session['user_id'], item_id))

        conn.commit()

    conn.close()
    return redirect(url_for('home') + "#myitems")

# very similar to the user items update to quantity but this is for wishlist
@app.route("/update_wishlist_quantity/<item_id>/<action>", methods=['POST'])
def update_wishlist_quantity(item_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()

    # update for increasing quantity
    if action == 'increase':
        cursor.execute('''
            UPDATE WISHLIST
            SET WishlistQuantity = WishlistQuantity + 1
            WHERE UserID = ? AND ItemID = ?
        ''', (session['user_id'], item_id))
    # update for decreasing quantity
    elif action == 'decrease':
        cursor.execute('''
            UPDATE WISHLIST
            SET WishlistQuantity = WishlistQuantity - 1
            WHERE UserID = ? AND ItemID = ?
        ''', (session['user_id'], item_id))

        # delete if it reaches 0
        cursor.execute('''
            DELETE FROM WISHLIST
            WHERE UserID = ? AND ItemID = ? AND WishlistQuantity <= 0
        ''', (session['user_id'], item_id))

    conn.commit()
    conn.close()

    return redirect(url_for('home') + "#wishlist")

# removing a wishlist entry
@app.route("/remove_wishlist_item/<item_id>", methods=['POST'])
def remove_wishlist_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM WISHLIST
        WHERE UserID = ? AND ItemID = ?
    ''', (session['user_id'], item_id))

    conn.commit()
    conn.close()

    return redirect(url_for('home') + "#wishlist")

# adding a wishlist entry
@app.route("/add_to_wishlist/<item_id>", methods=['POST'])
def add_to_wishlist(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # like with items we pull quantity from the form
    quantity = int(request.form.get('quantity', 1))

    # we try to insert the entry and if it exists we update instead
    try:
        cursor.execute('''
            INSERT INTO WISHLIST (UserID, ItemID, WishlistQuantity)
            VALUES (?, ?, ?)
        ''', (session['user_id'], item_id, quantity))
        conn.commit()
    except sqlite3.IntegrityError:
        # again when updating quantity we simply add the increase of quantity to the old one
        cursor.execute('''
            UPDATE WISHLIST
            SET WishlistQuantity = WishlistQuantity + ?
            WHERE UserID = ? AND ItemID = ?
        ''', (quantity, session['user_id'], item_id))
        conn.commit()

    conn.close()
    return redirect(url_for('home') + "#wishlist")

# inserts an item into the museum table to mark as doanted
@app.route("/mark_donated/<item_id>", methods=['POST'])
def mark_donated(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    user_id = session['user_id']

    # When a user donates to the museum they actually lose the item so we must do several things
    # first we try inserting the item into museum
    try:
        cursor.execute('''
            INSERT INTO MUSEUM (UserID, ItemID)
            VALUES (?, ?)
        ''', (user_id, item_id))
    # if for some reason the item was already donated
    except sqlite3.IntegrityError:
        pass

    # now we find the item in their user items if they added it to their items
    cursor.execute('''
        SELECT QuantityOwned
        FROM USER_ITEM
        WHERE UserID = ? AND ItemID = ?
    ''', (user_id, item_id))
    result = cursor.fetchone()

    # if it is found we update the quantity and decrease by 1. we reuse logic from update item quantity
    if result:
        quantity = result[0]
        cursor.execute('''
                        UPDATE USER_ITEM
                        SET QuantityOwned = QuantityOwned - 1
                        WHERE UserID = ? AND ItemID = ?
                    ''', (session['user_id'], item_id))

        # if the quantity ever goes to 0 we delete the entry
        cursor.execute('''
                        DELETE FROM USER_ITEM
                        WHERE UserID = ? AND ItemID = ? AND QuantityOwned <= 0
                    ''', (session['user_id'], item_id))
    conn.commit()
    conn.close()

    # as multiple parts of the home page use this function, we pull the anchor that was used to bring the page back to where
    # it was.
    source = request.form.get('source', '')

    if source:
        return redirect(url_for('home') + f"#{source}")
    # we redirect home as an else in case something was missed in code or something is added in the future
    else:
        return redirect(url_for('home'))

# due to time constraints, a remove from museum was not added meaning once something is donated it cannot be undone in the case
# of an accidental addition. this is hoped to be added soon

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
