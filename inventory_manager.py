
# inventory_manager.py version 3

import sqlite3, functools, datetime, logging
from collections import namedtuple
from contextlib import contextmanager

# Get logger
logger = logging.getLogger("InventoryApp.manager")

# namedtiple for handling items in inventory
InventoryItem = namedtuple('InventoryItem', "id name quantity price")

def log_db_operation(func):
    @functools.wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            print("called")
            logger.debug(f"Calling function %s with arguments: %s, %s", func.__name__, args, kwargs)
            result = func(*args, **kwargs)
            logger.debug(f"Successfully executed: %s. Result {result}", func.__name__)
            logger.debug(f"-" * 40 + "")
            return result
        except Exception as e:
            logger.error(f"ERROR during %s: %s", func.__name__, e, exc_info=True)
            raise
    return wrapper_function


@contextmanager
def managed_db_session(db_name):
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        logger.debug(f"Database connection to '%s' successful...", db_name)
        yield cursor
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error connecting to databse %s: %s.", db_name, e, exc_info=True)
        logger.error("Database rollback commenced.")
        conn.rollback()
        raise
    except Exception as e_ext:
        logger.error(f"Error outside of database was caught: %s.", e_ext, exc_info=True)
        logger.error("Database rollback commenced.")
        conn.rollback()
        raise
    finally:
        if conn:
            logger.debug(f"Database connection to '%s' closed...", db_name)
            conn.close()

"""
^^^ Obsolete after creating custom contextmanager above ^^^
def connect_inv_database(db_name):
    Establishes and returns a database connection.
    conn = None # Initialize conn to None
    try:
        conn = sqlite3.connect(db_name)
        print(f"Succesfully connected to database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database {db_name}: {e}")
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
        logger.info("Table 'inventory' checked/created successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error creating 'inventory' table: %s", e, exc_info=True)
        raise

@log_db_operation     
def add_item(cursor, name, quantity, price):
    sql = """
        INSERT INTO inventory (name, quantity, price) 
        VALUES (?, ?, ?)
        """
        
    try:
        # Execute sql command with tuple of values for the placeholders
        cursor.execute(sql, (name, quantity, price)) 
        logger.info(f"Item '%s' added successfully (ID: %s).", name, cursor.lastrowid)
        return True
    except sqlite3.IntegrityError as e:
        logger.error(f"Error adding item: %s | %s", name, e, exc_info=True)
        return False
    except sqlite3.Error as e:
        logger.error(f"Database error adding bookmark: %s", e, exc_info=True)
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
                logger.info(f"ID: %s | Name: %-8s | Qty: %-3s | Price: %-5s", item.id, item.name, item.quantity, item.price)
            logger.info("--------------------\n")
    except sqlite3.Error as e:
        logger.error(f"Database error viewing inventory: %s", e, exc_info=True)
        raise

@log_db_operation       
def view_item(cursor, item_id):
    sql = "SELECT id, name, quantity, price FROM inventory WHERE inventory.id = ?"
    
    try:
        cursor.execute(sql, (item_id,))
        item = cursor.fetchone()
        
        if item:
            item_obj = InventoryItem(*item)
            logger.info(f"ID: %s | Name: %-8s | Qty: %-3s | Price: %-5s", item_obj.id, item_obj.name, item_obj.quantity, item_obj.price)
        else:
            logger.warning(f"No item found for item ID: %s", item_id)
    except sqlite3.Error as e:
        logger.error(f"Database error fetching item id: %s | %s", item_id, e, exc_info=True)
        raise

@log_db_operation        
def update_inventory(cursor, item_id, new_qty, new_price):
    sql = """
        UPDATE inventory SET quantity = ?, price = ? WHERE id = ?
        """
    
    try:
        cursor.execute(sql, (new_qty, new_price, item_id))
        
        if cursor.rowcount > 0:
            logger.info(f"Inventory for item ID %s updated successfully.", item_id)
            return True
        else:
            logger.warning(f"No inventory item found with ID %s. Nothing performed.", item_id)
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error updating inventory: %s", e, exc_info=True)
        return False

@log_db_operation   
def delete_item(cursor, item_id):
    sql = "DELETE FROM inventory WHERE id = ?"
    
    try:
        cursor.execute(sql, (item_id,))
        if cursor.rowcount > 0:
            logger.info(f"Item ID: %s, successfully deleted.", item_id)
            return True
        else:
            logger.warning(f"Item ID: %s was not found. Nothing performed.", item_id)
            return False
    except sqlite3.Error as e:
        logger.error(f"Database error deleting item from inventory: %s", e, exc_info=True)
        raise

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