
import sqlite3
from venv import create

# _db_name = "inventory.db" # The database file name

def connect_inv_database(_db_name):
    """Establishes and returns a database connection."""
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect(_db_name)
        print(f"Succesfully connected to database: {_db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database {_db_name}: {e}")
        if conn:
            conn.close() # Close connection if error occured
        return None
    
def create_inv_tables(connection):
    if connection is None:
        return # Cannot proceed without a connection
    
    try:
        cursor = connection.cursor()
        # SQL command to create a table (inventory table)
        # IF NOT EXISTS ensures it doesn't error if table already exists
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                price REAL NOT NULL DEFAULT 0.0
           )            
        """)
        connection.commit() # Save the changes (table creation)
        print("Table 'inventory' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating 'inventory' table: {e}")
        
def add_item(connection, name, quantity, price):
    if connection is None:
        return # Cannot proceed without a connection
    
    sql = """
        INSERT INTO inventory (name, quantity, price) 
        VALUES (?, ?, ?)
        """
        
    try:
        cursor = connection.cursor() # Create cursor object of db
        # Execute sql command with tuple of values for the placeholders
        cursor.execute(sql, (name, quantity, price)) 
        connection.commit() # Save the new row
        print(f"Item '{name}' added succesfully (ID: {cursor.lastrowid}).")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error adding item: {e}.")
        return False
    except sqlite3.Error as e:
        print(f"Database error adding bookmark: {e}")
        return False
    
def view_inventory(connection):
    if connection is None:
        return # Cannot proceed without a connection
    
    sql = """
        SELECT id, name, quantity, price FROM inventory ORDER BY id
        """
    
    try:
        cursor = connection.cursor() 
        cursor.execute(sql)
        inventory = cursor.fetchall()
        
        if inventory:
            for item in inventory:
                print(f"ID: {item[0]}, Name: {item[1]}, Qty: {item[2]}, Price: {item[3]}")
            print("--------------------\n")
    except sqlite3.Error as e:
        print(f"Database error viewing inventory: {e}")
        
def view_item(connection, item_id):
    if connection is None:
        return
    
    sql = "SELECT id, name, quantity, price FROM inventory WHERE inventory.id = ?"
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (item_id,))
        item = cursor.fetchone()
        
        if item:
            print(f"ID: {item[0]}, Name: {item[1]}, Qty: {item[2]}, Price: {item[3]}")
        else:
            print(f"No item found for item ID: {item_id}")
    except sqlite3.Error as e:
        print(f"Database error fetching item id: {e}")

        
def update_inventory(connection, item_id, new_qty, new_price):
    if connection is None:
        return # Cannot proceed without a connection
    
    sql = """
        UPDATE inventory SET quantity = ?, price = ? WHERE id = ?
        """
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (new_qty, new_price, item_id))
        connection.commit() # Save updates
        
        if cursor.rowcount > 0:
            print(f"Inventory for item ID {item_id} updated successfully.")
            return True
        else:
            print(f"No inventory item found with ID {item_id}. Nothing updated.")
            return False
    except sqlite3.Error as e:
        print(f"Database error updating inventory: {e}")
        return False
    
def delete_item(connection, item_id):
    if connection is None:
        return
    
    sql = "DELETE FROM inventory WHERE id = ?"
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, (item_id,))
        connection.commit() # Save changes
        
        if cursor.rowcount > 0:
            print(f"Item ID: {item_id}, successfully deleted.")
            return True
        else:
            print(f"Item ID: {item_id} was not found. Nothing updated.")
            return False
    except sqlite3.Error as e:
        print(f"Database error deleting item from inventory: {e}")

"""       
if __name__ == "__main__":
    db_conn = connect_inv_database("inventory.db")
    if db_conn:
        create_inv_tables(db_conn)
        add_item(db_conn, "Remote", 5, 10.99)
        update_inventory(db_conn, 2, 100, 19.99)
        delete_item(db_conn, 2)
        view_inventory(db_conn)
        db_conn.close()
"""
