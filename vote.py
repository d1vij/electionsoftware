import tkinter as tk
from PIL import Image, ImageTk
import os


from dbconnection import Database

"""
main voting window

after clicking the submit button , a confirmation popup is provided
if yes - votes are submitted and processed
else - closes popup and retuns to the voting screen

"""




class VoteScreen:
    def __init__(self, post_ : str, candidates_ : list[str]):
        #database
        self.database = Database()

        self.post = post_
        self.candidates = candidates_

        #root initialization
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title(self.post)

        #variable defn
        self.currvote = tk.StringVar()
        self.currvote.set("NONE")
        #functions
        self.main()


    def main(self):
        #current post voting label
        heading = tk.Label(self.root,text=f"Currently voting for the post {self.post}")
        heading.config(anchor="center")
        heading.grid()


        for candidate in self.candidates:
            candidate_radio = tk.Radiobutton(self.root,
                                             variable = self.currvote,
                                             value = candidate, # the variable value is the name of the candidate itself | no need to map to elif statements in db management
                                             text = candidate,
                                             image=self.instantiate_image(name = candidate),
                                             compound="right")
            candidate_radio.config(anchor=tk.W,
                                   font=("Monospace",50))

            candidate_radio.grid()


        submit_button = tk.Button(self.root, text = "submit", command = self.confirm_window)
        submit_button.grid()


        self.start()

    def confirm_window(self):
        #TODO: make sure that the main vote screen closes onces after the vote is confirmed

        cwindow = tk.Toplevel(self.root)
        text= tk.Label(cwindow)

        if self.currvote.get() != "NONE":
            text.config(text="Do you want to submit the votes?")
            text.grid()
            yes_button = tk.Button(cwindow,text="yes",
                                   command=self.submit_votes,
                                   anchor="center",
                                   font = ("arial",20))

            no_button = tk.Button(cwindow,
                                  text="no",
                                  command=cwindow.destroy, #destroys confirm window
                                  anchor = "center",
                                  font = ("arial", 20))
            yes_button.grid()
            no_button.grid()

        else:
            cwindow.config(background="red")
            text.config(text="You have to choose atleast one candidate")
            text.grid()
            ok_button = tk.Button(cwindow,
                                  text = "OK!",
                                  command=cwindow.destroy, #destroys confirm window
                                  anchor = "center",
                                  font = ("arial", 20))
            ok_button.grid()
        # cwindow.destroy()


    def submit_votes(self):
        name = self.currvote.get()
        self.database.update_database(name)

    def instantiate_image(self, name : str) -> ImageTk:
        #TODO: work on images for the radio buttons
        try:
            # image_path = os.path.join(f"{name}.png")
            image = Image.open(os.getcwd()+"snoop.png").resize((100,80))
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"No image exists with name {name} in directory ")

    def start(self):self.root.mainloop()



if __name__ == "__main__":
    candidates = ["divij","shinchan","snoop"]
    VoteScreen("Test",candidates)

    
    

