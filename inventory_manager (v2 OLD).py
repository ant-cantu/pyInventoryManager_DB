
# inventory_manager.py version 2

import sqlite3, functools, datetime
from collections import namedtuple
from contextlib import contextmanager

InventoryItem = namedtuple('InventoryItem', "id name quantity price")


def log_db_operation(func):
    @functools.wraps(func)
    def wrapper_function(*args, **kwargs):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S")
        try:
            with open("inventory_manager_log.txt", "a") as f:
                try:
                    f.write(f"{current_time} [LOG]: The function {func.__name__} was called with arguments: {args[1:]}, {kwargs}\n")
                    result = func(*args, **kwargs)
                    f.write(f"{current_time} [LOG]: Successfully executed: {func.__name__}. Result: {result}\n")
                    f.write(f"-" * 40 + "\n")
                    return result
                except Exception as e:
                    f.write(f"{current_time} [LOG]: ERROR during {func.__name__}: {type(e).__name__} - {e}")
                    raise
        except FileNotFoundError as f_e:
            print("[ERROR]: Unable to create log file.")
            raise
    return wrapper_function


@contextmanager
def managed_db_session(_db_name):
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect(_db_name)
        cursor = conn.cursor()
        print(f"Database connection to '{_db_name}' successful...")
        yield cursor
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error connecting to databse {_db_name}: {e}.")
        print("Database rollback commenced.")
        conn.rollback()
        raise
    except Exception as e_ext:
        print(f"Error outside of database was caught: {e_ext}.")
        print("Database rollback commenced.")
        conn.rollback()
        raise
    finally:
        if conn:
            print(f"Database connection to '{_db_name}' closed...")
            conn.close()

"""
^^^ Obsolete after creating custom contextmanager above ^^^
def connect_inv_database(_db_name):
    Establishes and returns a database connection.
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
"""

@log_db_operation
def create_inv_tables(cursor):
    try:
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
        print("Table 'inventory' checked/created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating 'inventory' table: {e}")

@log_db_operation     
def add_item(cursor, name, quantity, price):
    sql = """
        INSERT INTO inventory (name, quantity, price) 
        VALUES (?, ?, ?)
        """
        
    try:
        # Execute sql command with tuple of values for the placeholders
        cursor.execute(sql, (name, quantity, price)) 
        print(f"Item '{name}' added succesfully (ID: {cursor.lastrowid}).")
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error adding item: {e}.")
        return False
    except sqlite3.Error as e:
        print(f"Database error adding bookmark: {e}")
        return False

@log_db_operation    
def view_inventory(cursor):
    sql = """
        SELECT id, name, quantity, price FROM inventory ORDER BY id
        """
    
    try:
        cursor.execute(sql)
        inventory = cursor.fetchall()

        inventory_list = []

        if inventory:
            for item in inventory:
                itme_obj = InventoryItem(*item)
                inventory_list.append(itme_obj)
        
        if inventory_list:
            for item in inventory_list:
                print(f"ID: {item.id}, Name: {item.name}, Qty: {item.quantity}, Price: {item.price}")
            print("--------------------\n")
    except sqlite3.Error as e:
        print(f"Database error viewing inventory: {e}")

@log_db_operation       
def view_item(cursor, item_id):
    sql = "SELECT id, name, quantity, price FROM inventory WHERE inventory.id = ?"
    
    try:
        cursor.execute(sql, (item_id,))
        item = cursor.fetchone()
        
        if item:
            item_obj = InventoryItem(*item)
            print(f"ID: {item_obj.id}, Name: {item_obj.name}, Qty: {item_obj.quantity}, Price: {item_obj.price}")
        else:
            print(f"No item found for item ID: {item_id}")
    except sqlite3.Error as e:
        print(f"Database error fetching item id: {e}")

@log_db_operation        
def update_inventory(cursor, item_id, new_qty, new_price):
    sql = """
        UPDATE inventory SET quantity = ?, price = ? WHERE id = ?
        """
    
    try:
        cursor.execute(sql, (new_qty, new_price, item_id))
        
        if cursor.rowcount > 0:
            print(f"Inventory for item ID {item_id} updated successfully.")
            return True
        else:
            print(f"No inventory item found with ID {item_id}. Nothing updated.")
            return False
    except sqlite3.Error as e:
        print(f"Database error updating inventory: {e}")
        return False

@log_db_operation   
def delete_item(cursor, item_id):
    sql = "DELETE FROM inventory WHERE id = ?"
    
    try:
        cursor.execute(sql, (item_id,))
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
