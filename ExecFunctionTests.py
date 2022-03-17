#GUI Module
import tkinter as tk
from tkinter.messagebox import showinfo
import customtkinter 
from PIL import Image, ImageTk

#Databse Module
import pyodbc
 
#Module for adding date of last login
from datetime import date

#Importing a real world dictionary for language test
import enchant
import re



class ExecutiveFunctionTest1(object):
    def __init__(self, difficulty):

        self.animal_allready_said = []
        self.exec_mark = 0
        self.exec_total = 5


        self.DIFFICULTY = difficulty

        if self.DIFFICULTY == "HARD": #COnfiguring depending on the test difficulty
            self.amount_of_words = 30

        elif self.DIFFICULTY == "MEDIUM":
            self.time_remaining = 45

        elif self.DIFFICULTY == "EASY":
            self.time_remaining = 60

        else:
            self.time_remaining = 45

        self.initial_time_remaining = self.time_remaining
        self.initial_time_remaining = self.initial_time_remaining *1000
        self.words_correct = 0

        #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Executive Function Test")

        self.canvas = tk.Canvas(self.root, width = 630, height = 630)
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'

        #Defining the size of the window 
        self.root.geometry("626x626")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('InitalTestImage.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)
 

        self.canvas = tk.Canvas(self.root,
                                    width = 475, 
                                    height = 500, 
                                    bg =  '#FEFFFE')
        self.canvas.place(x = 75, y = 50)

        #Adding title
        self.title_label = tk.Label(self.root,
                                    text = "Executive Function Test", 
                                    font = ("Century Gothic", 28), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.title_label.place(x = 110, y = 80)

        #Label to explain to user what to do
        self.explanation = customtkinter.CTkLabel(self.root,
                                    text = "Please list as many" + "\n" + "animals you can!", 
                                    width=240,
                                    height=100,
                                    corner_radius=12,
                                    text_font= ("Century Gothic", 18),
                                    text_color= self.BLACK,
                                    fg_color=self.PASTEL_BLUE,
                                    bg_color = self.WHITE)
        self.explanation.place(x = 200, y=160)

                #Answer entry label
        self.answer_label = tk.Label(self.root,
                                    text = "Answer (One word at a time)", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.answer_label.place(x = 200, y = 320)

        #Answer entry box
        self.answer_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.answer_entry.place(x = 200, y = 340)

        #Submit button
        self.submit_answer = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Submit",
                                    command = self.buttonPress,
                                    border_width=5,
                                    corner_radius=10)
        self.submit_answer.place(x =260, y = 380)

        #Label to explain time remaining
        self.answer_label = tk.Label(self.root,
                                    text = "Time remaining: ", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.answer_label.place(x = 200, y = 420)

        #Label to explain to user what to do
        self.time_remaining_label = customtkinter.CTkLabel(self.root,
                                    text = str(self.time_remaining),
                                    width=100,
                                    height=50,
                                    corner_radius=12,
                                    text_font= ("Century Gothic", 18),
                                    text_color= self.BLACK,
                                    fg_color=self.PASTEL_BLUE,
                                    bg_color = self.WHITE)
        self.time_remaining_label.place(x = 270, y=440)

        self.root.bind('<Return>',lambda event: self.buttonPress())
        self.time_remaining_label.after(1000, self.updateTimer)
        
        self.time_remaining_label.after(self.initial_time_remaining, self.scoreAllocation)

        self.root.mainloop()


    def buttonPress(self):
        entry_var = self.answer_entry.get()
        entry_var = entry_var.upper()
        self.answer_entry.delete(0,"end")

        if self.isAnAnimal(entry_var): #Calls teh function to check if it is a word
            if self.allreadySaid(entry_var) is False:
                self.animal_allready_said.append(entry_var)
                self.words_correct +=1


    def isAnAnimal(self,word):
        word_to_query = word.upper()
        pwl = enchant.request_pwl_dict("AnimalsTestFile.txt")
        is_an_animal = pwl.check(word_to_query)
        return is_an_animal


    def allreadySaid(self,word):
        for i in range(len(self.animal_allready_said)):
            if word == self.animal_allready_said[i]:
                showinfo("Window", "You have allready said this word")
                return True
        return False


    def updateTimer(self):
        self.time_remaining_label.configure(text= str(self.time_remaining)) #Updates the time remaning 
        self.time_remaining = int(self.time_remaining)
        self.time_remaining -=1 #Incremting down

        # schedule another timer
        self.time_remaining_label.after(1000, self.updateTimer) #Calls it so it is every second


    def scoreAllocation(self):
        if self.words_correct >13:
            self.exec_mark = 5

        if self.words_correct >10:
            self.exec_mark = 4

        elif self.words_correct >7:
            self.exec_mark = 3

        elif self.words_correct > 5:
            self.exec_mark = 2

        elif self.words_correct >3:
            self.exec_mark = 1

        else:
            self.exec_mark = 0

        showinfo("Window", "You got this many words: " + str(self.words_correct))
        self.root.destroy()
        print(self.words_correct, self.exec_mark)


    def logTest(self, mark_to_add, total_to_add, user_id):
        """Function that updates to have the attention marks added"""
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()
        today = date.today()

        sql = ("""
            INSERT INTO SubsquentTestTbl(DateCompleted, UserID, TypeOfTest, Mark, TotalMark)
            VALUES (?,?,?,?,?)
        """)
        params = (
            today,
            user_id,
            "Executive Function",
            mark_to_add,
            total_to_add
        )
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()

