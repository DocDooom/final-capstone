# HyperionDev Task 32 - OOP - Capstone IV
# Overview: Inventory Management System for Nike store - We load inventory from a text/csv file
# carrying out operation and save back to that file

# Note: I'm omitting the use of docstring documentation comments for functions, hopefully this will reduce
# bloat. Comments about the functionality and thought process are still present as usual.

# Note: Using Pandas can add some processing time please allow for a little extra time when loading

# Module imports
from dataclasses import dataclass
from typing import Union
from tabulate import tabulate
import pandas as pd
import os
import re


# ========The beginning of the class==========
# It's more efficient to mark the class as a dataclass it implements __init__ for us
@dataclass
class Shoe:
    country: str
    prod_code: str
    product: str
    cost: float
    quantity: int

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def update_cost(self, new_cost):
        self.cost = new_cost

    def __str__(self):
        return "Country: " + self.country + " Product Code: " + self.prod_code + " Product: " + self.product + \
               " Cost: " + str(self.cost) + " Quantity: " + str(self.quantity)


# ==========Functions outside the class==============

# ------------- Utility Functions ----------------
# Function to check for whether an input str can be converted to float or int
def check_number(string_input: str, check_type="int") -> Union[int, float, None]:
    try:
        match check_type:
            case "int":
                num = int(string_input)
                return num
            case "float":
                num = float(string_input)
                return num
    except ValueError:
        print("The input cannot be converted to a number!")
        return None


# This is the utility function we'll call everytime we want to exit from
# a function back to the main menu
def return_to_menu(check_var: str) -> Union[None, int]:
    if check_var == "q" or check_var == "-1":
        print("Returning to Main Menu...")
        return None
    else:
        return 1


# This is our function to write the changes back to the file
def write_file(s_list: list[Shoe], path: str, mode="w"):
    try:
        with open(path, mode, encoding="utf-8") as shoes_file:
            shoes_file.write("Country,Code,Product,Cost,Quantity\n")
            for s in s_list:
                shoes_file.write(f"{s.country},{s.prod_code},{s.product},{s.cost},{s.quantity}\n")

        print("The file has been written...")
        return

    except PermissionError:
        print("You do not have permission to access the file... Is the file open? Please"
              "close it and try again")
        return
    except IOError:
        print("There was an error reading/writing the file")
        return
    # General exceptions might not be the best but in the case of writing files a lot can happen
    # so this final exception is a general catchall to keep the program running if something unexpected happens
    except Exception:
        print("There's been a problem... please check your system and try again")
        return


# ------------- Global Functions ----------------
# Read in the file we can use pandas for it's CSV features and convert that into
# a list of Shoe objects
# Note: Pandas can increase loading times
def read_shoes_data(filename: str) -> Union[list[Shoe], None]:
    if os.path.exists(filename):
        shoe_dat = pd.read_csv(filename)

        # Check shoe_dat shape
        # this is so we can see if there are issues with the data
        shoe_dat_before = shoe_dat.shape[0]
        shoe_dat = shoe_dat.dropna()
        shoe_dat_after = shoe_dat.shape[0]

        if shoe_dat_before != shoe_dat_after:
            print("\033[1m\033[91m ---- Warning ---- \033[00m")
            print("\033[1m\033[91m Some issues in the data were found preventing proper loading, please check "
                  "the data. The rows without errors have been loaded... \033[00m")
        else:
            print("\033[1m\033[92mInventory data OK ✔\033[00m")

        return [Shoe(row["Country"], row["Code"], row["Product"], row["Cost"], row["Quantity"])
                for _, row in shoe_dat.iterrows()]
    else:
        print("\033[1m\033[91m ---- ERROR ---- \033[00m")
        print("\033[1m\033[91mThe inventory data does not appear to be in the correct place,"
              " please check and try again...\033[00m")
        return None


# Capture shoes prompts user for new shoe will not allow the same product code to be entered as an existing
# shoe this must be unique
def capture_shoes(s_list: list[Shoe]):
    """
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    """
    while True:
        country = input("Enter the country (q or -1 to return to main menu): ")
        if return_to_menu(country) is None:
            return

        if len(country) < 3:
            print("The Country input is too short please try again")
            continue
        else:
            break

    while True:
        code = input("Enter the product code (q or -1 to return to main menu): ").upper()
        if return_to_menu(code.lower()) is None:
            return

        if len(code) < 3:
            print("The product code is too short. This needs to be a unique id please try again")
            continue

        for s in s_list:
            if getattr(s, "prod_code") == code:
                print("\033[91m\033[1mA shoe with that same Product Code already exists... Please try again\033[00m")
                code = None
                break

        if code is None:
            continue
        else:
            break

    while True:
        product = input("Enter the product name (q or -1 to return to main menu): ")
        if return_to_menu(product) is None:
            return

        if len(product) < 1:
            print("Product name cannot be empty please try again...")
            continue
        else:
            break

    while True:
        cost = input("Enter the cost as a float e.g. 1200.00 (q or -1 to return to main menu): ")
        if return_to_menu(cost) is None:
            return None

        pattern = re.compile(r"^\d+.{1,4}$")
        match = pattern.search(cost)

        if match is None:
            print("Cost is not in a valid format... Please try again.")
            continue

        cost = check_number(cost, "float")
        if cost is None:
            continue
        else:
            break

    while True:
        quantity = input("Enter the quantity (q or -1 to return to main menu): ")
        if return_to_menu(quantity) is None:
            return

        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(quantity)

        if match is None:
            print("Quantity is not in a valid format... Please try again.")
            continue

        quantity = check_number(quantity, "int")
        if quantity is None:
            continue
        else:
            break

    # Create, Shoe object, update list, write file
    new_shoe = Shoe(country, code, product, cost, quantity)

    s_list.append(new_shoe)

    write_file(s_list, "inventory.txt")

    print("\033[1m" + "———— Shoe Details Added ————" + "\033[0m")
    print(tabulate([new_shoe],
                   headers=["Country", "Product Code", " Product", "Cost", "Quantity"], tablefmt="fancy_grid"))


# Tabulated overview of data in memory
def view_all(s_list: list) -> None:
    """
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    """
    print(tabulate(s_list, headers=["Country", "Product Code",
                                    "Product", "Cost", "Quantity"], tablefmt="fancy_grid"))


def re_stock(s_list: list[Shoe]):
    """
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    """
    min_shoe_quantity = min(s_list, key=lambda x: x.quantity)
    min_quantity_index = s_list.index(min_shoe_quantity)

    print("The Shoe with the lowest stock is: ")
    print(tabulate([min_shoe_quantity],
                   headers=["Country", "Product Code", " Product", "Cost", "Quantity"], tablefmt="fancy_grid"))

    while True:
        quantity = input("Enter the new quantity (q or -1 to return to main menu): ")
        if return_to_menu(quantity) is None:
            return

        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(quantity)

        if match is None:
            print("Quantity is not in a valid format... Please try again")
            continue

        if quantity == "q" or int(quantity) == -1:
            break

        quantity = check_number(quantity, "int")
        if quantity is None:
            continue
        else:
            break

    min_shoe_quantity.update_quantity(quantity)

    s_list[min_quantity_index] = min_shoe_quantity

    write_file(s_list, "inventory.txt")
    print("\033[93m\033[1m ———— The Shoe has been updated ———— \033[00m")
    print(min_shoe_quantity)


# Search function works with list of Shoe we search by SKU
def search_shoe(s_list: list[Shoe]):
    """
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    """
    print("\033[1m" + "———— Search by SKU ————" + "\033[0m")
    search_for = input("What is the product code of the shoe you're looking for?: ").upper()

    # If the user does or does not include SKU as a prefix we can still find the
    # intended shoe
    is_sku_included = search_for.find("SKU")
    if is_sku_included == -1:
        search_for = "SKU" + search_for

    shoe_found = None

    # Find by attribute
    for s in s_list:
        if getattr(s, "prod_code") == search_for:
            print("———— Shoe Found ————")
            shoe_found = 1
            print(tabulate([s],
                           headers=["Country", "Product Code", " Product", "Cost", "Quantity"], tablefmt="fancy_grid"))

    # No match prompt user
    if shoe_found is None:
        print("There is no shoe with that SKU...")


# We'll print only a few identifying columns of data plus the value calculation
def value_per_item(s_list: list[Shoe]):
    """
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    """
    # We'll display the value as follows Table: Product, Code, Total Value
    value_list = []

    for shoe in s_list:
        item_val = [shoe.product, shoe.prod_code, shoe.cost * float(shoe.quantity)]
        value_list.append(item_val)

    print(tabulate(value_list,
                   headers=["Code", "Product", "Total Stock Value (R)"], tablefmt="fancy_grid"))


def highest_qty(s_list: list[Shoe]):
    """
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    """
    # let use enter the percentage off they'd like to give the sale
    max_shoe_quantity = max(s_list, key=lambda x: x.quantity)
    min_quantity_index = s_list.index(max_shoe_quantity)

    print("\033[93m\033[1m ———— Highest Quantity ———— \033[00m")
    print(tabulate([max_shoe_quantity],
                   headers=["Country", "Product Code", " Product", "Cost", "Quantity"], tablefmt="fancy_grid"))

    while True:
        discount = input("Enter the percentage discount as a number with no % sign (q or -1 to return to main menu): ")
        if return_to_menu(discount) is None:
            return

        pattern = re.compile(r"^\d{1,2}$")
        match = pattern.search(discount)

        if match is None:
            print("Discount is not in a valid format... Please try again.")
            continue

        if discount == "q" or int(discount) == -1:
            break

        discount = check_number(discount, "float")
        if discount is None:
            continue
        else:
            break

    max_shoe_quantity.update_cost(max_shoe_quantity.cost - ((discount / 100) * max_shoe_quantity.cost))

    s_list[min_quantity_index] = max_shoe_quantity

    write_file(s_list, "inventory.txt")
    print("\033[93m\033[1m ———— The Shoe is now on Sale ———— \033[00m")
    print(f"{max_shoe_quantity.product} is on sale with a {discount}% discount")
    print(tabulate([max_shoe_quantity],
                   headers=["Country", "Product Code", " Product", "Cost", "Quantity"], tablefmt="fancy_grid"))


# ---- Global Vars ----
# Styling
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
ESCAPE = "\033[00m"
CYAN = "\033[96m"
PURPLE = "\033[35m"
BOLD = "\033[1m"

# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
if __name__ == "__main__":
    print(BLUE + BOLD + "╔═════════════════════════════════════════════╗" + ESCAPE)
    print(RED + BOLD + "               INVENTORY MANAGER           " + ESCAPE)
    print(BLUE + BOLD + "╚═════════════════════════════════════════════╝" + ESCAPE)

    # Attempt to load inventory data
    shoe_list = read_shoes_data("inventory.txt")

    # if data does not exist warn user and exit the program
    # We can't continue without the data
    if shoe_list is None:
        exit()

    # Menu Options
    while True:
        print(YELLOW + BOLD + "---- MENU ----" + ESCAPE, end="")
        menu_selection = input("""
v - View all inventory
s - Search for shoe by SKU
a - Add new item to inventory
r - Restock low items
h - Put high stock items on sale
t - View the total value of the current inventory
e - Exit
: """).lower()

        # Selection matching
        match menu_selection:
            case "v":
                view_all(shoe_list)
                print()
            case "s":
                search_shoe(shoe_list)
            case "a":
                capture_shoes(shoe_list)
            case "r":
                re_stock(shoe_list)
            case "h":
                highest_qty(shoe_list)
            case "t":
                value_per_item(shoe_list)
            case "e":
                print("Good bye!")
                exit()
            case _:
                print("You've made an incorrect selection... Please try again")
                print()
