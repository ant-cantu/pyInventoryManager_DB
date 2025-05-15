
from multiprocessing import Value
import inventory_manager as im
import os, platform, string

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
    db_conn = im.connect_inv_database(db_name)
    im.create_inv_tables(db_conn)
    if db_conn:
        while True:
            try:
                print(f"\n*** Connected to {db_name} database ***\n")
            
                print("1. Add Item")
                print("2. View All Items")
                print("3. Update Item")
                print("4. Delete Item")
                print("5. Exit Application\n")
            
                selection = int(input("Please make a selection (1-5): "))
                
                if selection == 1:
                    while True:
                        try:
                            print("\n*** Add Item to Inventory Database ***\n")
                            
                            name = input("Item Name: ")
                            qty = int(input("Item Quantity: "))
                            price = float(input("Item Price: "))
                            im.add_item(db_conn, name, qty, price)
                            input("Press enter to continue...")
                            break
                        except ValueError:
                            print("ERROR: Please enter a valid input.")
                elif selection == 2:
                    print("\n*** Viewing Full Inventory ***\n")
                    im.view_inventory(db_conn)
                    input("Press enter to continue...")
                elif selection == 3:
                    while True:
                        try:
                            print("\n*** Update Item in Inventory Database ***\n")
                            
                            item_id = int(input("Item ID: "))
                            qty = int(input("Enter new item quantity: "))
                            price = float(input("Enter new item price: "))
                            im.update_inventory(db_conn, item_id, qty, price)
                            input("Press enter to continue...")
                            break
                        except ValueError:
                            print("ERROR: Please enter a valid input.")
                elif selection == 4:
                    while True:
                        try:
                            print("\n*** Delete Item in Inventory Database ***\n")
                            
                            item_id = int(input("Item ID to Delete: "))
                            im.view_item(db_conn, item_id)
                            confirm = input("Do you really want to delete this item? (Y/n): ")
                            
                            if confirm.lower() == "y":
                                im.delete_item(db_conn, item_id)
                                input("Press enter to continue...")
                                break
                            else:
                                print(f"Deletion of item ID: {item_id} cancelled.")
                                input("Press enter to continue...")
                                break
                        except ValueError:
                            print("ERROR: Please enter a valid input.")
                elif selection == 5:
                    input("\nPress enter to exit...")
                    db_conn.close()
                    break
                else:
                    print("ERROR: Please enter a valid selection.")
            except ValueError:
                print("ERROR: Please enter a valid input.")
        
    
if __name__ == "__main__":
    main()
    

