
# inventory_manager.py version 2 (main.py test program)

import inventory_manager as im
import os, platform, logging

# --- Setup logger ---
logger = logging.getLogger("InventoryApp")
logger.setLevel(logging.DEBUG)
logger.propagate = True

log_formatter = logging.Formatter(
    '%(asctime)s [%(name)-25s] | [%(levelname)-8s] : %(message)s',
    datefmt='%I:%M:%S'
)

console_log = logging.StreamHandler()
console_log.setLevel(logging.INFO) # INFO, WARNING, ERROR, CRITICAL
console_log.setFormatter(log_formatter)
logger.addHandler(console_log)

file_log = logging.FileHandler("inventory_manager.log", mode='a')
file_log.setLevel(logging.DEBUG) # DEBUG, INFO, WARNING, ERROR, CRITICAL
file_log.setFormatter(log_formatter)
logger.addHandler(file_log)
# --- End logger setup ---

def clear_terminal():
    """Clears the terminal screen"""
    # Windows
    if platform.system() == "Windows":
        os.system('cls')
    # Linux & macOS
    else:
        os.system('clear')
        
def main():    
    print("*** inventory_manager.py Test Program ***\n")

    db_name = input("Please insert inventory database file name: ")
    with im.managed_db_session(db_name) as db_cursor:
        im.create_inv_tables(db_cursor)
        while True:
            try:
                print(f"\n*** Connected to {db_name} database ***\n")
            
                print("1. Add Item")
                print("2. View All Items")
                print("3. Search Item by ID")
                print("4. Update Item")
                print("5. Delete Item")
                print("6. Exit Application\n")
            
                selection = int(input("Please make a selection (1-5): "))
                
                if selection == 1:
                    clear_terminal()
                    while True:
                        try:
                            print("\n*** Add Item to Inventory Database ***\n")
                            
                            name = input("Item Name: ")
                            qty = int(input("Item Quantity: "))
                            price = float(input("Item Price: "))
                            im.add_item(db_cursor, name, qty, price)
                            input("Press enter to continue...")
                            clear_terminal()
                            break
                        except ValueError:
                            logger.error("Please enter a valid input.")
                elif selection == 2:
                    clear_terminal()
                    print("\n*** Viewing Full Inventory ***\n")
                    im.view_inventory(db_cursor)
                    input("Press enter to continue...")
                    clear_terminal()
                elif selection == 3:
                    clear_terminal()
                    print("\n*** Search Item by ID ***\n")
                    im.view_item(db_cursor, int(input("Enter item ID number: ")))
                    input("Press enter to continue...")
                    clear_terminal()
                elif selection == 4:
                    clear_terminal()
                    while True:
                        try:
                            print("\n*** Update Item in Inventory Database ***\n")
                            
                            item_id = int(input("Item ID: "))
                            qty = int(input("Enter new item quantity: "))
                            price = float(input("Enter new item price: "))
                            im.update_inventory(db_cursor, item_id, qty, price)
                            input("Press enter to continue...")
                            clear_terminal()
                            break
                        except ValueError:
                            logger.error("Please enter a valid input.")
                elif selection == 5:
                    clear_terminal()
                    while True:
                        try:
                            print("\n*** Delete Item in Inventory Database ***\n")
                            
                            item_id = int(input("Item ID to Delete: "))
                            im.view_item(db_cursor, item_id)
                            confirm = input("Do you really want to delete this item? (Y/n): ")
                            
                            if confirm.lower() == "y":
                                im.delete_item(db_cursor, item_id)
                                input("Press enter to continue...")
                                clear_terminal()
                                break
                            else:
                                print(f"Deletion of item ID: {item_id} cancelled.")
                                input("Press enter to continue...")
                                clear_terminal()
                                break
                        except ValueError:
                            logger.error("Please enter a valid input.")
                elif selection == 6:
                    clear_terminal()
                    input("\nPress enter to exit...")
                    break
                else:
                    logger.error("Please enter a valid selection.")
            except ValueError:
                logger.error("Please enter a valid input.")
        
if __name__ == "__main__":
    main()
    

