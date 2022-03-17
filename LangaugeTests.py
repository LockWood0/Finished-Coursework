#GUI Module
import random
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


class LanguageTest1(object):
    def __init__(self,difficulty):

        self.word_allready_said = []

        self.language_mark = 0
        self.language_total = 5

        self.DIFFICULTY = difficulty

        if self.DIFFICULTY == "HARD": #COnfiguring depending on the test difficulty
            list_of_letters = ["L", "C", "U", "D", "K"]

        elif self.DIFFICULTY == "MEDIUM":
            list_of_letters = ["O", "T", "N", "S"]

        elif self.DIFFICULTY == "EASY":
            list_of_letters = ["E", "A", "R", "I"]

        else:
            list_of_letters = ["O", "T", "N" , "S", "L", "C", "U", "D"]

        self.random_letter  = list_of_letters[random.randint(0,len(list_of_letters)-1)]

        self.time_remaining = 45
        self.words_correct = 0
         #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Language Test")

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
                                    text = "Language Test", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.title_label.place(x = 180, y = 80)

        #Label to explain to user what to do
        self.explanation = customtkinter.CTkLabel(self.root,
                                    text = "Please list as many" + "\n" + "words you can" +"\n" + "begining with " + self.random_letter, 
                                    width=240,
                                    height=100,
                                    corner_radius=12,
                                    text_font= ("Century Gothic", 16),
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
        self.time_remaining_label.after(45000, self.scoreAllocation)

        self.root.mainloop()


    def buttonPress(self):
        entry_var = self.answer_entry.get()
        entry_var = entry_var.upper()
        self.answer_entry.delete(0,"end")

        word_for_re = "^" + self.random_letter
        starts_with = re.search(word_for_re, entry_var) #CHecks to see if it starts with a letter

        if starts_with == None: #Check to see if the word starts with the letter
            showinfo("Window", "Sorry your word does not start with " + self.random_letter)
            return None

        if self.isEnglishWord(entry_var): #Calls teh function to check if it is a word
            if self.allreadySaid(entry_var) is False:
                self.words_correct +=1


    def isEnglishWord(self,word):
        d = enchant.Dict("en_GB")
        isWord = d.check(word)
        return isWord


    def allreadySaid(self,word):
        for i in range(len(self.word_allready_said)):
            if word == self.word_allready_said[i]:
                showinfo("Window", "You have allready said this word")
                return True
        return False


    def scoreAllocation(self):
        """gotta make this have the score before printing"""
        if self.words_correct >13:
            self.language_mark = 5

        elif self.words_correct >10:
            self.language_mark = 4

        elif self.words_correct >7:
            self.language_mark = 3

        elif self.words_correct > 5:
            self.language_mark = 2

        elif self.words_correct >4:
            self.language_mark = 1

        else:
            self.language_mark = 0

        showinfo("Window", "You got this many words: " + str(self.words_correct))
        self.root.destroy()
        print(self.words_correct, self.language_mark)


    def updateTimer(self):
        self.time_remaining_label.configure(text= str(self.time_remaining)) #Updates the time remaning 
        self.time_remaining = int(self.time_remaining)
        self.time_remaining -=1 #Incremting down

        # schedule another timer
        self.time_remaining_label.after(1000, self.updateTimer) #Calls it so it is every second


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
            "Language",
            mark_to_add,
            total_to_add
        )
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()


