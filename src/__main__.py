from db import Database
from login import Login
from customtkinter import CTk

"""
main file just connects the to the database and runs a login instance
all login and voting processes occur through login file itself
so technically running program by running the login file would work just fine (noting that votes would only be saved locally)

in the login file, a single root window is used to display the login as well as the voting screen which helps remove redundancy
closing of the "root" window is not possible , instead the "exit" button of the login screen should be used

storing of votes occurs in both, a central database as well as a local csv file (which can be configured in log.py)

"""


def EOL():print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")

def main() ->None:
    database = Database()
    login = Login(database, CTk())

    if database.connect() == "CONNECTION_SUCCESS":

        print("database connection successfull")
        EOL()
        while login.CONTINUELOGIN:
            login.start_login()

    else:exit(1)
    database.ENDCONNECTION()

if __name__ == "__main__":
    main()