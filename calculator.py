# Simple calculator module

# init
def calculator():
    output = "\nWelcome to the calculator. QUIT at any time."
    run = True
    while run:
        print output
    
        entered = raw_input('Calc> ')
        if entered == "quit":
            run = False
        else:
            output = eval(entered)

