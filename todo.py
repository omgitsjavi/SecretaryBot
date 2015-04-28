"""Module for task lists and help deciding what to do right now."""

import random
from time import sleep
import json
from sbot_exceptions import *

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
    """Parses line address from "x.y.z" format into [x-1, y, z].

       The first index is -1 to adjust for the implementation of nested
       lists in this module."""
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
    # Convert string indices into ints
    result = index
    i = 0
    for line_index in index:
        result[i] = int(line_index)
        i += 1
    # -1 first index to correct for implementation of nested lists
    result[0] -= 1
    return result

def read_line(nested_list, line_index):
    """Traverse nested list to obtain the line at given line_address."""
    result = nested_list[:]
    for index in line_index:
        # Conditional for catching index errors
        if type(result) == type([]):
            result = result[index]
        else:
            raise IndexError
    # Accounts for if request is the first line in a sublist
    if type(result) == type([]):
        result = result[0]
    return result

def parse_list(nested_list, indent=0, sup_line=""):
    """Takes a raw nested list and returns a human-readable organized list."""
    result = ""
    tab = ""
    # Build indent string
    for i in range(indent):
        tab += "    "
    # Go through line by line
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
        # Else each line is added to result with a newline inserted
        else:
            result = result + tab + line_label + line + '\n'
        i += 1
    return result

def delete_all_lists():
    unanswered = True
    while unanswered:
        print "\nYou're about to throw away EVERYTHING. Like, all of it."
        sleep(1.5)
        print "Would this really, truly make you happy?"
        answer = raw_input('Y/N> ')
        if answer in "Yy":
            print "If you say so."
            sleep(1)
            print "Shredding all your hard work",
            for i in range(3):
                print ".",
                sleep(1.5)
            with open(user_file, 'w') as file:
                user_data['todo'] = {}
                json.dump(user_data, file)
            print "Done!"
            unanswered = False
            sleep(2)
            print
        elif answer in "Nn":
            print "That's right. In fact, you should go make another list for the collection!"
            unanswered = False
            sleep(1.5)
            print
        

def quit_todo():
    global run
    run = False

def close_list(*args):
    global list_opened
    list_opened = False

def rename_list(old_list_name):
    new_name = raw_input('New List Name> ')
    # Auto-capitalize
    new_name = new_name.title()
    with open(user_file, 'w') as file:
        user_data['todo'][new_name] = user_data['todo'][old_list_name]
        del user_data['todo'][old_list_name]
        json.dump(user_data, file)
    close_list()

def delete_list(list_name):
    unanswered = True
    while unanswered:
        print "\nToss the whole thing in the can? You sure?"
        answer = raw_input('Y/N> ')
        if answer in "Yy":
            with open(user_file, 'w') as file:
                del user_data['todo'][list_name]
                json.dump(user_data, file)
            sleep(1)
            print "Job's done. Hope you're happy."
            sleep(2)
            unanswered = False
            close_list()
        elif answer in "Nn":
            print "Got it. Yeah I dunno what you were thinking, to be honest."
            unanswered = False
            sleep(1)
            

def remove_line_at_address(nested_list, line_index):
    """Returns modified list with line removed at the specified line_index.

       Assumes that line_index is in parse_line_number format."""
    result = nested_list[:]
    top_index = line_index[0]
    # Traverse up to the last index
    if len(line_index) > 1:
        result[top_index] = remove_line_at_address(result[top_index],
                                                   line_index[1:])
    # Remove the specified line at the final index
    else:
        del result[top_index]
    return result

def remove_line(list_name, line_number):
    """Removes line specified by line_number."""
    edited_list = user_data['todo'][list_name]
    line_index = parse_line_number(line_number)
    try:
        print read_line(edited_list, line_index)
    except IndexError:
        raise NestedListIndexError(line_number)
    else:
        edited_list = remove_line_at_address(edited_list, line_index)
        with open(user_file, 'w') as file:
            user_data['todo'][list_name] = edited_list
            json.dump(user_data, file)

def insert_line_at_address(nested_list, line_index, new_line):
    """Returns modified list with new_line inserted below specified line_index.

       Assumes that line_index is in parse_line_number format."""
    result = nested_list[:]
    top_index = line_index[0]
    # Traverse up to the last index
    if len(line_index) > 1:
        result[top_index] = insert_line_at_address(result[top_index],
                                                   line_index[1:], new_line)
    # Insert below line at final index
    else:
        # If there are already lines below it, insert at bottom of sublist
        if type(result[top_index]) == type([]):
            result[top_index].append(new_line)
        # Else create sublist
        else:
            new_sublist = [result[top_index]]
            new_sublist.append(new_line)
            result[top_index] = new_sublist
    return result

def insert_line(list_name, line_number):
    """Insert line beneath specified line_number."""
    edited_list = user_data['todo'][list_name]
    line_index = parse_line_number(line_number)
    try:
        read_line(edited_list, line_index)
    except IndexError:
        raise NestedListIndexError(line_number)
    print "Inserting a line beneath " + line_number + "..."
    new_line = raw_input('Line Contents> ')
    edited_list = insert_line_at_address(edited_list, line_index, new_line)
    with open(user_file, 'w') as file:
        user_data['todo'][list_name] = edited_list
        json.dump(user_data, file)

def edit_line_at_index(nested_list, line_index, new_line):
    """Returns modified list with new_line replacing specified line_index.

       Assumes that line_index is in parse_line_number format."""
    result = nested_list[:]
    top_index = line_index[0]
    #Traverse up to the last index
    if len(line_index) > 1:
        result[top_index] = edit_line_at_index(result[top_index],
                                               line_index[1:], new_line)
    # Change specified line
    else:
        # Accounts for if specified line starts a sublist
        if type(result[top_index]) == type([]):
            result[top_index][0] = new_line
        else:
            result[top_index] = new_line
    return result

def edit_line(list_name, line_number):
    """Changes line at specified line_number."""
    line_index = parse_line_number(line_number)
    try:
        read_line(user_data['todo'][list_name], line_index)
    except IndexError:
        raise NestedListIndexError(line_number)
    old_line = read_line(user_data['todo'][list_name], line_index)
    print "Editing:", old_line
    new_line = raw_input(line_number + '> ')
    edited_list = user_data['todo'][list_name]
    edited_list = edit_line_at_index(edited_list, line_index, new_line)
    with open(user_file, 'w') as file:
        user_data['todo'][list_name] = edited_list
        json.dump(user_data, file)

# open_list placeholder, function is defined below list_options
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
    print "Quite excellent."
    sleep(0.75)
    print
    open_list(list_name)

def new_line(list_name):
    line_contents = raw_input('New Line> ')
    with open(user_file, 'w') as file:
        user_data['todo'][list_name].append(line_contents)
        json.dump(user_data, file)

def editing_help(*args):
    print """\nNEW LINE: Add a top-level line.
INSERT [line number]: Insert line below the given line.
EDIT [line number]: Edits the given line.
DELETE [line number]: Removes the given line.
                      THIS WILL ALSO REMOVE ALL LINES UNDER IT."""
    sleep(1)

module_menu = "NEW LIST | DELETE ALL LISTS | GIVE ME A NUMBER | QUIT to Main Menu"
menu_options = {'new list': new_list,
                'delete all lists': delete_all_lists,
                'give me a number': give_me_a_number,
                'quit': quit_todo}
list_menu = "RENAME | DELETE | HELP with Editing | BACK to Menu"
list_options = {'new line': new_line,
                'rename': rename_list,
                'delete': delete_list,
                'help': editing_help,
                'back': close_list}

def open_list(list_name):
    """Opens a saved list for editing."""
    global list_opened
    list_opened = True
    while list_opened:
        print "\n", list_name + ":"
        print parse_list(user_data['todo'][list_name])
        print list_menu
        command = raw_input('LIST> ')
        print
        # Note that the INSERT, DELETE, and EDIT commands must separate out line number
        if "delete " in command:
            try:
                remove_line(list_name, command[7:])
            except NestedListIndexError as error:
                print error
        elif "insert " in command:
            try:
                insert_line(list_name, command[7:])
            except NestedListIndexError as error:
                print error
        elif "edit " in command:
            try:
                edit_line(list_name, command[5:])
            except NestedListIndexError as error:
                print error
        elif command in list_options:
            list_options[command](list_name)
        else:
            print CommandError(command)


# Module loop
def todo(active_user):
    global run
    load_user(active_user)
    run = True
    
    while run:
        for list_name in user_data['todo']:
            print "[" + list_name + "]"
        print module_menu

        entered = raw_input('TODO> ')
        if entered.title() in user_data['todo']:
            open_list(entered.title())
        elif entered in menu_options:
            print
            menu_options[entered]()
        else:
            print CommandError(entered), "\n"
            


##nested_list1 = ['Line 1', ['Line 2', 'Line 2.1', ['Line 2.2', 'Line 2.2.1'], 'Line 2.3'], 'Line 3']
##potato_list = [["Potatoes", "Red potatoes", "Old potatoes"], "Fish"]
##print parse_list(potato_list)
##print "Requesting '1.1'...", read_line(parse_line_number("1.1"), potato_list)
##print "----------------"
##print parse_list(nested_list1)
##print "Requesting '2.2.1'...", read_line(parse_line_number("2.2.1"), nested_list1)
