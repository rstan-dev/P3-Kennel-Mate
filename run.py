import gspread

from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('p3-kennel-mate-data')

bookings = SHEET.worksheet('bookings-data')
all_bookings = bookings.get_all_values()


def start():
    '''
    Starts the program - generates a welcome screen to the user
    '''
    print('*' * 50)
    print("** Welcome to the Doggy Daycare Admin System. **\n")


def display_main_menu():
    '''
    Displays Main menu of options.  Try statement validates user input 
    for integer between 1 and 5 only
    '''
    print('*' * 50)
    print("Main Menu\n")
    menu_choice = 'x'
    while not menu_choice.isnumeric() or int(menu_choice) not in range(1, 6):
        print('Please choose an option from the following:\n')
        print('[1] - Create A Booking')
        print('[2] - Update A Booking')
        print('[3] - Delete A Booking')
        print('[4] - View Bookings')
        print('[5] - Exit')
        try:
            main_menu_choice = int(input())
            if main_menu_choice not in range(1, 6):
                raise ValueError
        except ValueError:
            print('Invalid input.  Please enter a number between 1 and 5')
    return main_menu_choice


def update_bkg_menu():
    '''
    Displays Main menu of options.  Try statement validates user input 
    for integer between 1 and 5 only
    '''
    print('*' * 22)
    print("Update a Booking Menu\n")
    print('*' * 22)
    print("To update a booking, you will need the Booking Number\n")
    menu_choice = 'x'
    while not menu_choice.isnumeric() or int(menu_choice) not in range(1, 6):
        print('Please choose an option from the following:\n')
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search bookings by Date')
        print("[3] - Or, Search bookings by Dog's Name")
        print('[4] - Return to Main menu')
        menu_choice = input()

    return int(menu_choice)






def test_function_calls():
    '''
    A place to keep all test function calls during the build process.
    Delete when project is completed
    '''
    print(all_bookings)
    start()
    display_main_menu()


test_function_calls()

