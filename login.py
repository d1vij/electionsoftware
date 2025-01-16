import tkinter as tk
import hashlib
from time import sleep



"""
initial login window - pops up when app runs
if password is correct , instantiates the main voting window
else stays on login window
"""



class Login:
    def __init__(self):
        self._hashed_password = "bae35f2615069b212f493f0d5f57d2af94b1c2ad9fbee222f4f96b8d4eaa34db"
        self.login_window = tk.Tk()
        self.login_window.geometry("800x600")
        self.status = tk.Label(self.login_window)

    def main(self):
        #delete using root.destroy
        self.login_window.title("Login")

        textlabel = tk.Label(self.login_window, text="Input password")
        textlabel.pack()
        #password entry
        entry = tk.Entry(self.login_window)
        entry.pack()
        #submit
        submit_button = tk.Button(self.login_window, text="submit", command=lambda:self.checkpassword(entry.get()))
        submit_button.pack()
        self.start()

    def checkpassword(self, password):
        #hashing
        hashobj = hashlib.sha256()
        hashobj.update(password.encode())
        hash = hashobj.hexdigest()

        if hash == self._hashed_password:
            self.update_success_label(1)
        else:
            self.update_success_label(0)


    def update_success_label(self,condition : int = 0):
        #outputs if entered password is correct or not
        match condition:
            case 1: #correct password
                self.status.config(text="correct password")
                self.status.pack()

            case 0:
                self.status.config(text="incorrect password")
                self.status.pack()
            case _:
                self.status.config(text="ERROR OCCURED!")
                self.status.pack()

    def start(self):self.login_window.mainloop()


