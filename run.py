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


def revenue_total(values):
    '''
    Displays a sum total of the revenue for the displayed bookings
    '''
    pattern = re.compile(r"\d+.\d{2}")
    revenue_list = []
    total = 0

    for value in values:
        match = pattern.findall(value[4])
        if match:
            revenue = float(match[0])
            revenue_list.append(revenue)
            total += revenue

    print(f"Total Revenue: £{total:.2f}")


def bookings_counter(values):
    '''
    Displays a total count of displayed bookings
    '''
    count_bookings = sum(isinstance(elem, list) for elem in values)
    print(f'Total Bookings: {count_bookings}')

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
    Displays all bookings in the system, with a count of total booking sand sum of revenue, and displays a message if there is no booking data - based on if a booking number is present
    '''
    all_bookings = bookings.get_all_values()
    bookings_B1000_or_higher = []

    for row in all_bookings:
        if any('B' + str(i).zfill(4) in value for i, value in enumerate(row)):
            bookings_B1000_or_higher.append(row)

    if not bookings_B1000_or_higher:
        print(
            tabulate(
                bookings_B1000_or_higher,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']
                )
            )
        print("No booking data to display")
    else:
        print(
            tabulate(
                bookings_B1000_or_higher,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']
                )
            )
        bookings_counter(bookings_B1000_or_higher)
        revenue_total(bookings_B1000_or_higher)


def view_booking_no(booking_num):
    '''
    Displays all bookings in the system by Booking No., with a count of total
        bookings and a sum of total revenue
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_booking_num = []

    for row in all_bookings:
        if ('B' + str(booking_num)) in row:
            rows_containing_booking_num.append(row)

    if not rows_containing_booking_num:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid'])
            )
        print("No booking data to display")

    else:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid']))

        bookings_counter(rows_containing_booking_num)
        revenue_total(rows_containing_booking_num)


def view_booking_date(booking_date):
    '''
    Displays all bookings in the system by Date, with a count of total
        bookings and a sum of total revenue
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_booking_date = []
    no_booking_data = True

    for row in all_bookings:
        if booking_date in row:
            rows_containing_booking_date.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(
            rows_containing_booking_date,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid']))
        print("No booking data to display for this date")
    else:
        print(tabulate(
            rows_containing_booking_date,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid']))

        bookings_counter(rows_containing_booking_date)
        revenue_total(rows_containing_booking_date)



def view_dog_bookings(dogs_name):
    '''
    Displays all bookings in the system by Dogs name, either by first name or last name,
    with a count of total bookings and a sum of total revenue
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_dog = []

    for row in all_bookings:
        if dogs_name in row:
            rows_containing_dog.append(row)

    if not rows_containing_dog:
        print(tabulate(
        rows_containing_dog,
        headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid']))
        print("No booking data to display")
    else:
        print(tabulate(
        rows_containing_dog,
        headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name', 'Amount Paid']))

        bookings_counter(rows_containing_dog)
        revenue_total(rows_containing_dog)


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
            view_all_bookings()
            choose_view_menu()
            break
        elif view_menu_choice == 2:
            print("View by booking number\n")
            print("Enter Booking Number digits only...\n")
            booking_num = int(input())
            print(f"collecting booking data...\n")
            view_booking_no(booking_num)
            choose_view_menu()
            break
        elif view_menu_choice == 3:
            print("View by booking date\n")
            print("Enter date DD-MM-YYYY")
            input_date = input()
            view_booking_date(input_date)
            choose_view_menu()
            break
        elif view_menu_choice == 4:
            print("View by dog's name\n")
            print("Enter the Dog's name")
            dogs_name = input().title()
            view_dog_bookings(dogs_name)
            choose_view_menu()
            break
        elif view_menu_choice == 5:
            print("Return to Main menu\n")
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
    #view_all_bookings()
    #view_booking_no()
    # print("Enter date DD-MM-YYYY")
    # input_date = input()
    # view_booking_date(input_date)
    print("Enter the Dog's name")
    dogs_name = input().title()
    view_dog_bookings(dogs_name)
    start()


test_function_calls()

