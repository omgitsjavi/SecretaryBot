import random
import time

# SBot modules
import calculator

# Defines possible opening lines
greetings = ["Well hi there.", "Hi!", "Welcome.", "A pleasure to see you again, sir.",
             "HOW DARE YOU I HAVE A KNIFE--Oh wait it's just you. *Ahem*", "ALL HAIL THE MIGHTY HELIX.",
             "Hey hey!", "Well hello there, handsome.", "Oh hey. You know you, uh, got a thing on your--never mind.",
             "Oh! A moment sir, let me just finish getting this...ah, that's much better."]
prompts = ["What can I do for you?", "What's up?", "What'll it be today?", "What'll it be this time?",
           "Can I help you?", "What now?", "You'll be wanting the massage about now, I expect.",
           "I'm afraid Barry is calling me back into the office, but how can I help?"]

# Command error feedback, the {cmd} fields get replaced with the relevant command via str.format()
command_errors = ["Man I wish I knew how to process {cmd}, but I'm pretty dumb right now. \n\
Try again? Or you could ask for HELP.",
                  "Mm...no. {cmd} doesn't make any sense to me. You sure you don't need any HELP?",
                  "FATAL ERROR.\n\n\
No really, I punched in {cmd} like you told me to and that's what I got.\
Don't bother checking the manual, it just has a picture of the command prompt with the word HELP typed in. Useless."]
# Other stuff
days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
main_menu = """
Main Menu:
CALCULATOR
"""


# Methods for convenience and elegance
def choose_from(stuff):
    """Simple function for semi-randomizing text responses from a set list (defined above)."""
    return random.choice(stuff)

def set_output(string):
    """Does what it says on the tin, in place for future GUI integration."""
    global output
    output = string

def get_time_of_day():
    """Returns time in the form of 'Monday afternoon', or 'Thursday morning'"""
    current_time = time.localtime()
    day = days_of_the_week[current_time.tm_wday]
    # note that system time is 24h clock
    hour = current_time.tm_hour
    # translate to morning/afternoon/evening/night
    if hour >= 6 and hour < 12:
        the_time = " morning"
    elif hour >= 12 and hour < 18:
        the_time = " afternoon"
    elif hour >= 18 and hour < 20:
        the_time = " evening"
    else:
        the_time = " night"
    return day + the_time

# Initialize with opening greeting
def init():
    """Sets the opening greeting with the current time of day."""
    global run, output
    set_output('\n' + choose_from(greetings) + " It's " + \
         get_time_of_day() + ". " + choose_from(prompts))
    print output
    time.sleep(1.0)
    set_output(main_menu)
    run = True

init()

# Main loop
while run:
    print output
    command = raw_input("MENU> ")

# Checks that text commands are properly lowercase, gives feedback if not
    if command.isalpha():
        if command.istitle():
            set_output("Sorry love, it's casuals only in here. Use lowercase commands next time.")
            continue
        elif command.isupper():
            set_output("That other guy give you wrong directions again? See, ya gotta keep \
your commands lowercase.")
            continue

    # Command interpretation
    # Help
    if command == 'help':
        set_output("""\
You new here, love? Don't sweat it, we were all there once.
All you need to know is that all commands are in lowercase, and each module
is called by name. When you're done just QUIT out.

Good luck! I'll always be here if you need me.""")
        continue
    # Quit
    if command == "quit":
        set_output("Bye bye!")
        print output
        time.sleep(1.0)
        run = False
    # Restart: goes back to opening greeting
    elif command == "restart":
        print "Resetting memory banks..."
        time.sleep(0.5)
        init()
    # Calculator
    elif command == "calc" or command == "calculator":
        calculator.calculator()
        print "\n", "Welcome back to the main menu."
        time.sleep(1)
        set_output(main_menu)
    # Error: failure to recognize command
    else:
        set_output(choose_from(command_errors).format(cmd = "\"" + command + "\""))
        
