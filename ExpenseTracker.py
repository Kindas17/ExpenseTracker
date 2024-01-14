#####################################################################
                                                  # Expense Tracker #
                                                  ###################

import os

class ExpenseTracker:

    # Keeps track of the project version to print in every view
    OBJ_VERSION = {
        'M': 1, # Major
        'm': 0, # Minor
    }

    # Application header shown in every view
    HEADER = [
        70 * '*',
        'Expense Tracker {}.{}'.format(OBJ_VERSION['M'], 
                                       OBJ_VERSION['m']),
        70 * '*' + '\n',
    ]

    # Fields that are shown in the main menu view with corresponding
    # numbers for user choice
    MENU_FIELDS = {
        'Dashboard':           1,
        'Import Transactions': 2,
        'Options':             3,
        'Exit':                4,
    }


    def __init__(self) -> None:

        # Initialize the user choice to a null value
        self.userChoice = 0



    def mainLoop(self) -> None:
        '''
        Application main loop: this is the entry point
        '''

        while (self.userChoice != self.MENU_FIELDS['Exit']):
            self.userChoice = self.__showMenu()
            self.mapFun(self.userChoice)



    def mapFun(self, choice) -> None:

        if (choice == self.MENU_FIELDS['Dashboard']):
            self.Fun_Dashboard()

        elif (choice == self.MENU_FIELDS['Options']):
            self.Fun_Options()

        elif (choice == self.MENU_FIELDS['Exit']):
            pass

        elif (choice == 0):
            pass

        else:
            self.Fun_Unknown()


    
    def Fun_Dashboard(self) -> None:
        print('Not available')
        input('Press a key...')

    def Fun_Options(self) -> None:
        print('Not available')
        input('Press a key...')

    def Fun_Unknown(self) -> None:
        print('Unknown request')
        input('Press a key...')



    def __showMenu(self) -> int:
        '''
        Clears the terminal window and shows the application menu.
        It asks the user for something to do and sends the request 
        to other components
        '''

        os.system('clear')

        self.__showHeader()

        for field in self.MENU_FIELDS.keys():
            print(f'{self.MENU_FIELDS[field]} - {field}')

        print('')

        userChoice = input('Choice: ')
        return int(userChoice) if userChoice.isdigit() else 0
    


    def __showHeader(self):
        for s in self.HEADER:
            print(s)



# The End
