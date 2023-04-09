import os
import gspread
import datetime
import re
from tabulate import tabulate

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
booking_num_column = bookings.col_values(1)

# UTILITY FUNCTIONS
def todays_date():
    '''
    Returns todays date formatted as dd-mm-yyyy, which is used to display 
    the current days data for the benefit of the user.
    '''
    today = datetime.date.today()
    today_formatted = today.strftime('%d-%m-%Y')
    return today_formatted


def get_booking_date():
    '''
    Requests a date input in a specific format, to be used for creating, 
    and retrieving bookings
    '''
    date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')

    while True:
        print("Please enter the booking date as: (DD-MM-YYYY)")
        booking_date = input()
        if not date_pattern.match(booking_date):
            print("Invalid date format, please try again.\n The day must be between 1 and 31,\n "
                                 "The month must be between 1 and 12,"
                                 "\nAnd the year must be a four-digit number")
            continue
        try:
            day, month, year = map(int, booking_date.split("-"))
            date = datetime.date(year, month, day)
            if date.month != month or date.day != day:
                raise ValueError("Invalid date, please reenter the correct "
                                 "date.\n The day must be between 1 and 31,\n "
                                 "The month must be between 1 and 12,"
                                 "\nAnd the year must be a four-digit number")
            else:
                return booking_date
            break

        except ValueError as e:
            print(f"Invalid date input: {e}")


def increment_booking_number():
    '''
    Automatically generates and increments a sequential booking number starting with B1001
    '''
    highest_num = 1000

    booking_num_column = bookings.col_values(1)

    for booking_num in booking_num_column:
        match = re.match(r'^B(\d+)$', booking_num)
        if match:
            num = int(match.group(1))
            if num > highest_num:
                highest_num = num

    next_num = highest_num + 1
    return f'B{next_num}' if highest_num != 1000 else 'B1001'


# def count_bookings()
'''
Displays a sum total of the number of displayed bookings
'''
# def revenue_total()
'''
Displays a sum total of the revenue for the displayed bookings
'''

def bookings_counter(values):
    '''
    Displays a total count of displayed bookings
    '''
    count_bookings = sum(isinstance(elem, list) for elem in values)
    print(f'Total Bookings: {count_bookings -1}')

#CRUD FUNCTIONS
# def create_booking()
'''
'''
# def update_booking()
'''
'''
# def delete_booking()
'''
'''
def view_all_bookings():
    '''
    Displays all bookings in the system, 
    '''
    all_bookings = bookings.get_all_values()

    print(tabulate(all_bookings[1:], headers=['Booking No.', 'Date', 'Dogs Name',
                                   'Amount Paid']))
    bookings_counter(all_bookings)
    
# def view_booking_no()
'''
'''
# def view_booking_date()
'''
'''
# def view_dog_bookings()
'''
'''



def start():
    '''
    Starts the program - generates a welcome screen to the user
    '''
    print('*' * 50)
    print("** Welcome to the Doggy Daycare Admin System. **\n")
    print("Press any key + Enter to start the program...")
    input()
    choose_main_menu()


# MENU FUNCTIONS
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
    while True:
        print('Please choose an option from the following:\n')
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search bookings by Date')
        print("[3] - Or, Search bookings by Dog's Name")
        print('[4] - Return to Main menu')
        try:
            delete_menu_choice = int(input())
            if delete_menu_choice not in range(1, 5):
                raise ValueError
            break
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
    while True:
        print('Please choose an option from the following:\n')
        print('[1] - View all bookings')
        print('[2] - View by booking No.')
        print('[3] - View by booking Date')
        print("[4] - View by booking Name")
        print('[5] - Return to Main menu')
        try:
            view_menu_choice = int(input())
            if view_menu_choice not in range(1, 6):
                raise ValueError
            break
        except ValueError:
            print('Invalid input.  Please enter a number between 1 and 5')
    return view_menu_choice


# SUBMENU CHOICE FUNCTIONS
def choose_update_menu():
    '''
    Update menu choice passed to this if else statement which activates 
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
        

def choose_delete_menu():
    '''
    Delete menu choice passed to this if else statement which activates 
    one of the relevant functions
    '''
    delete_menu_choice = delete_bkg_menu()
    while True:
        #to check and complete terminal clear
        # os.system('cls' if os.name == 'nt' else "printf 
        # '\033c'")
        if delete_menu_choice == 1:
            print("Enter a booking number to delete\n")
            break
        elif delete_menu_choice == 2:
            print("Search bookings by date - to delete\n")
            break
        elif delete_menu_choice == 3:
            print("Search bookings by dog's name - to delete\n")
            break
        elif delete_menu_choice == 4:
            print("Return to main menu\n")    
        else:
            print("Invalid choice, please choose between 1 and 4")


def choose_view_menu():
    '''
    View menu choice passed to this if else statement which activates 
    one of the relevant functions
    '''
    view_menu_choice = view_bkg_menu()
    while True:
        #to check and complete terminal clear
        # os.system('cls' if os.name == 'nt' else "printf 
        # '\033c'")
        if view_menu_choice == 1:
            print("View all bookings\n")
            break
        elif view_menu_choice == 2:
            print("View by booking number\n")
            break
        elif view_menu_choice == 3:
            print("View by booking date\n")
            break
        elif view_menu_choice == 4:
            print("View by dog's name\n")
            break
        elif view_menu_choice == 5:
            print("View by dog's name\n")
            break    
        else:
            print("Invalid choice, please choose between 1 and 5")

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
            choose_delete_menu()
            break
        elif main_menu_choice == 4:
            print("View bookings\n")
            choose_view_menu()
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
    #print(todays_date())
    #get_booking_date()
    #print(increment_booking_number())
    view_all_bookings()
    start()
    

test_function_calls()

