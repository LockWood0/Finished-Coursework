#GUI Module
import queue
import random
import tkinter as tk
from tkinter.messagebox import showinfo
import customtkinter 
from PIL import Image, ImageTk
from numpy import diff

#Databse Module
import pyodbc
 
#Module for adding date of last login
from datetime import date

#Importing a queue
import Queue


class AttentionTest1(object):
    def __init__(self, difficulty):
        self.DIFFICULTY = difficulty

        self.amount_correct = 0
        self.attention_mark = 0
        self.total_attention = 5

        if self.DIFFICULTY == "HARD": #COnfiguring depending on the test difficulty
            possible_numbers = [7,8,13] 

        elif self.DIFFICULTY == "MEDIUM":
            possible_numbers = [8,9,13]

        elif self.DIFFICULTY == "EASY":
            possible_numbers = [11,6,4]

        else:
            possible_numbers = [7,8,9,11,13] 

        random_number  = possible_numbers[random.randint(0,len(possible_numbers)-1)] #Finds a number

        self.time_remaining = 30

        Queue_of_Entries = Queue.Queue()


        #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Registration")

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
                                    text = "Attention Test", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.title_label.place(x = 180, y = 80)

        #Label to explain to user what to do
        self.explanation = customtkinter.CTkLabel(self.root,
                                    text = "Please subract " + str(random_number) + "\n" +"from 100 as many" + "\n" + "times as you can", 
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
                                    text = "Answer (One number at a time)", 
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
                                    command = lambda : self.clickedSubmit(Queue_of_Entries),
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

        #Button binding
        self.root.bind('<Return>',lambda event: self.clickedSubmit(Queue_of_Entries))

        self.time_remaining_label.after(1000, self.updateTimer)

        self.explanation.after(30000,self.finishSubmission, Queue_of_Entries, random_number)
        self.root.mainloop()


    def clickedSubmit(self, Queue_of_Entries):
        entry_var = self.answer_entry.get()
        self.answer_entry.delete(0, 'end')
        Queue_of_Entries.enQueue(entry_var)


    def finishSubmission(self,Queue_of_Entries, random_number):
        correct_number = 100
        while Queue_of_Entries.isEmpty() == False:
            int(correct_number)
            correct_number = correct_number - random_number
            if str(correct_number) == Queue_of_Entries.deQueue():
                self.amount_correct +=1
        
        showinfo("Window", "Well done you had! \n"  +str(self.amount_correct) + " correct subtractions") #Creates alert box
        showinfo("Window", "Well done for completing an additional test!")
        self.scoreAllocation()
        self.root.destroy()


    def scoreAllocation(self):
        if self.amount_correct >5:
            self.attention_mark = 5

        elif self.amount_correct > 4:
            self.attention_mark = 4

        elif self.amount_correct >3:
            self.attention_mark = 3

        elif self.amount_correct >1:
            self.attention_mark = 2

        elif self.amount_correct >0:
            self.attention_mark = 1

        else:
            self.attention_mark = 0
        

    def updateTimer(self):
        self.time_remaining_label.configure(text= str(self.time_remaining)) #Updates the time remaning 
        self.time_remaining = int(self.time_remaining)
        self.time_remaining -=1 #Incremting down

        # schedule another timer
        self.time_remaining_label.after(1000, self.updateTimer) #Calls it so it is every second


    def logTest(self,mark_to_add, total_to_add, user_id):
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
            "Attention",
            mark_to_add,
            total_to_add
        )
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()

