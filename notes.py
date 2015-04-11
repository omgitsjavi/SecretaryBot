"""Notes module, used by user for storing miscellaneous bits of information."""
import json
from time import sleep

help_text = """The Notes module saves any piece of information you might want to 
recall later. Each note is saved with a label and can be edited freely.
To read or edit a note, enter its name at the main menu. All note labels are
automatically capitalized, so just enter note names lowercase, as always."""

def init_notes_data():
    """Initializes user's Notes data to an empty dictionary."""
    print "Initializing Notes data...",
    with open(user_file, 'w') as file:
        user_data['notes'] = {}
        json.dump(user_data, file)
    sleep(0.5)
    print "Done!\n"
    sleep(0.5)
    # Include welcome message and help info to new user
    print "Welcome to Notes!", '\n', help_text, '\n'
    sleep(2.0)

def load_user(active_user):
    """Loads active user's save data."""
    global user_file, user_data
    user_file = active_user.name + ".txt"
    with open(user_file, 'r') as file:
        user_data = json.load(file)
    # If no Notes data, update profile
    if "notes" not in user_data:
        init_notes_data()

def quit_notes():
    global run
    run = False

def new_note():
    """Creates a new note based on user input."""
    print "What do you want to save?"
    note_contents = raw_input('Note contents> ')
    print "And what shall I file it under, luv?"
    note_label = raw_input('Note label> ')
    # Auto-capitalize
    note_label = note_label.title()
    # Save to file
    with open(user_file, 'w') as file:
        user_data['notes'][note_label] = note_contents
        json.dump(user_data, file)
    print "Got it!", "\n"
    
def edit_note(note_name):
    print "Give me the update. Or CANCEL, that's alright, too."
    new_contents = raw_input('New Contents> ')
    if new_contents == 'cancel':
        return 0
    else:
        with open(user_file, 'w') as file:
            user_data['notes'][note_name] = new_contents
            json.dump(user_data, file)
    print "Saved!"
    sleep(0.5)
    
def rename_note(note_name):
    print "What should I call it now? Or CANCEL."
    new_label = raw_input('New Label> ')
    if new_label == 'cancel':
        return 0
    else:
        new_label = new_label.title()
        note_contents = user_data['notes'][note_name]
        with open(user_file, 'w') as file:
            user_data['notes'][new_label] = note_contents
            del user_data['notes'][note_name]
            json.dump(user_data, file)
    print "Done! Returning to Notes list."
    close_note()
    sleep(0.5)
    
def delete_note(note_name):
    print "Don't need this anymore? No problem."
    with open(user_file, 'w') as file:
        del user_data['notes'][note_name]
        json.dump(user_data, file)
    close_note()
    sleep(0.75)

        
def delete_all_notes():
    print """You're about to delete ALL of your notes.
Are you really, truly, very, very sure? [YES/NO]"""
    # Get confirmation from user
    asking = True
    while asking:
        entered = raw_input('YES/NO> ')
        # User confirmed
        if entered == 'yes':
            print "Alright, you're the boss.",
            sleep(0.75)
            print "Shredding evidence",
            for drama_ellipses in range(3):
                sleep(1)
                print ".",
            # Erase Notes data from user file
            with open(user_file, 'w') as file:
                user_data['notes'] = {}
                json.dump(user_data, file)
            print "all done!"
            asking = False
        # User changed their mind
        elif entered == 'no':
            print "Good call."
            asking = False
        # Invalid input
        else:
            print "Sorry, what? I didn't catch that. Do you want to nuke these notes or not?"
    sleep(1)
    print

def close_note(*args):
    global note_opened
    note_opened = False
    
menu_options = {'new note': new_note,
                'delete all notes': delete_all_notes,
                'quit': quit_notes}
note_options = {'edit': edit_note,
                'rename': rename_note,
                'delete': delete_note,
                'back' : close_note}

def open_note(note_name):
    global note_opened
    note_opened = True
    while note_opened:
        print note_name + ":"
        print user_data['notes'][note_name]
        print "EDIT | RENAME | DELETE | BACK to Menu"
        command = raw_input('NOTE> ')
        if command in note_options:
            note_options[command](note_name)
        print


def notes(active_user):
    """Main module command loop."""
    global run
    load_user(active_user)
    run = True
    while run:
        # If no saved notes, say so
        if len(user_data['notes']) == 0:
            output = """You don't seem to have any saved notes right now.
NEW NOTE | DELETE ALL NOTES | QUIT to Main Menu"""
        # Else build list of notes
        else:
            notes_list = ""
            for note in user_data['notes']:
                notes_list += "[" + note + "]" + "   "
            output = "Your saved notes:\n" + notes_list + \
            "\nNEW NOTE | DELETE ALL NOTES | QUIT to Main Menu"
        print output
        # Command interpretation
        entered = raw_input('NOTES> ')
        # Checks for note title
        if entered.title() in user_data['notes']:
            print
            open_note(entered.title())
        # Checks for menu command
        if entered in menu_options:
            print
            menu_options[entered]()

