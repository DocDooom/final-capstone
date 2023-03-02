# HyperionDev Task 48 - Bookstore Manager - Capstone V
# Overview: We load or create a database of books (depending on whether the db table exists)
# We can then carry out various operations on the books' database such as adding to it, updating etc
# We do this discreetly closing the connection to the db between. So things are safely committed

# Note: I've omitted Docstring documentation comments (for use with the help() function)
# This is to reduce bloat. General comments about functionality are included as usual

# ---- IMPORTS ----
import sqlite3
from dataclasses import dataclass
from typing import Union
from tabulate import tabulate
import re


# ---- CLASSES ----
# We'll create an intermediary class to load books into and from when needed
@dataclass
class Book:
    id: int
    title: str
    author: str
    quantity: int

    def return_tuple(self) -> tuple:
        return self.id, self.title, self.author, self.quantity

    def __str__(self) -> str:
        return "ID: " + str(self.id) + " Title: " \
               + self.title + " Author: " + self.author + " Quantity: " + str(self.quantity)


# ---- UTILITY FUNCTIONS ----
# This is the utility function we'll call everytime we want to exit from
# a function back to the main menu
def return_to_menu(check_var: str) -> Union[None, int]:
    if check_var == "q" or check_var == "-1":
        print("Returning to Main Menu...")
        return None
    else:
        return 1


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


# ---- DB FUNCTIONS ----
# Create db if none/no table exists
def initialize_db(path: str) -> bool:
    db = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        list_of_tables = cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='books';
            """
        ).fetchall()

        if len(list_of_tables) < 1:
            cursor.execute("""
            CREATE TABLE books
            (id INTEGER PRIMARY KEY, title TEXT, author_name TEXT, qty INTEGER)""")

            books_list = [
                Book(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                Book(3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                Book(3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                Book(3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                Book(3005, "Alice in Wonderland", "Lewis Carroll", 12)
            ]

            # Insert into table
            cursor.executemany("""
            INSERT INTO books(
            id,
            title,
            author_name,
            qty
            )
            VALUES(?,?,?,?) 
            ON CONFLICT DO NOTHING;
            """, [book.return_tuple() for book in books_list])

            db.commit()
            print("\033[1m\033[92mTable Created ✔\033[00m")

        success = True

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
        success = False
    except sqlite3.DatabaseError as db_error:
        print(f"A problem has occured with the database: {db_error}")
        success = False
    finally:
        if db:
            db.close()

    return success


# Get the ID for the next book entry
def next_id(path: str) -> Union[int, None]:
    db = None
    new_id = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        # We automatically generate an ID based on the max id in the db
        cursor.execute("SELECT MAX(id) FROM books")
        prev_highest_id = cursor.fetchone()[0]
        new_id = int(prev_highest_id) + 1

        return new_id

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DataError as d_error:
        print(f"An error occurred accessing the database: {d_error}")
    finally:
        if db:
            db.commit()
            db.close()

    if new_id is not None:
        return new_id
    else:
        return None


# Get the lowest number ID - so we know the low range
def min_id(path: str) -> Union[int, None]:
    # initializing db var
    db = None
    lowest_id = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        cursor.execute("SELECT MIN(id) FROM books")
        lowest_id = cursor.fetchone()[0]

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DataError as d_error:
        print(f"An error occurred accessing the database: {d_error}")
    finally:
        if db:
            db.commit()
            db.close()

    if lowest_id is not None:
        return int(lowest_id)
    else:
        return None


# Get the highest number ID - so we know the high range
def max_id(path: str) -> Union[int, None]:
    # initializing db var
    db = None
    largest_id = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        cursor.execute("SELECT MAX(id) FROM books")
        largest_id = cursor.fetchone()[0]

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DataError as d_error:
        print(f"An error occurred accessing the database: {d_error}")
    finally:
        if db:
            db.commit()
            db.close()

    if largest_id is not None:
        return int(largest_id)
    else:
        return None


# Input validation for ID matching
def pattern_match_id(path: str, message=": "):
    lowest_id = min_id(path)
    highest_id = max_id(path)

    while True:
        select_by_id = input(message)
        if return_to_menu(select_by_id) is None:
            return None

        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(select_by_id)

        if match is None:
            print("Invalid input, please input the ID of the book you'd like to delete...")
            continue
        else:
            select_by_id = int(select_by_id)
            if select_by_id < lowest_id or select_by_id > highest_id:
                print("The selection is out of range... Please try again")
                continue
            else:
                break

    return select_by_id


# Input validation for Quantity entries
def pattern_match_quantity() -> [int, None]:
    while True:
        quantity = input("Enter quantity (q or -1 to return to main menu): ")
        if return_to_menu(quantity) is None:
            return None

        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(quantity)

        if match is None:
            print("Quantity is not in a valid format... Please try again.")
            continue
        else:
            quantity = int(quantity)
            break

    return quantity


# ---- GLOBAL FUNCTIONS ----
# This function is called when we add books - it handles user input
# as well as calling next_id to automatically generate the id for the entry
def input_book(path: str) -> Union[Book, None]:
    # We automatically generate an ID based on the max id in the db
    book_id = next_id(path)

    str_pattern = r'^[a-zA-Z0-9 ]{2,}$'

    # Get book info
    while True:
        title = input("Enter the book title (q or -1 to return to main menu): ")
        if return_to_menu(title) is None:
            return None

        match = re.search(str_pattern, title)

        if match is None:
            print("The input needs to have at least 2 characters... Please try again")
            continue
        else:
            break

    while True:
        author = input("Enter the author name (q or -1 to return to main menu): ")
        if return_to_menu(author) is None:
            return None

        match = re.search(str_pattern, author)

        if match is None:
            print("The input needs to have at least 2 characters... Please try again")
            continue
        else:
            break

    while True:
        quantity = input("Enter quantity (q or -1 to return to main menu): ")
        if return_to_menu(quantity) is None:
            return None

        # Validate input is a digit between 0 - 9999
        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(quantity)

        if match is None:
            print("Quantity is not in a valid format... Please try again.")
            continue
        else:
            quantity = int(quantity)
            break

    return Book(book_id, title, author, quantity)


# Here we'll call input_book() which returns a Book object
# then add that object to the books
def add_book(path: str) -> Union[int, None]:
    new_book = input_book(path)

    # Exit back to main menu if we return None from new_book
    if new_book is None:
        return None

    db = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        cursor.execute(
            """
            INSERT INTO books(
            id,
            title,
            author_name,
            qty
            )
            VALUES(?,?,?,?);
            """,
            (new_book.id, new_book.title, new_book.author, new_book.quantity)
        )

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DatabaseError as e:
        db.rollback()
        print("Something's gone wrong with the database... Changes have been rolled back")
        print(e)
        return None
    finally:
        if db:
            db.commit()
            db.close()

    print("\033[1m" + "———— Book Added to DB ————" + "\033[0m")
    print(new_book)
    return 1


# We'll first display the book list to the user, to allow them to make a selection of the book
# they'd like to update. After selecting by ID we let the user enter new data for each field
def update_book(path: str):
    print("\033[1m" + "———— Update A Book ————" + "\033[0m")
    view_all(path)

    select_id = pattern_match_id(path, "select ID (q or -1 to return to Main Menu): ")
    if select_id is None:
        return None

    db = None

    # Get and print the book to be updated from the db
    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        selected_book = cursor.execute("""
        SELECT * FROM books
        Where id = ?;
        """, (select_id,)).fetchone()

        if selected_book is None:
            print("There is no book with that ID... Returning to Main Menu")
            return None

        print(tabulate([selected_book], headers=["ID", "Title", "Author", "Quantity"], tablefmt="fancy_grid"))

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DatabaseError:
        print("There was an error connecting to the database... Nothing has been updated")
    finally:
        if db:
            db.close()

    str_pattern = r'^[a-zA-Z0-9 ]{2,}$'

    # Get changes from user
    while True:
        new_title = input("Please enter a new title for the book (q or -1 to exit): ")
        if return_to_menu(new_title) is None:
            return None

        match = re.search(str_pattern, new_title)

        if match is None:
            print("The input needs to have at least 2 characters... Please try again")
            continue
        else:
            break

    while True:
        new_author = input("Please enter a new author for the book (q or -1 to exit): ")
        if return_to_menu(new_author) is None:
            return None

        match = re.search(str_pattern, new_author)

        if match is None:
            print("The input needs to have at least 2 characters... Please try again")
            continue
        else:
            break

    new_quantity = pattern_match_quantity()

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        cursor.execute("""
        UPDATE books 
        SET title = ?, author_name = ?, qty = ? 
        WHERE id = ?;
        """, (new_title, new_author, str(new_quantity), select_id))
    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DatabaseError:
        print("There was an error connecting to the database... Nothing has been updated")
    finally:
        if db:
            db.commit()
            db.close()


# We can select the ID of the book we'd like to delete. We display the book list to the user
# allowing them to make the selection
def delete_book(path: str):
    print("\033[1m" + "———— Delete A Book ————" + "\033[0m")
    view_all(path)

    print("Which book would you like to delete? Please select by ID (q or -1 to return to main menu)", end="")

    lowest_id = min_id(path)
    highest_id = max_id(path)

    # Validate input
    while True:
        select_by_id = input(": ")
        if return_to_menu(select_by_id) is None:
            return None

        pattern = re.compile(r"^\d{1,4}$")
        match = pattern.search(select_by_id)

        if match is None:
            print("Invalid input, please input the ID of the book you'd like to delete...")
            continue
        else:
            select_by_id = int(select_by_id)
            if select_by_id < lowest_id or select_by_id > highest_id:
                print("The selection is out of range... Please try again")
                continue
            else:
                break

    db = None
    selected_book = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        # return object for selected row
        selected_row = cursor.execute(
            """
            SELECT * FROM books WHERE id = ?;
            """, (select_by_id,)
        ).fetchone()

        if selected_row is None:
            print("No book found using that ID... Returning to Main Menu")
            return None

        selected_book = Book(selected_row[0], selected_row[1],
                             selected_row[2], selected_row[3])

        cursor.execute(
            """
            DELETE FROM books
            WHERE id = ?;
            """,
            (select_by_id,)
        )
    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DatabaseError as e:
        db.rollback()
        print("Something's gone wrong with the database... Changes have been rolled back")
        print(e)
        return None
    finally:
        if db:
            db.commit()
            db.close()

    if selected_book is not None:
        print(f"---- {selected_book.title} had been deleted ----")
        print(selected_book)


# Fuzzy search, so we don't have to enter exact strings to get results
# Can search against various types of data: id, title, author
def search_books(path: str) -> Union[int, None]:
    print("\033[1m" + "———— Search for a Book ————" + "\033[0m")

    selection_dict = {
        "i": 'id',
        "t": 'title',
        "a": 'author_name',
        "q": None,
        "-1": None
    }

    while True:
        selection = input(
            """What would you like to search by? Please input the following:
i - id
t - title
a - author name
(type q or -1 to return to main menu)
: """)
        if selection in selection_dict:
            if selection_dict[selection] is not None:
                break
            else:
                print("Returning to Main Menu...")
                return None
        else:
            print("You've made an incorrect selection... Please try again")
            continue

    search = input("Please enter the item you'd like to search for: ").strip()
    if return_to_menu(search) is None:
        return None

    db = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        query = f"SELECT * FROM books WHERE {selection_dict[selection]} LIKE '%{search}%'"
        search_result = cursor.execute(query).fetchall()

        if len(search_result) > 0:
            for s in search_result:
                print(tabulate([s], headers=["ID", "Title", "Author", "Quantity"], tablefmt="fancy_grid"))
            return 1
        else:
            print("\033[91m\033[1mSorry your search returned no matches...\033[00m")
            print("\033[91m\033[1mReturning to Main Menu...\033[00m")
            return None

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database {o_error} has occurred")
    except sqlite3.DataError as d_error:
        print(f"An error occurred accessing the database: {d_error}")
    finally:
        if db:
            db.commit()
            db.close()


# Get all from book table and display tabulated
def view_all(path: str):
    db = None

    try:
        db = sqlite3.connect(path)
        cursor = db.cursor()

        book_list = cursor.execute("""
        SELECT * FROM books;
        """)
        print(tabulate(book_list, headers=["ID", "Title", "Author", "Quantity"], tablefmt="fancy_grid"))

    except sqlite3.OperationalError as o_error:
        print(f"There is a problem with the database '{o_error}' has occurred")
    except sqlite3.DataError as d_error:
        print(f"An error occurred accessing the database: {d_error}")
    finally:
        if db:
            db.close()


# Styling
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
ESCAPE = "\033[00m"
CYAN = "\033[96m"
PURPLE = "\033[35m"
BOLD = "\033[1m"

# ---- MAIN ----
if __name__ == "__main__":
    # Header
    print(BLUE + BOLD + "╔═════════════════════════════════════════════╗" + ESCAPE)
    print(PURPLE + BOLD + "               BOOKSTORE MANAGER           " + ESCAPE)
    print(BLUE + BOLD + "╚═════════════════════════════════════════════╝" + ESCAPE)

    # Check DB
    db_path = "ebookstore.db"

    initialize_success = initialize_db(db_path)

    if not initialize_success:
        print("There's been a problem with the database please check your working directory and try again...")
        print("You may not have permission to write the file")
        exit()
    else:
        print("\033[1m\033[92mDB OK ✔\033[00m")

    # Present Main Menu
    while True:
        menu_selection = input(YELLOW +
                               """———— MAIN MENU ————
v - View all
a - Add a book
d - Delete a book
u - Update a book
s - Search book
e - Exit
: """ + ESCAPE).lower()

        match menu_selection:
            case "v":
                view_all(db_path)
            case "a":
                add_book(db_path)
            case "d":
                delete_book(db_path)
            case "s":
                search_books(db_path)
            case "u":
                update_book(db_path)
            case "e":
                print(YELLOW + BOLD + "Bye, Bye from me on T48! Thanks for all the reviews!!!" + ESCAPE)
                print(CYAN + BOLD + "All the best" + ESCAPE)
                print(CYAN + BOLD + "McZane" + ESCAPE)
                exit()
            case _:
                print("You've made an incorrect selection... Please try again")
