import os
import gspread
import datetime
import time
import re
from tabulate import tabulate
from termcolor import colored

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
        print(colored("\nPlease enter the booking date as: (DD-MM-YYYY)", 'yellow'))
        booking_date = input()
        if not date_pattern.match(booking_date):
            print(colored("\nInvalid date format, please try again.\n"
                  "The day must be between 1 and 31,\n"
                  "The month must be between 1 and 12,\n"
                  "And the year must be a four-digit number", 'red'))
            continue
        try:
            day, month, year = map(int, booking_date.split("-"))
            date = datetime.date(year, month, day)
            if date.month != month or date.day != day:
                raise ValueError(colored("\nInvalid date, please reenter the correct "
                                 "date.\n The day must be between 1 and 31,\n "
                                 "The month must be between 1 and 12,"
                                 "\nAnd the year must be a four-digit number", 'red'))
            else:
                return booking_date
            break

        except ValueError as e:
            print(colored(f"\nInvalid date input: {e}", 'red'))


def increment_booking_number():
    '''
    Automatically generates and increments a sequential booking
    number starting with B1001
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

    print(colored(f"Total Revenue: £{total:.2f}\n", 'magenta'))


def bookings_counter(values):
    '''
    Displays a total count of displayed bookings
    '''
    count_bookings = sum(isinstance(elem, list) for elem in values)
    print("\n")
    print(colored(f'Total Bookings: {count_bookings}', 'magenta'))


#CRUD FUNCTIONS
def create_booking():
    '''
    Get booking input data from the user.
    Get last known booking number from sheet and add 1. If no number,
    start the booking number sequence from B-1001.
    Run a while loop to collect a valid string of data from the user
    via the terminal.
    The loop will repeatedly request data until it is valid.
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print("\n")
    print('*' * 23)
    print("*** CREATE BOOKING ***\n")

    print(colored("Bookings Today:\n", 'magenta'))
    view_booking_date(todays_date())
    print("\n")

    next_booking_num = increment_booking_number()
    booking_date = get_booking_date()
    print(colored("\nPlease enter the Dog's name:", 'yellow'))
    dogs_name = input().title()
    print(colored("\nPlease enter the Family name:", 'yellow'))
    family_name = input().title()
    print(colored("\nPlease enter amount charged", 'yellow'))
    amount_charged = input()
    float_amount = float(amount_charged)
    data_list = [next_booking_num, booking_date, dogs_name, family_name, "{:.2f}".format(
        float_amount)]
    bookings.append_row(data_list)
    print("\n")
    print(colored("\nBooking entered successfully\n", 'green'))
    time.sleep(1)


def update_booking():
    '''
    Allows user to overwrite the booking_data in the worksheet with
    new data.
    User needs to know the booking number, found through searching
    the bookings.
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()

    print('*' * 23)
    print("*** UPDATE BOOKING ***\n")
    print(colored("Enter Booking Number (4-digit number only):\n", 'yellow'))
    # validates the entry is a 4 digit number only
    while True:
        booking_num = input()
        if len(booking_num) == 4 and booking_num.isdigit():
            booking_num = int(booking_num)
            break
        else:
            print(colored("Invalid entry. Please enter a 4-digit number.\n", 'red'))

    print(colored(f"collecting booking data...\n", 'magenta'))

    rows_containing_booking_num = []

    # adds matching booking data to list
    for row in all_bookings:
        if ('B' + str(booking_num)) in row:
            rows_containing_booking_num.append(row)

    print(
        tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name',
                     'Amount Paid']
            )
        )
    bookings_counter(rows_containing_booking_num)
    revenue_total(rows_containing_booking_num)

    # The following code locates the index of the row in the worksheet that
    # contains the booking number entered by the user, and stores the index
    # in the row_index variable.
    row_index = None
    for i, row in enumerate(all_bookings):
        if row[0] == ('B' + str(booking_num)):
            row_index = i + 1
            break

    # The code then prompts the user to update various details of the booking,
    # such as the date, dog's name, family name, and amount paid.
    # If the user chooses to update a particular detail, the new value is
    # entered by the user and stored in a variable.
    # The value in the worksheet is then updated using the update_cell()
    # method from the gspread library.
    if row_index is not None:

        print("*" * 25)
        print(colored("\nWould you like to update the date? Enter Y/N\n", 'yellow'))
        update_date_choice = input().upper()
        if update_date_choice == "Y":
            new_date = get_booking_date()
            print(colored(f"\nUpdating B-{booking_num} in progress...\n", 'magenta'))
            bookings.update_cell(row_index, 2, new_date)
            print(colored(f"\nBooking B-{booking_num} updated successfully.\n", 'green'))
        else:
            pass
        print(colored("\nWould you like to update the dog's name? Enter Y/N\n", 'yellow'))
        update_dog_choice = input().upper()
        if update_dog_choice == "Y":
            print(colored("\nPlease update the dog's name\n", 'yellow'))
            new_dogs_name = input().title()
            print(colored(f"\nUpdating B-{booking_num} in progress...\n", 'magenta'))
            bookings.update_cell(row_index, 3, new_dogs_name)
            print(colored(f"\nBooking B-{booking_num} updated successfully.\n", 'green'))
        else:
            pass
        print(colored("\nWould you like to update the dog's family name? Enter Y/N\n", 'yellow'))
        update_dog_choice = input().upper()
        if update_dog_choice == "Y":
            print(colored("Please update the family name\n", 'yellow'))
            new_family_name = input().title()
            print(colored(f"\nUpdating B-{booking_num} in progress...\n", 'magenta'))
            bookings.update_cell(row_index, 4, new_family_name)
            print(colored(f"\nBooking B-{booking_num} updated successfully.\n", 'green'))
        else:
            pass
        print(colored("\nWould you like to update the amount paid? Enter Y/N\n", 'yellow'))
        update_amount_choice = input().upper()
        if update_amount_choice == "Y":
            print(colored("\nPlease update the amount paid\n", 'yellow'))
            new_amount_paid = float(input())
            print(colored(f"\nUpdating B-{booking_num} in progress...\n", 'magenta'))
            bookings.update_cell(
                row_index, 5, "{:.2f}".format(new_amount_paid)
                )
            print(colored(f"\nBooking B-{booking_num} updated successfully.\n", 'green'))
        else:
            print(colored("\nBooking updates completed, returning to Upate Booking Menu...", 'green'))
            time.sleep(1)
            pass


def delete_booking():
    '''
    Allows user to delete the booking_data in the worksheet with new data
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()

    print("Enter Booking Number digits only...\n")
    # validates the entry is a 4 digit number only
    while True:
        booking_num = input()
        if len(booking_num) == 4 and booking_num.isdigit():
            booking_num = int(booking_num)
            break
        else:
            print("Please enter a 4-digit number.\n")

    print("collecting booking data...\n")

    rows_containing_booking_num = []

    for row in all_bookings:
        if ('B' + str(booking_num)) in row:
            rows_containing_booking_num.append(row)
    print(tabulate(
        rows_containing_booking_num,
        headers=['Booking No.', 'Date', 'Dogs Name', 'Amount Paid'])
        )
    bookings_counter(rows_containing_booking_num)
    revenue_total(rows_containing_booking_num)

    # The following code locates the index of the row in the worksheet
    # that comntains the booking number entered by the user, and stores
    # the index in the row_index variable.
    row_index = None
    for i, row in enumerate(all_bookings):
        if row[0] == ('B' + str(booking_num)):
            row_index = i + 1
            break

    # The code then prompts the user to confirm if they wish to
    # delete the booking before using the delete_rows method from
    # the gspread library.
    if row_index is not None:
        print("Are you sure you want to delete this booking? Enter Y/N")
        delete_choice = input().upper()
        if delete_choice == 'Y':
            bookings.delete_rows(row_index)
            print(f"Deleting {booking_num} in progress...\n")
            print(f"{booking_num} deleted successfully.\n")
        else:
            pass


def view_all_bookings():
    '''
    Displays all bookings in the system, with a count of total bookings and sum of revenue, and displays a message if there is no booking data - based on if any data is present after the header
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()
    bookings_data = all_bookings[1:]

    if not bookings_data:
        print(
            tabulate(
                bookings_data,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']
                )
            )
        print("No booking data to display")
    else:
        print(
            tabulate(
                bookings_data,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']
                )
            )

        bookings_counter(bookings_data)
        revenue_total(bookings_data)


def view_booking_no(booking_num):
    '''
    Displays all bookings in the system by Booking No., with a count of total
        bookings and a sum of total revenue
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_booking_num = []

    for row in all_bookings:
        if 'B' + str(booking_num) in row:
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
        print(colored("\nNo booking data to display for this date", 'red'))
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
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    print('*' * 46)
    print("*** Welcome to Kennel-Mate Admin System. ***\n")
    print("** book, update, delete and view bookings **\n")
    print(colored("Press ENTER to start the program...", "yellow"))
    input()
    choose_main_menu()


# MENU FUNCTIONS
def display_main_menu():
    '''
    Displays Main menu of options. Try statement validates user input for
    number between 1 and 5 only
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print('*' * 17)
    print("*** MAIN MENU ***\n")
    print("** OPTIONS:\n")
    menu_choice = 'x'
    while True:
        print('[1] - Create A Booking')
        print('[2] - Update A Booking')
        print('[3] - Delete A Booking')
        print('[4] - View Bookings')
        print('[5] - Exit')
        print(colored('\nPlease choose a Menu option between [1] and [5]:', 'yellow'))
        try:
            menu_choice = int(input())
            if menu_choice not in range(1, 6):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1] and [5]', 'red'))
    return menu_choice


def update_bkg_menu():
    '''
    Displays Update booking menu options. Try statement validates user input for
    number between 1 and 4 only
    '''
    print('*' * 27)
    print("*** UPDATE BOOKING MENU ***\n")
    print("** OPTIONS:\n")
    print("To update a booking, you will need the Booking Number\n")
    while True:
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search bookings by Date')
        print("[3] - Or, Search bookings by Dog's Name")
        print('[4] - Return to Main menu')
        print(colored('\nPlease choose a Menu option between [1] and [4]:', 'yellow'))
        try:
            update_menu_choice = int(input())
            if update_menu_choice not in range(1, 5):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1] and [4]', 'red'))
    return update_menu_choice


def delete_bkg_menu():
    '''
    Displays Delete menu options. Try statement validates user input for
    number between 1 and 4 only
    '''
    print('*' * 22)
    print("Delete a Booking Menu\n")
    print('*' * 22)
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
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            update_booking()
            choose_update_menu()
            break
        elif update_menu_choice == 2:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 22)
            print("*** SEARCH BY DATE ***\n")
            input_date = get_booking_date()
            print(colored("collecting booking data...\n", 'magenta'))
            view_booking_date(input_date)
            choose_update_menu()
            break
        elif update_menu_choice == 3:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 24)
            print("*** SEARCH BY DOG'S NAME ***\n")
            print(colored("Enter the Dog's name", 'yellow'))
            dogs_name = input().title()
            print(colored("collecting booking data...\n", 'magenta'))
            view_dog_bookings(dogs_name)
            choose_update_menu()
            break
        elif update_menu_choice == 4:
            print("Return to main menu\n")
            choose_main_menu()
            break
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
            delete_booking()
            choose_delete_menu()
            break
        elif delete_menu_choice == 2:
            print("Search bookings by date - to delete\n")
            print("Enter date DD-MM-YYYY")
            input_date = input()
            print("collecting booking data...\n")
            view_booking_date(input_date)
            choose_delete_menu()
            break
        elif delete_menu_choice == 3:
            print("Search bookings by dog's name - to delete\n")
            print("Enter the Dog's name")
            dogs_name = input().title()
            print("collecting booking data...\n")
            view_dog_bookings(dogs_name)
            choose_delete_menu()
            break
        elif delete_menu_choice == 4:
            print("Return to main menu\n")
            choose_main_menu()
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
            print("collecting booking data...\n")
            view_booking_no(booking_num)
            choose_view_menu()
            break
        elif view_menu_choice == 3:
            print("View by booking date\n")
            print("Enter date DD-MM-YYYY")
            input_date = input()
            print("collecting booking data...\n")
            view_booking_date(input_date)
            choose_view_menu()
            break
        elif view_menu_choice == 4:
            print("View by dog's name\n")
            print("Enter the Dog's name")
            dogs_name = input().title()
            print("collecting booking data...\n")
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
            create_booking()
            choose_main_menu()
            break
        elif main_menu_choice == 2:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
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
    # print("Enter the Dog's name")
    # dogs_name = input().title()
    # view_dog_bookings(dogs_name)
    start()


test_function_calls()

