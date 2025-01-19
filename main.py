#main file

from db import Database
from login import Login

#main screen will only instantiate the login window,
#and then the login window will instantiate the voting screen


def main() ->None:
    database = Database()
    login = Login(database)
    if database.connect() == "CONNECTION_SUCCESS":
        while login.CONTINUELOGIN:
            login.start_login()
    else:exit(1)


if __name__ == "__main__":
    main()