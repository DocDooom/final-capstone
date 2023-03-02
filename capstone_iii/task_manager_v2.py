# Overview: A task manager with login, allowing users to view, add tasks. Administrators have extra privileges
# such as adding/registering new users and viewing stats associated with the user base
# IMPORTANT! Please note I'll be omitting docstring documentation for functions as the code is already very long
# comments about code functionality will still be included as usual

# ===== importing libraries ===========
'''This is the section where you will import libraries'''
# We'll need the current date when assigning tasks
from dataclasses import dataclass
# We need some functions from typing Typevar to create our placeholder types and Union
# to indicate we can return multiple types
from typing import TypeVar, Union
# We need this to compare dates, convert to date etc
from datetime import date, datetime
# We'll need to wrap the text when printing out tasks to the user
import textwrap
# We're importing os primarily to check for file existence
import os

# Here we're creating a type variable T bound to "User" that we'll use as a place-holder to
# indicate the User as a type
T = TypeVar("T", bound="User")


# -------- Classes --------
# Note: The user class right now is not completely necessary especially if we are using a txt file and are not
# using something like Pickle to serialize the data. However, I plan to expand this later.
# So for now we'll use the class in some minimal way
# The @dataclass decorator implements __init__ among other methods automatically for us
@dataclass
class User:
    user_name: str
    is_admin = False

    def set_admin(self) -> None:
        self.is_admin = True

    def revoke_admin(self) -> None:
        self.is_admin = False

    # Static Methods
    # We're can use this to check whether any user object is an admin
    @staticmethod
    def check_admin(user: T) -> bool:
        return user.is_admin

    # Dunder overrides
    # using str and print for example returns the string below
    def __str__(self):
        return "username: " + self.user_name + ", admin status: " + str(self.is_admin)


# We're defining a Tasks class to load each task from tasks.txt to a Task object
@dataclass
class Task:
    assigned_to: str
    task: str
    task_description: str
    date_assigned: str
    due_date: str
    complete: str

    def get_due_date(self) -> Union[datetime, None]:
        try:
            return datetime.strptime(self.due_date, "%d %b %Y")
        except ValueError:
            return None

    # ---- Dunder overrides ----
    # we can override the dunder str method to return our specified str output
    # when called
    def __str__(self) -> str:
        return f"—————————————————————————————————————————————————————————————————————\n" \
               f"Task:                       {self.task}\n" \
               f"Assigned to:                {self.assigned_to}\n" \
               f"Date Assigned:              {self.date_assigned}\n" \
               f"Due Date:                   {self.due_date}\n" \
               f"Task Complete?              {self.complete}\n" \
               f"Task Description:\n" + \
               textwrap.fill(f"      {self.task_description}", 70) + \
               "\n—————————————————————————————————————————————————————————————————————"


# -------- Functions --------
# Function to load users text and create dictionary
def check_number(string_input: str) -> Union[int, None]:
    try:
        num = int(string_input)
        return num
    except ValueError:
        print("The input cannot be converted to a number!")
        return None


# Check if input string can be cast to a date
def check_date(date_input: str) -> Union[datetime, None]:
    try:
        return datetime.strptime(date_input, "%d %b %Y")
    except ValueError:
        print("The date is not correctly formatted")
        return None


# We'll create a function that can read our users.txt and create a dictionary
# pairing their passwords to their usernames
def open_users_to_dict(text_file: str) -> dict[str: str]:
    """Note: Type hints is a Python 3.5 feature.
    This function reads in a users.txt file formatted as 'USER, PASS' with
    a new line for each user. Here we transform that into a list where
    EVEN elements are users and ODD elements are passwords"""
    try:
        with open(text_file, "r", encoding="utf-8") as user_file:
            read_users_in_file = user_file.read()
            read_users_in_file = read_users_in_file.replace("\n", ", ")
            users_list = read_users_in_file.split(", ")
            users = []
            passes = []
            for i, user in enumerate(users_list):
                if i % 2 == 0:
                    users.append(user)
                else:
                    passes.append(user)

            users_dict = {key: value for key, value in zip(users, passes)}

            return users_dict
    except FileNotFoundError:
        print("\033[91m" + "\033[1m" + "STOP!" + "\033[00m")
        print("A users.txt file is required to run the program... "
              "Please ensure you download the provided txt files to run the program")
        print("Now exiting...")
        exit()


# This utility function we'll call everytime we want to exit from
# a function back to the main menu
def return_to_menu(check_var: str) -> Union[None, int]:
    if check_var == "q" or check_var == "-1":
        print("Returning to Main Menu...")
        return None
    else:
        return 1


# reg user, make sure no user has the same username, update dict of users
def reg_user(users_dict: dict) -> Union[dict, None]:
    reg_new_pass = None
    new_user_success = False

    while True:
        reg_new_user = input("Please enter username (or type q to go back to Main Menu): ")

        if return_to_menu(reg_new_user) is None:
            return

        if reg_new_user in users_dict:
            print("Sorry the Username is already registered... Please try another")
            continue
        else:
            new_user_success = True
            break

    while new_user_success:
        # Create list from user input
        reg_new_pass = input("Please enter password (or type q to return to Main Menu): ")

        if return_to_menu(reg_new_pass) is None:
            return

        # Get pass from user again
        pass_match_check = input("Please type your password in again (or type q to return to Main Menu): ")

        # We'll give the user an opportunity to exit from registering the user using "q"
        if pass_match_check.lower() == "q":
            print("No user has been registered... Returning to Main Menu")
            return None

        # Check if user typed in the same pass
        if reg_new_pass == pass_match_check:
            break
        else:
            print("Sorry the password does not match... Please try again")

    # If above is successful write the result to the user.txt file
    with open("user.txt", "a", encoding="utf-8") as tasks_file:
        tasks_file.write(f"\n{reg_new_user}, {reg_new_pass}")

    print()
    print("\033[1m" + "New user successfully added!" + "\033[0m")

    # Above will append the new user - here we'll read the file again (making sure it's after the change)
    # and update the credentials_list to include the newly added user
    return open_users_to_dict("user.txt")


# Add a task to tasks.txt return a list of updated tasks
def add_task(users_dict: dict, tasks_file_path: str) -> Union[list[Task], None]:
    # initialize the date.today() function to var today
    today = date.today()

    print("\033[1m" + "———— Add a Task ————" + "\033[0m")

    # We'll loop and check if the specified user actually exists
    while True:
        user_to_assign = input("Which user do you want to assign the task to? "
                               "(type q to go back to Main Menu): ")

        if return_to_menu(user_to_assign) is None:
            return

        # if the user exists we'll prompt the user, and assign their input to variables
        # and if not we'll ask them to try again
        if user_to_assign in users_dict:
            print("Success!!! Username found...")
            task_title = input("Please input the task title: ")
            task_description = input("Please write a description of the task: ")
            while True:
                task_due_date = input("What is the task due date (for example: 10 Oct 2022): ")

                try:
                    task_due_date = datetime.strptime(task_due_date, "%d %b %Y")
                    break
                except Exception:
                    print("date has not been written in the correct format!... Please try again")
                    continue

            current_date = today.strftime("%d %b %Y")
            task_complete = "No"
            break

        else:
            # Empty print for visual space
            print()
            print("Sorry the username has NOT been found... Please Try again")

    # We'll try to write the successful input from above to the tasks.txt file
    # We'll handle to errors and ask the user to check the tasks.txt
    # in a case where there is a problem with the file it will affect our ability to successfully read it
    try:
        with open("tasks.txt", "a", encoding="utf-8") as tasks_file:
            tasks_file.write(f"\n{user_to_assign}, {task_title}, {task_description}, {current_date}, "
                             f"{str(task_due_date.strftime('%d %b %Y'))}, {task_complete}")
    except IndexError:
        print("The text file may be tampered with please re-download the tasks.txt file and try again")
        return
    except FileNotFoundError:
        print("Is the tasks.txt file present? Please look in your projects dir and try again")
        return

    # An extra print for visual space
    print()

    # update the current task list
    tasks_list = load_tasks(tasks_file_path)
    if tasks_list is None:
        print("There's been a error creating your task!")
        return

    print("———— Task has been successfully added! ————")
    return tasks_list


# View all simply goes through the task list printing each
# all we need to do is call print(task) as the dunder method in class
# takes care of the string representation
def view_all(list_of_tasks: list[Task]):
    print("\033[1m" + "———— View All Tasks ————" + "\033[0m")

    for task in list_of_tasks:
        print(YELLOW + BOLD + f"Task Number: {list_of_tasks.index(task)}" + ESCAPE)
        print(task)

    print("\033[1m" + "———— END OF TASKS ————" + "\033[0m")


# We'll load tasks to a list of task objects
# We'll use the list created by this function in our other functions
def load_tasks(tasks_file_path: str) -> Union[list[Task], None]:
    try:
        with open(tasks_file_path, "r", encoding="utf-8") as read_tasks:
            # Create an empty outer list to put our other lists in
            tasks_list = []

            for line in read_tasks:
                # Strip newline chars & split the line by ", " store result to list
                line = line.strip("\n")
                tasks_sections = line.split(", ")
                # Append the above list to the outer list
                try:
                    task = Task(tasks_sections[0], tasks_sections[1],
                                tasks_sections[2], tasks_sections[3], tasks_sections[4], tasks_sections[5])
                    tasks_list.append(task)
                except IndexError:
                    print("\033[91m" + "\033[1m" + "The file looks like it's been tampered with, "
                                                   "please check or re-download, the tasks.txt file" + "\033[00m")
                    return

            return tasks_list
    except FileNotFoundError:
        print("\033[91m" + "\033[1m" + "STOP!" + "\033[00m")
        print("A tasks.txt file is required to run the program... "
              "Please ensure you download the provided txt files to run the program")
        print("Now exiting...")
        exit()


# This function will save the tasks to the tasks.txt file and load_tasks()
# can be called to load from file
def save_tasks(tasks_list: list[Task], tasks_path: str):
    try:
        with open(tasks_path, "w", encoding="utf-8") as tasks_file:
            for task in tasks_list:
                tasks_file.write(f"{task.assigned_to}, {task.task}, "
                                 f"{task.task_description}, {task.date_assigned}, {task.due_date}, {task.complete}\n")
    except PermissionError:
        print("You do not have permission to access the file... Is the file open? Please"
              "close it and try again")
        return
    except IOError:
        print("There was an error reading/writing the file")
        return
    except Exception:
        print("There's been a general problem... please check your system and try again")
        return


# This function allows the user to view and edit their own tasks
# This function provides a sub menu to the user with options on how they can edit the
# task
def view_mine(tasks_list: list[Task], task_path: str, users_dict: dict, logged_in_user: str):
    print()
    print("\033[1m" + "———— View My Tasks ————" + "\033[0m")
    # TODO Write some comments
    my_tasks = []

    for task in tasks_list:
        if task.assigned_to == logged_in_user:
            my_tasks.append(task)
            print("—————————————————————————————————————————————————————————————————————")
            # we're adding plus 1 to the index to remove zero indexing when we reference
            # the number later we'll minus 1
            print(YELLOW + BOLD + f"Task Number: {tasks_list.index(task)}" + ESCAPE)
            print(task)
    print("——————————————————————————  END OF TASKS —————————————————————————————")

    if len(my_tasks) < 1:
        print("\033[91m" + "\033[1m" + "You have no tasks assigned!" + "\033[00m")
        print()
        return

    print()

    # View Mine Sub Menu
    # Below is our flow for the sub menu structure at most points we'll allow the user
    # to quit using q or -1
    while True:

        task_selection = input(BOLD + "Please choose a task to edit "
                                      "(-1 or q to go back to main menu): " + ESCAPE)
        if return_to_menu(task_selection) is None:
            return

        if check_number(task_selection) is None:
            print("...Please try again")
            continue

        if int(task_selection) in range(len(tasks_list)) \
                and tasks_list[int(task_selection)].assigned_to == logged_in_user:
            while True:
                print("\033[1m" + "———— View Mine Sub Menu ————" + "\033[0m")

                edit_select = input("""Please choose what you'd like to do, from the following:
1 - Set task as complete
2 - Edit user assigned to
3 - Edit due date
q or -1 to go back to Main Menu: """)

                if return_to_menu(edit_select) is None:
                    return

                match edit_select:
                    case "1":
                        task_complete = input('Is the task complete? Type "Yes" or "No": ')
                        if task_complete.lower() == "yes" or task_complete.lower() == "no":
                            tasks_list[int(task_selection)].complete = task_complete.capitalize()
                            print(tasks_list[int(task_selection)])

                            save_tasks(tasks_list, task_path)

                        else:
                            print("Sorry it seems you've typed the input incorrectly..."
                                  "Returning to View Mine Sub Menu")

                    case "2":
                        if tasks_list[int(task_selection)].complete == "No":
                            assign_new_user = input("Please enter the user you'd like to re-assign the task to: ")
                            if assign_new_user in users_dict:
                                tasks_list[int(task_selection)].assigned_to = assign_new_user.lower()
                                save_tasks(tasks_list, task_path)

                                print("The user for the task has been reassigned... Returning to Main Menu")
                                return
                            else:
                                print("\033[91m" + "\033[1m" + "User not recognised... "
                                                               "Returning to View Mine Sub Menu" + "\033[00m")
                        else:
                            print("\033[91m" + "\033[1m" + "The task is already complete - "
                                                           "Returning to View Mine Sub Menu" + "\033[00m")

                    case "3":
                        if tasks_list[int(task_selection)].complete == "No":
                            new_due_date = check_date(input("Please input the new date (example format 10 Oct 2019): "))

                            if new_due_date is not None:
                                tasks_list[int(task_selection)].due_date = str(new_due_date.strftime("%d %b %Y"))
                                save_tasks(tasks_list, task_path)

                                print("The due date for the task has been reassigned... Returning to Main Menu")
                                return
                            else:
                                print("... Please try again")
                        else:
                            print("\033[91m" + "\033[1m" + "The task is already complete - "
                                                           "Returning to View Mine Sub Menu" + "\033[00m")

                    case "q" | "-1":
                        print("Returning to Main Menu...")
                        return
                    case _:
                        print("Invalid selection! Please try again (q or -1 to return to Main Menu)")
        else:
            print("You've made an incorrect selection... Please try again")


# in display stats we'll first call the generate functions for tasks and users
# this means we'll always get the latest stats when choosing the ds option from the menu
# there could be an issue, so we'll handle that present a message to the user
# and return without displaying any stats
def display_stats(dict_of_users: dict[str], list_of_tasks: list[Task]):
    try:
        gen_task_report(list_of_tasks)
    except Exception:
        print("Something is stopping the tasks overview file being written!")
        return

    try:
        gen_user_report(dict_of_users, list_of_tasks)
    except Exception:
        print("Something is stopping the users overview file being written!")
        return

    # Print Task Overview to console
    try:
        with open("task_overview.txt", "r", encoding="utf-8") as task_overview:
            for line in task_overview:
                line = line.strip("\n")
                print(line)
    except FileNotFoundError:
        print("It looks like there was a problem creating the task_overview.txt file")
        return

    try:
        # Print User Overview to console
        with open("user_overview.txt", "r", encoding="utf-8") as user_overview:
            for line in user_overview:
                line = line.strip("\n")
                print(line)
    except FileNotFoundError:
        print("It looks like there was a problem creating the user_overview.txt file")
        return


# We'll use the below function to define which menu shold be displayed to which user
# admin gets an extended menu
def display_menu(user_obj: User, standard_menu_dict: dict, admin_menu_dict: dict) -> str:
    print("\033[93m" + "\033[1m" + "———— ■ MAIN MENU ■ ————" + "\033[0m")
    print("\033[1m" + "Select one of the following options below" + "\033[0m")

    for key in standard_menu_dict:
        print("►", key, "-", standard_menu_dict[key])

    if user_obj.is_admin:
        print("\033[1m" + "———— Admin Options ————" + "\033[0m")
        for key in admin_menu_dict:
            print("►", key, "-", admin_menu_dict[key])


# This function will check the time of the day and greet the user accordingly
def greet_user(user_name: str):
    # Get the current hour
    current_hour = datetime.now().hour

    # Determine the greeting based on the current hour
    if 6 <= current_hour < 12:
        greeting = "Good Morning"
    elif 17 > current_hour >= 12:
        greeting = "Good Afternoon"
    elif 22 >= current_hour >= 17:
        greeting = "Good Evening"
    else:
        greeting = "Hey! You're Up Late"

    # Print the greeting and the user's name
    print("\033[1m" + "\033[96m" + f"{greeting}, {user_name.capitalize()}!" + "\033[1m")
    print()


# This is a small utility function to calculate percentages
def percent_calc(a: int, b: int) -> float:
    try:
        return round(float(a / b * 100), 2)
    except ZeroDivisionError:
        return 0.0


# This function generates the tasks_overview.txt
def gen_task_report(list_of_tasks: list[Task]) -> None:
    # Total number of tasks
    total_task_num = len(list_of_tasks)

    # TODO could possibly combine the loops so we're not looping
    # TODO multiple times
    # Total number of completed tasks
    count_complete = 0
    count_incomplete = 0
    for i in list_of_tasks:
        if i.complete == "Yes":
            count_complete += 1
        else:
            count_incomplete += 1

    # Find overdue tasks
    today = date.today()
    overdue_count = 0
    for task in list_of_tasks:
        task_due = datetime.strptime(task.due_date, "%d %b %Y")

        if today > task_due.date():
            overdue_count += 1

    # Percentage incomplete
    incomplete_percent = percent_calc(count_incomplete, total_task_num)
    overdue_percent = percent_calc(overdue_count, total_task_num)

    # Print everything to console for a test
    output_string = (f"———————————————— Task Overview ————————————————\n"
                     f"Total Number Of Tasks:         {total_task_num}\n"
                     f"Completed Tasks:               {count_complete}\n"
                     f"Incomplete Tasks:              {count_incomplete}\n"
                     f"Total Overdue:                 {overdue_count}\n"
                     f"Percent Incomplete:            {incomplete_percent}%\n"
                     f"Percent Overdue:               {overdue_percent}%\n"
                     f"——————————————————————————————————————————————")

    # Write task_overview.txt file
    try:
        with open("task_overview.txt", "w", encoding="utf-8") as task_overview:
            task_overview.write(output_string)
    except PermissionError:
        print("\033[91m" + "\033[1m" + "The file cannot be written... Is it open?" + "\033[0m")
        return
    except IOError:
        print("\033[91m" + "\033[1m" + "The file cannot be written" + "\033[0m")
        return
    except Exception:
        print("\033[91m" + "\033[1m" + "We've ran into an unknown problem please check your system" + "\033[0m")
        return


# This function generates the users_overview.txt
def gen_user_report(dict_of_users: dict[str], list_of_tasks: list[Task]) -> None:
    # Total number of user
    num_of_users = len(dict_of_users)

    # Total number of tasks
    total_task_num = len(list_of_tasks)
    today = date.today()

    users_stats_string = ""

    users_stats_string += f"———————————————— User Overview ————————————————\n"

    for user in dict_of_users:
        user_details = ""
        user_header = f"• {str(user).capitalize()} •\n"
        task_count = 0
        complete_task_count = 0
        overdue_tasks_count = 0

        for task in list_of_tasks:
            if str(user) == task.assigned_to:
                task_count += 1
                if task.complete == "Yes":
                    complete_task_count += 1

                task_due = datetime.strptime(task.due_date, "%d %b %Y")

                if today > task_due.date():
                    overdue_tasks_count += 1

        percentage_assigned = percent_calc(task_count, total_task_num)
        percent_user_completed = percent_calc(complete_task_count, task_count)
        percent_left = 100 - (percent_calc(complete_task_count, task_count))
        overdue_percent = percent_calc(overdue_tasks_count, task_count)

        user_details += user_header
        user_details += f"Tasks Assigned:                           {task_count}\n"
        user_details += f"Percentage of Tasks Assigned:             {percentage_assigned}%\n"
        user_details += f"Percentage of Tasks Assigned Completed:   {percent_user_completed}\n"
        user_details += f"Percentage Left To Complete:              {percent_left}%\n"
        user_details += f"Percentage of Tasks Overdue:              {overdue_percent}%\n"
        user_details += "\n"

        users_stats_string += user_details

    # Write the user overview
    try:
        with open("user_overview.txt", "w", encoding="utf-8") as task_overview:
            task_overview.write(users_stats_string)
    except PermissionError:
        print("\033[91m" + "\033[1m" + "The file cannot be written... Is it open?" + "\033[0m")
        return
    except IOError:
        print("\033[91m" + "\033[1m" + "The file cannot be written" + "\033[0m")
        return
    except Exception:
        print("\033[91m" + "\033[1m" + "We've ran into an unknown problem please check your system" + "\033[0m")
        return


# -------- Global Variables --------
# Styling
BLUE = "\033[94m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
ESCAPE = "\033[00m"
CYAN = "\033[96m"
PURPLE = "\033[35m"
BOLD = "\033[1m"

attempts = 3
login_success = False
user_match = False
pass_match = False
# We'll need to hold on to the username for the main loop
logged_user_name = ""
user_object = None
tasks = []

# Menu dictionaries - note we have a regular user menu and an admin one that includes only the extra
# options available to the admin
# we'll use our display_menu() function to format displaying it to the user
user_menu_dict = {
    "a": "Add a task",
    "va": "View all Tasks",
    "vm": "View my Tasks",
    "e": "Exit"
}

admin_menu_dict = {
    "r": "Register a user",
    "ds": "Display statistics",
    "gr": "Generate reports"
}

# Here we'll create an empty menu that gets set once we understand the status of the user
presented_menu = {}

# Call open_and_list_users save it to variable credentials_list
credentials_dict = open_users_to_dict("user.txt")

# ------------------------- PROGRAM ENTRY POINT --------------------------
print(BLUE + "╔═════════════════════════════════════════════╗" + ESCAPE)
print(RED + "              🔨 TASK MANAGER 🔨" + ESCAPE)
print(BLUE + "╚═════════════════════════════════════════════╝" + ESCAPE)

# Note: When you see this weird escape sequence, it's just to display the string in bold
print(BOLD + "———— Welcome! Please Login ————" + ESCAPE)

# ==== Login Section ====
# The thought here is to load the available usernames and passwords and check user input against
# those loaded from user.txt. We'll loop 3 times if unsuccessful we'll exit the program after these failed attempts.

# Login Loop
while attempts > 0:
    user_input_list = [input("Please Enter Your Username: "), input("Please Enter Your Password: ")]

    logged_user_name = user_input_list[0]
    # Looping through the even numbered credentials gives us a username
    # Looping through odd numbered credentials gives us passwords
    if user_input_list[0] in credentials_dict:
        user_match = True
    if user_match and user_input_list[1] == credentials_dict[logged_user_name]:
        pass_match = True
    else:
        user_match = False

    # If we match both a user and pass we set login_success to True
    # if not we prompt user with the amount of attempts left
    # ultimately if no attempts are left we'll exit the program
    if user_match and pass_match:
        print("Successful login!...")
        login_success = True
        logged_user_name = user_input_list[0]
        break
    else:
        # Here we'll check how many attempts the user has and update the message as needed
        # If none left we exit the program
        # Note: Match/case is a Python 3.10 feature please make sure you have an
        # up-to date install
        match attempts:
            case 2 | 3:
                attempts -= 1
                print(f"Incorrect, you have {attempts} attempts left...")
            case _:
                attempts -= 1
                print("Sorry you tried too many times... Please contact your system admin")
                print("Program will now exit...")
                exit()

# We'll consume our User class here after successful login
# We'll need a set of if statements to understand the status of the logged-in user
if login_success:
    user_object = User(logged_user_name)
    tasks = load_tasks("tasks.txt")
    greet_user(logged_user_name)

if logged_user_name == "admin":
    user_object.set_admin()

# We'll merge the user menu and admin menu dictionaries if admin else just present the user menu
if user_object.is_admin:
    presented_menu = user_menu_dict | admin_menu_dict
else:
    presented_menu = user_menu_dict

# If login successful We'll move onto the main loop
# Using the login_success bool we'll only run the following code after successful login
while login_success:

    # Display Menu
    display_menu(user_object, user_menu_dict, admin_menu_dict)

    # Prompt user for input
    menu = input(": ").lower()

    # Check users input against dictionary
    if menu not in presented_menu:
        print("You've entered something incorrectly... Please try again")
        continue

    match menu:
        case "r":
            # We'll call reg_user() here this function returns a dict with the updated users
            credentials_dict = reg_user(credentials_dict)

        case "a":
            # call add_task() and save result to tasks, this will give us upto date tasks
            tasks = add_task(credentials_dict, "tasks.txt")

        case "va":
            view_all(tasks)

        case "vm":
            view_mine(tasks, "tasks.txt", credentials_dict, logged_user_name)

        case "ds":
            display_stats(credentials_dict, tasks)

        case "gr":
            gen_task_report(tasks)
            gen_user_report(credentials_dict, tasks)
            print(GREEN + BOLD + "Report generated!" + ESCAPE)

        case "e":
            print("Goodbye!!!")
            exit()
