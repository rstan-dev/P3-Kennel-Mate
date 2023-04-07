import gspread
import os

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
    print("Press any key + Enter to start the program...")
    input()
    choose_main_menu()



def display_main_menu():
    '''
    Displays Main menu of options. Try statement validates user input for 
    number between 1 and 5 only
    '''
    print('*' * 50)
    print("Main Menu\n")
    menu_choice = 'x'
    while True:
        print('Please choose an option from the following:\n')
        print('[1] - Create A Booking')
        print('[2] - Update A Booking')
        print('[3] - Delete A Booking')
        print('[4] - View Bookings')
        print('[5] - Exit')
        try:
            menu_choice = int(input())
            if menu_choice not in range(1, 6):
                raise ValueError
            break
        except ValueError:
            print('Invalid input.  Please enter a number between 1 and 5')
    return menu_choice


def update_bkg_menu():
    '''
    Displays Update booking menu options. Try statement validates user input for 
    number between 1 and 4 only
    '''
    print('*' * 22)
    print("Update a Booking Menu\n")
    print('*' * 22)
    print("To update a booking, you will need the Booking Number\n")
    menu_choice = 'x'
    while True:
        print('Please choose an option from the following:\n')
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search bookings by Date')
        print("[3] - Or, Search bookings by Dog's Name")
        print('[4] - Return to Main menu')
        try:
            update_menu_choice = int(input())
            if update_menu_choice not in range(1, 5):
                raise ValueError
            break
        except ValueError:
            print('Invalid input. Please enter a number between 1 and 4')
    return update_menu_choice



def delete_bkg_menu():
    '''
    Displays Delete menu options. Try statement validates user input for 
    number between 1 and 4 only
    '''
    print('*' * 22)
    print("Delete a Booking Menu\n")
    print('*' * 22)
    menu_choice = 'x'
    while not menu_choice.isnumeric() or int(menu_choice) not in range(1, 5):
        print('Please choose an option from the following:\n')
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search bookings by Date')
        print("[3] - Or, Search bookings by Dog's Name")
        print('[4] - Return to Main menu')
        try:
            delete_menu_choice = int(input())
            if delete_menu_choice not in range(1, 5):
                raise ValueError
        except ValueError:
            print('Invalid input.  Please enter a number between 1 and 4')
    return delete_menu_choice


def view_bkg_menu():
    '''
    Displays View bookings menu of options. Try statement validates user input for 
    number between 1 and 4 only
    '''
    print('*' * 22)
    print("View a Booking Menu\n")
    print('*' * 22)
    menu_choice = 'x'
    while not menu_choice.isnumeric() or int(menu_choice) not in range(1, 6):
        print('Please choose an option from the following:\n')
        print('[1] - View All Bookings')
        print('[2] - Search by Booking No.')
        print('[3] - Or, Search bookings by Date')
        print("[4] - Or, Search bookings by Dog's Name")
        print('[5] - Return to Main menu')
        try:
            delete_menu_choice = int(input())
            if delete_menu_choice not in range(1, 6):
                raise ValueError
        except ValueError:
            print('Invalid input.  Please enter a number between 1 and 6')
    return delete_menu_choice


def choose_update_menu():
    '''
    Main menu choice passed to this if else statement which activates 
    one of the relevant functions
    '''
    update_menu_choice = update_bkg_menu()
    while True:
        #to check and complete terminal clear
        # os.system('cls' if os.name == 'nt' else "printf 
        # '\033c'")
        if update_menu_choice == 1:
            print("Enter a booking number\n")
            break
        elif update_menu_choice == 2:
            print("Search bookings by date\n")
            break
        elif update_menu_choice == 3:
            print("Search bookings by dog's name\n")
            break
        elif update_menu_choice == 4:
            print("Return to main menu\n")    
        else:
            print("Invalid choice, please choose between 1 and 4")
        


def choose_main_menu():
    '''
    Main menu choice passed to this if else statement which activates 
    one of the relevant functions
    '''
    main_menu_choice = display_main_menu()
    while True:
        #to check and complete terminal clear
        # os.system('cls' if os.name == 'nt' else "printf 
        # '\033c'")
        if main_menu_choice == 1:
            print("Create a new booking\n")
            break
        elif main_menu_choice == 2:
            print("Update a booking\n")
            choose_update_menu()
            break 
        elif main_menu_choice == 3:
            print("Delete a booking\n")
            break
        elif main_menu_choice == 4:
            print("View bookings\n")
            break       
        elif main_menu_choice == 5:
            print("Exit\n")
            start()      
        else:
            print("Invalid choice, please choose between 1 and 5")
        main_menu_choice = display_main_menu()



print("______________Test Area (to be deleted)___________________")
def test_function_calls():
    '''
    A place to keep all test function calls during the build process.
    Delete when project is completed
    '''
    # print(all_bookings)
    # start()
    # while True:
    #     main_menu_choice = display_main_menu()
    #     choose_main_menu(main_menu_choice)
    #     if main_menu_choice == 5:
    #     # Exit the program
    #         break
    # main_menu_choice = display_main_menu()
    # # print(main_menu_choice)
    # choose_main_menu(main_menu_choice)
    # update_bkg_menu()
    # delete_bkg_menu()
    # view_bkg_menu()
    start()
    

test_function_calls()

