import hashlib
import customtkinter as ctk

from electionsoftware.vote import Vote

class Login:
    def __init__(self, database):
        self._hashed_password = "bae35f2615069b212f493f0d5f57d2af94b1c2ad9fbee222f4f96b8d4eaa34db"
        self.defaultfont = ("Consolas",24)
        self.CONTINUELOGIN = True

        self.database = database
        #widgets
        self.password_input = None
        self.login_window = None


    def start_login(self):
        self.login_window = ctk.CTk() #root
        self.login_window.title("Login window")
        # self.login_window.attributes("-fullscreen", True)

        self.login_window.grid_rowconfigure(0,weight = 1)
        self.login_window.grid_columnconfigure(0,weight = 1)
        self.login_window.geometry("800x600")

        login_window_frame = ctk.CTkFrame(master = self.login_window)
        login_window_frame.grid(row=0,column=0,columnspan=2)

        # exitbuttonframe = ctk.CTkFrame(master = self.login_window)
        # exitbuttonframe.grid(row=1,column=1)
        # exit_button = ctk.CTkButton(exitbuttonframe,text="Exit",fg_color = "red", command = lambda: self.login_window.destroy())
        # exit_button.grid(row=2,column=2,columnspan=2,sticky=ctk.E)

        self.password_input  = ctk.CTkEntry(master = login_window_frame,
                                       font=self.defaultfont,
                                       placeholder_text="Password",
                                       show="*")
        self.password_input.grid(row=0, column=0, columnspan=2, pady=10)

        submit_button  = ctk.CTkButton(master = login_window_frame,
                                       text="submit",
                                       font = self.defaultfont,
                                       command = lambda : self._check_password(self.password_input.get()) )
        submit_button.grid(row=1,column=0,columnspan=2)

        self.START()


    def _check_password(self,user_password : str):
        hashobj = hashlib.sha256()
        hashobj.update(user_password.encode())
        hashed_user_password = hashobj.hexdigest()

        if hashed_user_password == self._hashed_password: # correct password
            self.password_input.delete(0,ctk.END)
            print("correct passs")
            # self.login_window.destroy()
            Vote(self.login_window, self.database).main()


        else:print("Incorrect passowrd")

    def START(self):self.login_window.mainloop()

if __name__ == '__main__':
    Login().start_login()