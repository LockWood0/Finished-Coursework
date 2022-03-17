#GUI Module
import queue
import random
import tkinter as tk
from tkinter.messagebox import showinfo
import customtkinter 
from PIL import Image, ImageTk

#Databse Module
import pyodbc
 
#Module for adding date of last login
from datetime import date

#Importing a queue
import Queue

class MemoryTest1(object):
    def __init__(self, difficulty):
        self.DIFFICULTY = difficulty

        if self.DIFFICULTY == "HARD": #COnfiguring depending on the test difficulty
            self.amount_of_words = 7

        elif self.DIFFICULTY == "MEDIUM":
            self.amount_of_words = 5

        elif self.DIFFICULTY == "EASY":
            self.amount_of_words = 3

        else:
            self.amount_of_words = 5

        #Initalising of variables
        self.total_memory_mark = 0
        self.memory_mark = 0

        number_of_words_shown = 0 #Initialisng the number of words shown to user
        list_of_words_shown = [] #Intialising the list of words that will be shown variable
        self.times_submit_pressed = 0
        self.finished = False

        #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Memory Test")

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
        
        #Adding the big title word
        self.title_label = tk.Label(self.root,
                                    text = "Memory Test", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.title_label.place(x = 200, y = 80)

        #Adding the word which chnages and the user has to recite
        self.changing_label = customtkinter.CTkLabel(self.root,
                                    text = "Ready?",
                                    width=240,
                                    height=100,
                                    corner_radius=12,
                                    text_font= ("Century Gothic", 24),
                                    text_color= self.BLACK,
                                    fg_color=self.PASTEL_BLUE,
                                    bg_color = self.WHITE)
        self.changing_label.place(x = 200, y=160)
        
        #Button that begins the test
        self.test_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Start test:",
                                    command = lambda: self.changeValue(number_of_words_shown,list_of_words_shown), #Calls beginTest method
                                    border_width=5,
                                    corner_radius=10)
        self.test_button.place(x =330, y = 280)
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
                                    command = lambda: self.checkAnswer(self.list_of_words_shown),
                                    border_width=5,
                                    corner_radius=10)
        self.submit_answer.place(x =260, y = 380)

        #Button binding
        self.root.bind('<Return>',lambda event: self.checkAnswer(self.list_of_words_shown))

        self.root.mainloop()


    def changeValue(self,num_times_repeated,list_of_words_shown):
        if num_times_repeated < self.amount_of_words: #This is a recursive function so this is to stop it after the 5th time
            with open("ListOfWords.txt") as word_file: #Text file of 1000s of commonly used nouns
                words = word_file.read().split() #Splits the file by line, so each word is a new value in a list
            
            random_word = random.choice(words) #This picks the word randomly from the text file
            
            if list_of_words_shown == []: #Checks to see if any words have been shown to the user so far, stops len(0) error
                pass

            else: #This checks to see if the word chosen is one that has allready been shown, this is statistically very low
                for i in range(len(list_of_words_shown)): #Goes through each word used and compares
                    if random_word == list_of_words_shown[i]:
                        #Immediatlly calls the function again but has not increemnted so it we dont have repeated words
                        self.changing_label.after(0,self.changeValue,num_times_repeated,list_of_words_shown) 

            #Passed check so can show the new word
            self.changing_label.config(text = random_word)
            num_times_repeated +=1 #Running total increases

            random_word = random_word.upper()
            list_of_words_shown.append(random_word) #Adds to list
            
            self.changing_label.after(2000,self.changeValue,num_times_repeated,list_of_words_shown) #Calls the function
        else:
            self.changing_label.config(text = "Recite words") #When five word called
            self.list_of_words_shown = list_of_words_shown


    def checkAnswer(self,correct_words):
        i = self.times_submit_pressed

        answer_var = self.answer_entry.get() #Getting the answer from the entry box
        answer_var = answer_var.upper()
        self.answer_entry.delete(0, 'end') #Clearing the entry box

        if i == self.amount_of_words: #If fucntion has been called more than five times 
            self.finished = True
            showinfo("Window", "Completed! \n" + "Number right: " +str(self.memory_mark) + " out of " + str(self.total_memory_mark)) #Creates alert box
            i =+1
            self.root.destroy()
            return None

        elif i > self.amount_of_words:
            showinfo("Window", "Added")

        if answer_var == correct_words[0]: #This is if they have the word right
            self.memory_mark +=1
            self.total_memory_mark +=1
            correct_words.pop(0) #Popping from the list 
            #Call a function that logs which they have right or if it is finished 
        
        else: #When they don't have the word right
            self.total_memory_mark +=1
            correct_words.pop(0)

        i +=1 #Running total
        self.times_submit_pressed = i


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
            "Memory",
            mark_to_add,
            total_to_add
        )
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()

