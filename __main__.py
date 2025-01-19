# RUN THIS FILE ONLY

from db import Database
from login import Login

#main screen will only instantiate the login window,
#and then the login window will instantiate the voting screen


def main() ->None:
    database = Database()
    login = Login(database)
    if database.connect() == "CONNECTION_SUCCESS":
        print("database connection successfull")
        while login.CONTINUELOGIN:
            login.start_login()

    else:exit(1)
    database.ENDCONNECTION()

if __name__ == "__main__":
    main()