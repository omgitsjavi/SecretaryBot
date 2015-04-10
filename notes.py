"""Notes module, used by user for storing miscellaneous bits of information."""
import json
from time import sleep

help_text = """The Notes module saves any piece of information you might want to 
recall later. Each note is saved with a label and can be edited freely.
To read or edit a note, enter its name at the main menu. All entries are case-
sensitive."""

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
    print "Welcome to Notes!", '\n', help_text
    sleep(2.0)

def load_user(active_user):
    """Loads active user's save data."""
    global user_file, user_data
    user_file = active_user.name + ".txt"
    with open(user_file, 'r') as file:
        user_data = json.load(file)
    # If no Notes data, update profile
    if "notes" not in user_data:
        init_notes_data(active_user)

def quit_notes():
    global run
    run = False

def new_note():
    """Creates a new note based on user input."""
    print "What do you want to save?"
    note_contents = raw_input('Note contents> ')
    print "And what shall I file it under, luv?"
    note_label = raw_input('Note label> ')
    # Save to file
    with open(user_file, 'w') as file:
        user_data['notes'][note_label] = note_contents
        json.dump(user_data, file)

# TODO
def edit_note(note):
    pass
def rename_note(note):
    pass
def delete_note(note):
    pass
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
    
menu_options = {'new note': new_note,
                'delete all notes': delete_all_notes,
                'quit': quit_notes}
note_options = {'edit': edit_note,
                'rename': rename_note,
                'delete': delete_note}


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
        menu_options[entered]()
