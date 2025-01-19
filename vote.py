import os
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

from electionsoftware.db import Database
from electionsoftware.students import posts

class Vote:
    defaultfont = ("Consolas",24)
    def __init__(self, root : ctk.CTk, database : Database):
        #variables
        #root
        self.root = root
        self.root.title("Voting screen")
        self.root.grid_rowconfigure(0,weight=1)
        self.root.grid_columnconfigure(0,weight=1)  # self.root.attributes('-fullscreen',True) #start fullscreen
        # self.root.geometry("1920x1080")

        # widget initialization
        self.masterframe  = ctk.CTkScrollableFrame(master = self.root) # main scrollable background  frame
        # self.masterframe.grid_rowconfigure(0,weight=1)
        # self.masterframe.grid_columnconfigure(0,weight=1)

        self.submit_button = ctk.CTkButton(master = self.masterframe,
                                           text="Submit",
                                           font = self.defaultfont,
                                           command=lambda : self._open_confirm_submit_window)

        self.choosen_candidates : list[ctk.StringVar] = [
            ctk.StringVar(value="NONE") for _ in posts # each post is assigned a new string variable
        ]


    def main(self):
        self.masterframe.grid(row=0,
                              column=0,
                              sticky=ctk.NSEW)
        currow = 0
        for POSTROW,post in enumerate(posts):
            self._set_row_of_candidates(currow,POSTROW,post, posts[post])
            currow += 2

        ctk.CTkButton(self.masterframe,text="submit",command=lambda:self._open_confirm_submit_window()).grid()
        self.START()

                                    #row to place in | name of the post | candidates in that post
    def _set_row_of_candidates(self,row,POSTROW ,post, candidates_name : list[str] ):
        ctk.CTkLabel(master = self.masterframe,
                     text=post,
                     font= ("Consolas",44),
                     ).grid(row=row,column=0,sticky=ctk.N, pady=15)

        for col,name in enumerate(candidates_name):
            holding_frame = ctk.CTkFrame(master = self.masterframe) #new frame on top of scrollable master frame
            name_label = ctk.CTkLabel(master = holding_frame,
                                      text="",
                                      image = ctk.CTkImage(dark_image = Image.open(os.path.join(os.getcwd(), f"images//{name}.png")),size = (100,100)),
                                      compound = ctk.TOP)
            curRadio = ctk.CTkRadioButton(master = holding_frame,
                                          text=name,
                                          variable = self.choosen_candidates[POSTROW] , #access the current name's corresponding post variable from the choosen_candidates list of strinvars
                                          value = name)

            holding_frame.grid(row=row+1,column=col,pady=25,padx=25, sticky=ctk.N)
            name_label.grid(row=0, column = 0)
            curRadio.grid(row=1,column=0)


        # ctk.CTkLabel(master = self.masterframe,text='----------------------------------------------').grid(row=row+1,column=0,columnspan=2)
        #TODO: figure this out  ^




    def _open_confirm_submit_window(self):
        if messagebox.askokcancel(message = "COnfirm to submit the votes ?"): self._submit_votes()
    def _submit_votes(self):
        for index,candidate in enumerate(self.choosen_candidates):
            print(f"{candidate.get()} was voted for the post {list(posts.keys())[index]}")

    def START(self):self.root.mainloop()

if __name__ == '__main__':
    Vote(ctk.CTk()).main()
    # for post in posts:
    #     print(post)
    #     for student in posts[post]:
    #         print(student)
    #     print()