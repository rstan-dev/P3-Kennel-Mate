# Project Name - Kennel-Mate

* [Link to Deployed Project](https://kennel-mate.herokuapp.com/)

## Contents(#contents)
​
* [User Experience (UX)](#user-experience)
    *  [Purpose & target audience](#purpose-and-target-audience)
    *  [User Story](#user-story)
    *  [Goals](#goals)

* [Design](#design)
  * [Wireframes](#wireframes)
  * [Color Scheme](#color-scheme)
  * [Typography](#typography)
  * [Imagery](#imagery)
  * [MVP](#mvp)
  * [Planned features](#planned-features)
* [Logic](#logic)
* [Validation](#validation)
* [Technology](#technology)
* [Modules & Libraries](#modules-libraries)
* [Deployment](#deployment)
* [Testing](#testing)
  * [Tests performed](#tests-performed)
  * [User Story Tests](#user-story-tests)
  * [Bugs resolved](#bugs-resolved)
  * [Unresolved bugs](#unresolved-bugs)
  * [Improvements & future developments](#improvements-and-future-developments)
* [Forking & Cloning Instructions](#forking-cloning-instructions)
* [Credits](#credits)
  * [Code](#code)
  * [Content](#content)
  * [Media](#media)
  * [Acknowledgements](#acknowledgements)


## User Experience

   ### Purpose and target audience

   * Kennel-Mate is a simple admin booking system for a doggy daycare business, safely backed up and updated to a google cloud worksheet.
   * The sytem is designed for an employee to capture, update, delete and view booking information, including date, name, family name and amount charged, each with a unique booking number.

   ### User Story

   * The user is presented with an attractive intuitive command-line admin portal, navigating through various menu choices.
   *  The user can choose to create a booking
   *  The user can choose to update a booking
   *  The user can choose to delete a booking
   *  The user can choose to view bookings in the system
   *  The user can find bookings by booking number
   * The user can find bookings by booking date
   * The user can find bookings by dog’s name or family name
   * The user will be presented with a list of relevant bookings at various points in the program, which will also include a useful count of the total bookings in the view and a total of the revenue for those bookings
   *  The user will be notified when the data has been updated after each action
   * The user will be notified if they enter invalid characters, and will prompt them to reenter the information correctly

  ### Goals
   * The program should be clear and easy to use by anyone, with very little training required
   * The information displayed should be relevant to each menu item selected
   * The system should automatically generate a sequential booking number, which can be used as a unique identifier
   * The system should retrieve, add, update or delete the correct information from a Google worksheet via API calls
   * The user should easily be able to exit a menu or return to the previous menu or main menu
   * The user should be given clear instructions, within the program, if any entry or selection is invalid.

## Design

*  The design is based around a terminal application that show cases Python.  The Code Institute mock terminal template was used.

* The initial menu function concept was sketched out using wireframes, a UX background designed in Canva and the logic behind the menus was created using Lucid.


   ### Wireframes  (created in [Balsamiq](https://balsamiq.cloud/))

   Desktop
   * Start Page
   * <img src="assets/images/wire_frame_start.png">

   * Main Menu
   * <img src="assets/images/wire_frame_main.png">

   * Create Booking Menu
   * <img src="assets/images/wire_frame_create.png">

   * Update Booking Menu
   * <img src="assets/images/wire_frame_update.png">

   * Delete Booking Menu
   * <img src="assets/images/wire_frame_delete.png">

    * View Bookings Menu
   * <img src="assets/images/wire_frame_view.png">




   ### Color Scheme (created in [Canva](https://www.canva.com/))

   * Main background
   * The app uses one background image which is a royalty-free template from Canva, to make the site relevant to the dog daycare industry
   * The design was initially conceived in Canva
   * <img src="assets/images/kennel_mate_canva.jpg">
   * In the terminal several font colors were chosen:
   * White for Menu items and headers
   * Yellow for anything requiring user input
   * Magenta for progress updates and displaying dynamic information such as the Bookings Counter and Revenue Total
   * Red for invalid messages
   * Green for success messages


   ### Typography

   *  The main text font is the default font in the command line terminal
   *  The font chosen for the Kennel-Mate logo is a Google Font caled 'Geo" which was the closest font to the Canva font used
   *  Arial was used for the body font on then main page which included the Run Program button

   ### MVP

   * The minimum viable product was to have a working system, that allowed the user to create a new booking, update the information in an existing booking, delete a booking and view bookings by booking number, date, and dog's name.
   * The system also needed to handle invalid entries so as not to crash

   ### Planned features

   * The original plan was to allow the user to navigate through the system using simple, familiar menus which led them to various actions and interactions within the program.
   * The original plan was to include a unique Booking number, which was the basis for finding, upating, and deleting bookings.
   * The date, dog's name and amount charged were identified as the basic requirements.
   * As the project developed it was clear that a seperate family name was also needed in the case where there was more than one dog with the same name.  This was incorporated into the system.
   * The final system deployed all of the planned features .


## Logic

   * The system was conceived using process flow diagrams created in [Lucid](https://lucid.app/) as follows:
   * Main Menu Flow and Create Booking Logic:
   * <img src="assets/images/logic_main_menu_flow.jpeg">
   * Update Booking Menu and Logic:
   * <img src="assets/images/logic_update_booking_menu_flow.jpeg">
   /workspace/P3-Kennel-Mate/assets/images/logic_update_booking _menu_flow.jpeg
   * Delete Booking Menu and Logic:
   * <img src="assets/images/logic_delete_booking_menu_flow.jpeg">
   * View Booking Menu and Logic:
   * <img src="assets/images/logic_view_booking_menu_flow.jpeg">



## Validation
    * Various validation messages were used to ensure that the user was notified correctly of any incorrect input and to ensure the program would not crash.
   * <img src="assets/documents/XXXX">

## Technology

   *

## Modules & Libraries

  *



## Deployment

The following steps were taken to deploy this site:

  *



## Testing
### Tests performed

  *


### User Story Tests




* Features tests

* Menu tests

* API Update tests

* Validation tests



### Bugs resolved:

  *

### Unresolved bugs:

  *

 ### Improvements and future developments:

  *
## Forking & Cloning Instructions



## Credits:

  ### Code

  *


  ### Content

  *

  ### Media

  *

  ### Acknowledgements

  *
