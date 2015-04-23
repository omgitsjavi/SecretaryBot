"""Module for task lists and help deciding what to do right now."""

import random
from time import sleep
import json

help_text = """This module keeps track of organized lists. Each list is saved
separately and editable line by line. To manage each list, open it by entering
its name at the main menu. All labels are automatically capitalized, so names
should be entered lowercase, as with all commands."""


def init_todo_data():
    """Initializes user's ToDo data to an empty dictionary."""
    print "Initializing ToDo data...",
    with open(user_file, 'w') as file:
        user_data['todo'] = {}
        json.dump(user_data, file)
    sleep(0.5)
    print "Done!"
    sleep(0.5)
    # Include welcome message and help info to new user
    print "\n", "Welcome to ToDo!", '\n', help_text, '\n'
    sleep(2.0)

def load_user(active_user):
    """Loads active user's save data."""
    global user_file, user_data
    user_file = active_user.name + ".txt"
    with open(user_file, 'r') as file:
        user_data = json.load(file)
    # If no ToDo data, update profile
    if "todo" not in user_data:
        init_todo_data()

def give_me_a_number():
    print "Ohmmm..."
    thinking_time = random.randrange(1, 2) + random.random()
    sleep(thinking_time)
    print "Your lucky number is " + str(random.randrange(101, 1500)) + "."
    sleep(1.25)
    print

def parse_line_number(line_address):
    """Parses line address from "1.2" format into ["1", "2"]."""
    index = []
    i = 0
    starts_index = True
    # Parses given string into a list address
    for char in line_address:
        if char == ".":
            i += 1
            # Boolean for separating indices, ie, "21.3" becomes ["21", "3"]
            starts_index = True
        else:
            if starts_index:
                index.append(char)
                starts_index = False
            else:
                index[i] += char
    return index

def read_line(line_address, todo_list):
    """Traverse nested list to obtain the line at given line_address."""
    # Top level index must be -1 to accomodate list structure implementation
    result = todo_list[int(line_address[0]) - 1]
    for index in line_address[1:]:
        result = result[int(index)]
    # Accounts for if request is the first line in a sublist
    if type(result) == type([]):
        result = result[0]
    return result

def parse_list(nested_list, indent=0, sup_line=""):
    """Turns a raw nested list into a human-readable organized list."""
    result = ""
    tab = ""
    # Build indent string
    for i in range(indent):
        tab += "    "

    i = 1
    for line in nested_list:
        # Build label based on current line
        if sup_line != "":
            line_label = sup_line + "." + str(i) + " "
        else:
            line_label = str(i) + " "
        # If line begins a nested list, traverse it, increasing indent for sublist
        if type(line) == type([]):
            result = result + tab + line_label + line[0] + '\n'
            # Note that sup_line strips the trailing space before passing
            result += parse_list(line[1:], indent=indent + 1, sup_line=line_label[:-1])
        # Else each line is simply added to result with a newline inserted
        else:
            result = result + tab + line_label + line + '\n'
        i += 1
    return result

def delete_all_lists():
    pass

def quit_todo():
    global run
    run = False

def edit_list():
    pass

def rename_list():
    pass

def delete_list():
    pass

# open_list placeholder, function is defined below new_list
def open_list():
    pass

def new_list():
    """Creates a new list saved in the user's profile."""
    print "A new list, so exciting! What do you want to call it?"
    list_name = raw_input('List name> ')
    # Auto-capitalize
    list_name = list_name.title()
    # Save to file
    with open(user_file, 'w') as file:
        user_data['todo'][list_name] = []
        json.dump(user_data, file)
    print "Quite excellent.", "\n"
    sleep(0.75)
    open_list(list_name)

def close_list(*args):
    global list_opened
    list_opened = False

module_menu = "NEW LIST | DELETE ALL LISTS | GIVE ME A NUMBER | QUIT to Main Menu"
menu_options = {'new list': new_list,
                'delete all lists': delete_all_lists,
                'give me a number': give_me_a_number,
                'quit': quit_todo}
list_menu = "EDIT | RENAME | DELETE | BACK to Menu"
list_options = {'edit': edit_list,
                'rename': rename_list,
                'delete': delete_list,
                'back': close_list}

def open_list(list_name):
    """Opens a saved list for editing."""
    global list_opened
    list_opened = True
    while list_opened:
        print list_name + ":"
        print parse_list(user_data['todo'][list_name])
        print "EDIT | RENAME | DELETE | BACK to Menu"
        command = raw_input('LIST> ')
        if command in list_options:
            list_options[command]()
        else:
            print "Command not recognized."


# Module loop
def todo(active_user):
    global run
    load_user(active_user)
    run = True
    
    while run:
        for list_name in user_data['todo']:
            print list_name + "   "
        print module_menu

        entered = raw_input('TODO> ')
        if entered.title() in user_data['todo']:
            open_list(entered.title())
        elif entered in menu_options:
            print
            menu_options[entered]()
        else:
            print "Command not recognized.", "\n"
            


##nested_list1 = ['Line 1', ['Line 2', 'Line 2.1', ['Line 2.2', 'Line 2.2.1'], 'Line 2.3'], 'Line 3']
##potato_list = [["Potatoes", "Red potatoes", "Old potatoes"], "Fish"]
##print parse_list(potato_list)
##print "Requesting '1.1'...", read_line(parse_line_number("1.1"), potato_list)
##print "----------------"
##print parse_list(nested_list1)
##print "Requesting '2.2.1'...", read_line(parse_line_number("2.2.1"), nested_list1)
