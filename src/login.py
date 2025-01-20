import hashlib
import customtkinter as ctk

from vote import Vote

def EOL():print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
def NODELETE():
    print("~~this window cannot be deleted.~~ ~~\npress the 'exit' button to stop execution normally without errors~~")




class Login:
    def __init__(self, database, root : ctk.CTk):
        self._hashed_password = "bae35f2615069b212f493f0d5f57d2af94b1c2ad9fbee222f4f96b8d4eaa34db"
        self.defaultfont = ("Consolas",24)
        self.CONTINUELOGIN = True

        self.database = database
        #widgets
        self.login_frame = None
        self.password_input = None
        self.root = None
        self.exitbuttonframe = None

        self.root : ctk.CTk = root

    def start_login(self):
        self.root.title("Login window")
        # self.login_window.attributes("-fullscreen", True)

        self.root.grid_rowconfigure(0, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
        self.root.geometry("800x600")

        self.root.protocol("WM_DELETE_WINDOW", func = lambda :NODELETE())

        self.login_frame = ctk.CTkFrame(master = self.root)
        self.login_frame.grid(row=0,column=0,columnspan=2)

        self.exitbuttonframe = ctk.CTkFrame(master = self.login_frame)
        self.exitbuttonframe.grid(row=2,column=1)
        exit_button = ctk.CTkButton(self.exitbuttonframe,
                                    text="Exit",
                                    fg_color = "red",
                                    command = lambda: self.EXIT() )
        exit_button.grid(row=2, column=2, columnspan=2, sticky=ctk.E)

        self.password_input  = ctk.CTkEntry(master = self.login_frame,
                                            font=self.defaultfont,
                                            placeholder_text="Password",
                                            show="*")
        self.password_input.grid(row=0, column=0, columnspan=2, pady=10)

        submit_button  = ctk.CTkButton(master = self.login_frame,
                                       text="submit",
                                       font = self.defaultfont,
                                       command = lambda : self._check_password(self.password_input.get()) )
        submit_button.grid(row=1,column=0,columnspan=2)
        self.START()


    def _check_password(self,user_password : str):
        hash_ = lambda string : hashlib.sha256( string.encode()).hexdigest() # hashes the passed string

        if hash_(user_password) == self._hashed_password: # correct password

            self.password_input.delete(0,ctk.END)
            print("correct pass")
            EOL()
            self._start_vote_screen()

        else:print("Incorrect password"); EOL()


    def _start_vote_screen(self):
        # self._hide_login()
        Vote(self.root, self.database).show_voting_screen()
        # self._show_login()

    def _show_login(self): self.login_frame.grid()
    def _hide_login(self): self.login_frame.grid_remove()


    def START(self):self.root.mainloop()
    def EXIT(self):
        self.CONTINUELOGIN = False
        self.root.destroy()

if __name__ == '__main__':
    Login(database = None,root = ctk.CTk()).start_login()
    #running script like this will throw an error during vote submition
    #cause no database connection is instantiated currently