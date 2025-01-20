import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from electionsoftware.db import Database
from electionsoftware.students import posts
from electionsoftware.log import log


def EOL():print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")


class Vote:
    defaultfont = ("Consolas",24)
    def __init__(self, root : ctk.CTk, database : Database = None):
        #variables
        self.database = database


        self.root : ctk.CTk = root
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)



        # widget initialization
        self.scrollable_vote_frame  = ctk.CTkScrollableFrame(master = self.root) # main scrollable background  frame
        self.scrollable_vote_frame.grid(row=0,
                                        column=0,
                                        sticky=ctk.NSEW)
        # self.masterframe.grid_rowconfigure(0,weight=1)
        # self.masterframe.grid_columnconfigure(0,weight=1)

        self.submit_button = ctk.CTkButton(master = self.scrollable_vote_frame,
                                           text="Submit",
                                           font = self.defaultfont,
                                           command=lambda : self._open_confirm_submit_window)

        self.chosen_candidates : list[ctk.StringVar] = [ctk.StringVar(value="NONE") for _ in posts] # each post is assigned a new string variable

    def show_voting_screen(self):
        self.root.title("Voting screen")

        currow = 0
        for POSTROW,post in enumerate(posts):
            self._set_row_of_candidates(currow,POSTROW,post, posts[post])
            currow += 2

        ctk.CTkButton(self.scrollable_vote_frame, text= "submit", command=lambda:self._open_confirm_submit_window()).grid()
        self.START()

                                    #row to place in | name of the post | candidates in that post
    def _set_row_of_candidates(self,row,POSTROW ,post, candidates_name : list[str] ):
        ctk.CTkLabel(master = self.scrollable_vote_frame,
                     text=post,
                     font= ("Consolas",44),
                     ).grid(row=row,column=0,sticky=ctk.N, pady=15)

        for col,name in enumerate(candidates_name):
            holding_frame = ctk.CTkFrame(master = self.scrollable_vote_frame) #new frame on top of scrollable master frame
            name_label = ctk.CTkLabel(master = holding_frame,
                                      text="",
                                      image = ctk.CTkImage(dark_image = Image.open(os.path.join(os.getcwd(), f"images//{name}.png")),size = (100,100)),
                                      compound = ctk.TOP)
            curRadio = ctk.CTkRadioButton(master = holding_frame,
                                          text=name,
                                          variable = self.chosen_candidates[POSTROW],  #access the current name's corresponding post variable from the choosen_candidates list of stringvars
                                          value = name)

            holding_frame.grid(row=row+1,column=col,pady=25,padx=25, sticky=ctk.N)
            name_label.grid(row=0, column = 0)
            curRadio.grid(row=1,column=0)


        # ctk.CTkLabel(master = .masterframe,text='----------------------------------------------').grid(row=row+1,column=0,columnspan=2)
        #TODO: figure this out  ^ -> a label / horzontal bar to seperate different posts

    def _hide_voting_screen(self):
        self.scrollable_vote_frame.grid_remove()


    def _open_confirm_submit_window(self):
        if messagebox.askokcancel(message = "COnfirm to submit the votes ?"):
            self._submit_votes()
            self._hide_voting_screen()

    def _submit_votes(self):
        for index,candidate in enumerate(self.chosen_candidates):
            candidate_name = candidate.get()
            post = list(posts.keys())[index] # this logic could be improved | gets the post name from the posts sequentially
            if candidate_name=="NONE":continue #ie no one was choosen
            else:
                print(f"{candidate_name} got voted for the post {post}")
                log(candidate_name, post) #log to csv file

                if self.database is not None : #logging to database only occurs when connected to a valid database -> this allows for running through the login.py file but the votes would only be saved locally
                    self.database.increment_vote(post, candidate_name)
                EOL()

        self.root.title("Login Window")

    def START(self):self.root.mainloop()

if __name__ == '__main__':
    Vote(ctk.CTk()).show_voting_screen()
