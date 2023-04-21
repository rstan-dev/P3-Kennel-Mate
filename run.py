# IMPORTS
'''
The following libraries are needed to clear the screen,
handling date functions, regular exporessions, presenting
data in a table format on screen, and displaying colors for
onscreen messages
'''
import os
import datetime
import time
import re
import gspread
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


# UTILITY FUNCTIONS

def todays_date():
    '''
    Returns todays date formatted as dd-mm-yyyy, which is used to display
    the current days data for the benefit of the user.

    Returns:
    str: A string representing today's date in the format "dd-mm-yyyy".
    '''
    today = datetime.date.today()
    today_formatted = today.strftime('%d-%m-%Y')
    return today_formatted


def get_booking_date():
    '''
    Prompts the user to enter a date in the format "DD-MM-YYYY", validates the
    input, and returns it.

    Returns:
    str: A string representing the booking date in the format "DD-MM-YYYY".

    Raises:
    ValueError: If the input is not a valid date in the format "DD-MM-YYYY".
    '''
    date_pattern = re.compile(r'^\d{2}-\d{2}-\d{4}$')

    while True:
        print(colored("\nPlease enter the booking date as: (DD-MM-YYYY)",
                      'yellow'))
        booking_date = input()
        if not date_pattern.match(booking_date):
            print(colored("\nInvalid date format, please try again as "
                          "DD-MM-YYY.\n"
                          "The day must be between 1 and 31,\n"
                          "The month must be between 1 and 12,\n"
                          "And the year must be a four-digit number\n", 'red'))
            continue
        try:
            day, month, year = map(int, booking_date.split("-"))
            date = datetime.date(year, month, day)
            if date.month != month or date.day != day:
                raise ValueError(colored("\nInvalid date format, "
                                         "please try again as DD-MM-YYY.\n"
                                         "The day must be between 1 and 31,\n"
                                         "The month must be between 1 and 12,"
                                         "\nAnd the year must be a four-digit"
                                         "number\n", 'red'))
            return booking_date

        except ValueError as e:
            print(colored(f"\nInvalid date input: {e}\n", 'red'))


def increment_booking_number():
    '''
    Automatically generates and increments a sequential booking
    number starting with B1001.

    Searches through the existing booking numbers in the first column of the
    bookings sheet and finds the highest number that matches the pattern
    "B<digits>". The function then increments that number by 1 to generate
    the next booking number.

    Returns:
    str: A string representing the next booking number in the format "Bxxxx",
    where "xxxx" is a sequence of four digits.
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
    Calculates the total revenue for a list of bookings and displays it on the
    screen.

    The function takes a list of booking data, which should include the amount
    charged for each booking in the format "£xxx.xx". It then extracts the
    revenue values, calculates the sum of all revenues, and displays the result
    on the screen in the format "Total Revenue: £xxx.xx".

    Args:
    values (list): A list of booking data, from google sheets, where each item
    is a list containing booking details including amount charged in the
    format "£xxx.xx".

    Returns:
    None

    Displays:
    Total Revenue on screen.
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
    Counts the number of bookings in a list of bookings and displays the total
    count.

    Args:
    values (list): A list of bookings.

    Returns:
    None

    Displays:
    The total number of bookings in the given list.
    '''
    count_bookings = sum(isinstance(elem, list) for elem in values)
    print("\n")
    print(colored(f'Total Bookings: {count_bookings}', 'magenta'))


def get_dogs_name():
    '''
    Prompts the user to enter the dog's name and returns it without any
    leading or trailing white spaces.

    Returns:
    str: The dog's name without any leading or trailing white spaces.

    Raises:
    ValueError: If the user enters an empty string or a string containing
    only white spaces.
    '''
    while True:
        dogs_name = input(
            colored("\nPlease enter the Dog's name:\n", 'yellow')
            ).strip().title()
        if not dogs_name:
            print(
                colored(
                    "Error: Dog's name cannot be empty or contain\n"
                    "only white spaces. Please try again.", 'red'
                    )
                )
        else:
            break
    return dogs_name


# CRUD FUNCTIONS

def create_booking():
    '''
    Prompts the user to input booking data and adds it to the bookings sheet.

    This function obtains the last known booking number from the sheet, adds
    1 to it, and uses it as the next booking number. If no booking numbers are
    present in the sheet, the function starts the booking number sequence from
    B-1001.

    The function then prompts the user to input the booking date, dog's name,
    family name, and amount charged. It ensures that the user provides valid
    input for each field before adding the booking data to the sheet.

    Raises:
    ValueError: If the user inputs an invalid amount charged, which must be
    either a whole number or a number with two decimal places.
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

    # checks if the Dog's name input is empty or contains only
    # white spaces
    while True:
        dogs_name = input(colored("\nPlease enter the Dog's name:\n",
                                  'yellow')).strip().title()

        if not dogs_name:
            print(colored("Error: Dog's name cannot be empty or contain\n"
                          "only white spaces. Please try again.", 'red'))
        else:
            break

    # checks if the Dog's Family name input is empty or contains
    # only white spaces
    while True:
        family_name = input(colored("\nPlease enter the Dog's Family name:\n",
                                    'yellow')).strip().title()
        if not family_name:
            print(colored("Error: Family name cannot be empty or contain\n"
                          "only white spaces. Please try again.", 'red'))
        else:
            break

    # checks if the amount charged input is a valid number
    while True:
        amount_charged = input(colored("\nPlease enter amount charged:\n",
                                       'yellow'))
        float_amount = float(amount_charged)
        try:
            if not float_amount.is_integer() and \
                    round(float_amount, 2) != float_amount:
                raise ValueError

        except ValueError:
            print(colored("Invalid Input: Amount charged must be a whole"
                          "number\n"
                          "or a number with 2 decimal places. Please try"
                          "again.", 'red'))
        else:
            break

    data_list = [next_booking_num, booking_date, dogs_name, family_name,
                 "{:.2f}".format(float_amount)]
    bookings.append_row(data_list)
    print("\n")
    print(colored("\nBooking entered successfully\n", 'green'))
    time.sleep(1)


def update_booking():
    '''
    Allows the user to update the booking data in the worksheet with new data.
    Prompts the user for the booking number they wish to update, searches for
    the corresponding row in the worksheet and updates the row with the new
    data.

    Returns:
        None
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()

    # Prompts user to enter a booking number to update
    print('*' * 23)
    print("*** UPDATE BOOKING ***\n")
    print(colored("Enter Booking Number (4-digit number only):\n", 'yellow'))

    # Validates the entry is a 4 digit number only
    while True:
        booking_num = input()
        if len(booking_num) == 4 and booking_num.isdigit():
            booking_num = int(booking_num)
            break
        else:
            print(colored("Invalid entry. Please enter a 4-digit number:\n",
                          'red'))

    print(colored("Collecting booking data...\n", 'magenta'))

    rows_containing_booking_num = []
    no_booking_data = True

    # Searches for the row containing the booking number,
    # or displays a message if there is no data to display.
    for row in all_bookings:
        if 'B' + str(booking_num) in row:
            rows_containing_booking_num.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(rows_containing_booking_num,
                       headers=['Booking No.', 'Date', 'Dogs Name',
                                'Family Name', 'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))
    else:
        print(tabulate(rows_containing_booking_num,
                       headers=['Booking No.', 'Date', 'Dogs Name',
                                'Family Name', 'Amount Paid']))

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

    # Prompts the user to update various details of the booking,
    # such as the date, dog's name, family name, and amount paid.
    # If the user chooses to update a particular detail, the new value is
    # entered by the user and stored in a variable.
    # The value in the worksheet is then updated using the update_cell()
    # method from the gspread library.
    if row_index is not None:

        # Prompts user to update the booking date
        print("*" * 25)
        print(colored("\nWould you like to update the date? Enter Y/N:",
                      'yellow'))

        # Validates Y/N for updating the date
        while True:
            update_date_choice = input().upper()
            if update_date_choice == "Y" or update_date_choice == "N":
                break
            else:
                print(colored("Invalid input. Please enter Y or N\n", 'red'))

        if update_date_choice == "Y":
            new_date = get_booking_date()
            print(colored(f"\nUpdating B-{booking_num} in progress...\n",
                          'magenta'))
            bookings.update_cell(row_index, 2, new_date)
            print(colored(f"\nBooking B-{booking_num} updated successfully.\n",
                          'green'))
        else:
            pass

        # Prompts user to update the dog's name
        print(colored("\nWould you like to update the Dog's name? Enter Y/N:",
                      'yellow'))

        # validates Y/N for updating the dog's name
        while True:
            update_dog_choice = input().upper()
            if update_dog_choice == "Y" or update_dog_choice == "N":
                break
            else:
                print(colored("Invalid input. Please enter Y or N\n", 'red'))

        if update_dog_choice == "Y":
            while True:
                new_dogs_name = input(colored("\nPlease update the Dog's "
                                              "name:\n",
                                              'yellow')).strip().title()
                if not new_dogs_name:
                    print(colored("Error: Dog's name cannot be empty or"
                                  "contain\n only white spaces. Please try"
                                  "again.", 'red'))
                else:
                    print(colored(f"\nUpdating B-{booking_num} in "
                                  "progress...\n", 'magenta'))
                    bookings.update_cell(row_index, 3, new_dogs_name)
                    print(colored(f"\nBooking B-{booking_num} updated "
                                  "successfully.\n", 'green'))
                    break
        else:
            pass

        # Prompts user to update the dog's family name
        print(colored("\nWould you like to update the Dog's Family name? "
                      "Enter Y/N:", 'yellow'))

        # Validates Y/N for updating the dog's family name
        while True:
            update_family_choice = input().upper()
            if update_family_choice == "Y" or update_family_choice == "N":
                break
            else:
                print(colored("Invalid input. Please enter Y or N\n", 'red'))

        if update_family_choice == "Y":
            while True:
                new_family_name = input(colored("\nPlease update the Dog's "
                                                "Family name\n:",
                                                'yellow')).strip().title()
                if not new_family_name:
                    print(colored("Error: Family name cannot be empty or "
                                  "contain\nonly white spaces. "
                                  "Please try again.", 'red'))
                else:
                    print(colored(f"\nUpdating B-{booking_num} in "
                                  "progress...\n", 'magenta'))
                    bookings.update_cell(row_index, 4, new_family_name)
                    print(colored(f"\nBooking B-{booking_num} updated "
                                  "successfully.\n", 'green'))
                    break
        else:
            pass

        # Prompts user to update the amount paid
        print(colored("\nWould you like to update the amount paid? "
                      "Enter Y/N:", 'yellow'))

        # Validates Y/N for updating the amount paid
        while True:
            update_amount_choice = input().upper()
            if update_amount_choice == "Y" or update_amount_choice == "N":
                break
            else:
                print(colored("Invalid input. Please enter Y or N\n", 'red'))

        if update_amount_choice == "Y":
            while True:
                update_amount_paid = input(colored("\nPlease update the "
                                                   "amount paid:\n", 'yellow'))
                try:
                    float_amount = float(update_amount_paid)
                    if not float_amount.is_integer() and \
                            round(float_amount, 2) != float_amount:
                        raise ValueError
                except ValueError:
                    print(colored("Invalid Input: Amount paid must be a "
                                  "whole number\n"
                                  "or a number with 2 decimal places. "
                                  "Please try again.", 'red'))
                else:
                    print(colored(f"\nUpdating B-{booking_num} in "
                                  "progress...\n", 'magenta'))
                    bookings.update_cell(row_index, 5,
                                         "{:.2f}".format(float_amount))
                    print(colored(f"\nBooking B-{booking_num} updated "
                                  "successfully.\n", 'green'))
                    time.sleep(1)
                    break
        else:
            print(colored("\nBooking updates completed, returning to Upate "
                          "Booking Menu...", 'green'))
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else "printf '\033c'")


def delete_booking():
    '''
    Allows user to delete the booking_data in the worksheet.
    Prompts the user for a booking number.
    If booking data is available, data is displayed and prompts
    if they wish to delete the booking.
    If yes, data is deleted from the worksheet.
    If no, the user is returned to the Delete Booking menu.
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()

    # Prompts user to enter a booking number to delete
    print('*' * 23)
    print("*** DELETE BOOKING ***\n")
    print(colored("Enter Booking Number (4-digit number only):\n", 'yellow'))

    # Validates the entry is a 4 digit number only
    while True:
        booking_num = input()
        if len(booking_num) == 4 and booking_num.isdigit():
            booking_num = int(booking_num)
            break
        else:
            print(colored("Invalid entry. Please enter a 4-digit number.\n",
                          'red'))

    print(colored("collecting booking data...\n", 'magenta'))

    rows_containing_booking_num = []
    no_booking_data = True

    # Adds matching booking data to list, or displays a message if there is
    # no data to display
    for row in all_bookings:
        if 'B' + str(booking_num) in row:
            rows_containing_booking_num.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))
    else:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))

        bookings_counter(rows_containing_booking_num)
        revenue_total(rows_containing_booking_num)

    # The following code locates the index of the row in the worksheet
    # that contains the booking number entered by the user, and stores
    # the index in the row_index variable.
    row_index = None
    for i, row in enumerate(all_bookings):
        if row[0] == ('B' + str(booking_num)):
            row_index = i + 1
            break

    # If there is data, the system prompts the user to confirm if they wish to
    # delete the booking before using the delete_rows method from
    # the gspread library.
    # The while loop validates for a correct Y or N input
    if row_index is not None:
        print(colored("Are you sure you want to delete this booking? "
                      "Enter Y/N:", 'yellow'))
        while True:
            delete_choice = input().upper()
            if delete_choice == 'Y' or delete_choice == "N":
                break
            else:
                print(colored("Invalid input.  Please enter Y or N\n", 'red'))

        if delete_choice == "Y":
            print(colored(f"Deleting B-{booking_num} in progress...\n",
                          'magenta'))
            bookings.delete_rows(row_index)
            print(colored(f"Booking B-{booking_num} deleted successfully.\n",
                          'green'))
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
        else:
            print(colored("\nBooking deletions completed, returning to Delete "
                          "Booking Menu...", 'green'))
            time.sleep(1)
            os.system('cls' if os.name == 'nt' else "printf '\033c'")


def view_all_bookings():
    '''
    Displays all bookings in the system along with a count of total bookings
    and the total sum of revenue.

    If there is no booking data available, a message will be displayed to
    inform the user.

    Returns:
        None
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    print('*' * 25)
    print("*** VIEW ALL BOOKINGS ***\n")

    all_bookings = bookings.get_all_values()
    bookings_data = all_bookings[1:]

    if not bookings_data:
        print(
            tabulate(
                bookings_data,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))
    else:
        print(
            tabulate(
                bookings_data,
                headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                         'Amount Paid']))

        bookings_counter(bookings_data)
        revenue_total(bookings_data)


def view_booking_no(booking_num):
    '''
    Displays all bookings in the system for a given Booking Number, along with
    a count of total bookings and sum of revenue for that number.

    Parameters:
    booking_num (int): The 4-digit booking number to be searched for.

    Returns:
    None

    Raises:
    ValueError: If an invalid booking number (not a 4-digit number) is entered.
    '''
    os.system('cls' if os.name == 'nt' else "printf '\033c'")

    all_bookings = bookings.get_all_values()

    # Prompts user to enter a booking number to view
    print('*' * 30)
    print("*** VIEW BY BOOKING NUMBER ***\n")
    print(colored("Enter Booking Number (4-digit number only):\n", 'yellow'))

    # Validates the entry is a 4 digit number only
    while True:
        booking_num = input()
        if len(booking_num) == 4 and booking_num.isdigit():
            booking_num = int(booking_num)
            break
        else:
            print(colored("Invalid entry. Please enter a 4-digit number.\n",
                          'red'))

    print(colored("collecting booking data...\n", 'magenta'))

    rows_containing_booking_num = []
    no_booking_data = True

    # Adds matching booking data to list, or displays a message if there is
    # no data to display
    for row in all_bookings:
        if 'B' + str(booking_num) in row:
            rows_containing_booking_num.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))

    else:
        print(tabulate(
            rows_containing_booking_num,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))

        bookings_counter(rows_containing_booking_num)
        revenue_total(rows_containing_booking_num)


def view_booking_date(booking_date):
    '''
    Displays all bookings in the system by Date, with a count of total
    bookings and a sum of total revenue.

    Parameters:
    booking_date (str): The date to search for bookings in the system. Should
    be in the format 'dd/mm/yyyy'.
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_booking_date = []
    no_booking_data = True

    # Adds matching booking data to list, or displays a message if there is
    # no data to display
    for row in all_bookings:
        if booking_date in row:
            rows_containing_booking_date.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(
            rows_containing_booking_date,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))
    else:
        print(tabulate(
            rows_containing_booking_date,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))

        bookings_counter(rows_containing_booking_date)
        revenue_total(rows_containing_booking_date)


def view_dog_bookings(dogs_name):
    '''
     Displays all bookings in the system for a given dog's name, with a count
     of total bookings and a sum of total revenue. Searches can be performed
     by first name or last name.
    '''
    all_bookings = bookings.get_all_values()

    rows_containing_dog = []
    no_booking_data = True

    # Adds matching booking data to list, or displays a message if there is
    # no data to display
    for row in all_bookings:
        if dogs_name in row:
            rows_containing_dog.append(row)
            no_booking_data = False

    if no_booking_data:
        print(tabulate(
            rows_containing_dog,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))
        print(colored("\nNo booking data to display for this date\n", 'red'))
    else:
        print(tabulate(
            rows_containing_dog,
            headers=['Booking No.', 'Date', 'Dogs Name', 'Family Name',
                     'Amount Paid']))

        bookings_counter(rows_containing_dog)
        revenue_total(rows_containing_dog)


def start():
    '''
    Starts the program - generates a welcome screen to the user.
    Prompts the user to press ENTER
    Calls the choose_main_menu function, which guides the user
    through the options.
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
    Displays Main Menu of options.
    Try statement validates user input for a number between 1 and 5 only

    Returns:
        menu_choice (users menu choice)
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
        print(colored('\nPlease choose a menu option between [1] and [5]:',
                      'yellow'))
        try:
            menu_choice = int(input())
            if menu_choice not in range(1, 6):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1]'
                          ' and [5]\n', 'red'))
    return menu_choice


def update_bkg_menu():
    '''
    Displays Update Booking Menu options.
    Try statement validates user input for
    number between 1 and 4 only.

    Returns:
        update_menu_choice (users menu choice)
    '''

    print('*' * 27)
    print("*** UPDATE BOOKING MENU ***\n")
    print("** OPTIONS:\n")
    print("To update a booking, you will need the Booking Number\n")
    while True:
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search Bookings By Date')
        print("[3] - Or, Search Bookings By Dog's Name")
        print('[4] - Return to Main Menu')
        print(colored('\nPlease choose a menu option between [1] and [4]:',
                      'yellow'))
        try:
            update_menu_choice = int(input())
            if update_menu_choice not in range(1, 5):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1]'
                          ' and [4]\n', 'red'))
    return update_menu_choice


def delete_bkg_menu():
    '''
    Displays Delete Booking Menu options.
    Try statement validates user input for a number between 1 and 4 only.

    Returns:
        delete_menu_choice (users menu choice)
    '''
    print('*' * 27)
    print("*** DELETE BOOKING MENU ***\n")
    print("** OPTIONS:\n")
    print("To delete a booking, you will need the Booking Number\n")
    while True:
        print('[1] - Enter Booking No.')
        print('[2] - Or, Search Bookings By Date')
        print("[3] - Or, Search Bookings By Dog's Name")
        print('[4] - Return to Main Menu')
        print(colored('\nPlease choose a menu option between [1] and [4]:',
                      'yellow'))
        try:
            delete_menu_choice = int(input())
            if delete_menu_choice not in range(1, 5):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1]'
                          ' and [4]\n', 'red'))
    return delete_menu_choice


def view_bkg_menu():
    '''
    Displays View bookings menu of options.
    Try statement validates user input for a number between 1 and 5 only.

    Returns:
        view_menu_choice (users menu choice)
    '''
    print('*' * 26)
    print("*** VIEW BOOKINGS MENU ***\n")
    print("** OPTIONS:\n")
    while True:
        print('[1] - View All Bookings')
        print('[2] - View By Booking No.')
        print('[3] - View By Booking Date')
        print("[4] - View By Booking Name")
        print('[5] - Return to Main Menu')
        print(colored('\nPlease choose a menu option between [1] and [5]:',
                      'yellow'))
        try:
            view_menu_choice = int(input())
            if view_menu_choice not in range(1, 6):
                raise ValueError
            break
        except ValueError:
            print(colored('\nInvalid input.  Please enter a number between [1]'
                          ' and [5]\n', 'red'))
    return view_menu_choice


# SUBMENU CHOICE FUNCTIONS

def choose_update_menu():
    '''
    The update_menu_choice is passed to this if else statement which activates
    one of the relevant functions.

    The user can choose between updating the booking with the booking number,
    or Searching for bookings by date or by dog's name to see the relevant
    number.

    The user is notified of an invalid entry if they do not choose a number
    between 1 and 4.

    Returns:
        None
    '''
    update_menu_choice = update_bkg_menu()
    while True:
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
            dogs_name = get_dogs_name()
            print(colored("collecting booking data...\n", 'magenta'))
            view_dog_bookings(dogs_name)
            choose_update_menu()
            break
        elif update_menu_choice == 4:
            print(colored("Returning to Main Menu\n", 'magenta'))
            time.sleep(1)
            choose_main_menu()
            break
        else:
            print(colored("Invalid choice, please choose between 1 and 4\n",
                          'red'))


def choose_delete_menu():
    '''
    The delete_menu_choice is passed to this if else statement which activates
    one of the relevant functions.

    The user can choose between deleting the booking with the booking number,
    or Searching for bookings by date or by dog's name to see the relevant
    number.

    The user is notified of an invalid entry if they do not choose a number
    between 1 and 4.

    Returns:
        None
    '''
    delete_menu_choice = delete_bkg_menu()
    while True:
        if delete_menu_choice == 1:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            delete_booking()
            choose_delete_menu()
            break
        elif delete_menu_choice == 2:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 22)
            print("*** SEARCH BY DATE ***\n")
            input_date = get_booking_date()
            print(colored("collecting booking data...\n", 'magenta'))
            view_booking_date(input_date)
            choose_delete_menu()
            break
        elif delete_menu_choice == 3:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 24)
            print("*** SEARCH BY DOG'S NAME ***\n")
            dogs_name = get_dogs_name()
            print(colored("collecting booking data...\n", 'magenta'))
            view_dog_bookings(dogs_name)
            choose_delete_menu()
            break
        elif delete_menu_choice == 4:
            print(colored("Returning to Main Menu\n", 'magenta'))
            time.sleep(1)
            choose_main_menu()
        else:
            print(colored("Invalid choice, please choose between 1 and 4\n",
                          'red'))


def choose_view_menu():
    '''
    The view_menu_choice is passed to this if else statement which activates
    one of the relevant functions.

    The user can choose between viewing all the bookings.  Viewing by the
    booking number, or viewing bookings by date or by dog's name.

    The user is notified of an invalid entry if they do not choose a number
    between 1 and 5.

    Returns:
        None
    '''
    view_menu_choice = view_bkg_menu()
    while True:
        if view_menu_choice == 1:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            view_all_bookings()
            choose_view_menu()
            break
        elif view_menu_choice == 2:
            view_booking_no(1000)
            choose_view_menu()
            break
        elif view_menu_choice == 3:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 20)
            print("*** VIEW BY DATE ***\n")
            input_date = get_booking_date()
            print(colored("collecting booking data...\n", 'magenta'))
            view_booking_date(input_date)
            choose_view_menu()
            break
        elif view_menu_choice == 4:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            print('*' * 24)
            print("*** VIEW BY DOG'S NAME ***\n")
            dogs_name = get_dogs_name()
            print(colored("collecting booking data...\n", 'magenta'))
            view_dog_bookings(dogs_name)
            choose_view_menu()
            break
        elif view_menu_choice == 5:
            print(colored("Returning to Main Menu\n", 'magenta'))
            time.sleep(1)
            choose_main_menu()
            break
        else:
            print(colored("Invalid choice, please choose between 1 and 5",
                          'red'))


def choose_main_menu():
    '''
    The main_menu_choice is passed to this if else statement which activates
    one of the relevant functions.

    he user can choose between creating a booking, updating a booking,
    deleting a booking or viewing bookings.

    The user is notified of an invalid entry if they do not choose a number
    between 1 and 5.

    Returns:
        None
    '''
    main_menu_choice = display_main_menu()
    while True:
        if main_menu_choice == 1:
            create_booking()
            choose_main_menu()
            break
        elif main_menu_choice == 2:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            choose_update_menu()
            break
        elif main_menu_choice == 3:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            choose_delete_menu()
            break
        elif main_menu_choice == 4:
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            choose_view_menu()
            break
        elif main_menu_choice == 5:
            print(colored("Ending program...\n", 'magenta'))
            time.sleep(1)
            start()
        else:
            print(colored("Invalid choice, please choose between 1 and 5\n",
                          'red'))
        main_menu_choice = display_main_menu()


# MAIN GUARD

if __name__ == '__main__':
    start()
