#GUI Module
from glob import glob
from pdb import line_prefix
import queue
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from xmlrpc.client import FastUnmarshaller
import customtkinter 
from PIL import Image, ImageTk

#Databse Module
import pyodbc
 
#Module for adding date of last login
from datetime import date

#Importing a queue
import Queue

#Importing a real world dictionary for language test
import enchant
import re

class MemoryTestInitial(object):
    def __init__(self):

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
        if num_times_repeated <5: #This is a recursive function so this is to stop it after the 5th time
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

        if i == 5: #If fucntion has been called more than five times 
            self.finished = True
            showinfo("Window", "Completed! \n" + "Number right: " +str(self.memory_mark) + " out of " + str(self.total_memory_mark)) #Creates alert box
            i =+1
            self.root.destroy()
            return None

        elif i >5:
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


    def logMark(self, mark_to_add, total_to_add, user_id):
        today = date.today()

        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
                INSERT INTO AssementsTbl(UserID, memeMark, memeTotal, dateCompleted) 
                VALUES (?,?,?,?)""") #This is the SQL Statement that adds the mark
        params = (
                user_id,
                mark_to_add,
                total_to_add,
                today) #This adds the variables
        conn.execute(sql,params)
        conn.commit() #This accutally sends of the command


class AttentionTestInital(object):
    def __init__(self):
        self.amount_correct = 0
        self.attention_mark = 0
        self.total_attention = 5

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


    def logAttentionMarks(self,mark_to_add, total_to_add, user_id):
        """Function that updates to have the attention marks added"""
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
            UPDATE AssementsTbl
            SET AtteMark = ?, AtteTotal = ?
            WHERE UserID= ?
        """)
        params = (mark_to_add, total_to_add, user_id)
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()


class LanguageTestInitial(object):
    def __init__(self):

        self.word_allready_said = []

        self.language_mark = 0
        self.language_total = 5

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


    def logLanguageMarks(self,mark_to_add, total_to_add, user_id):
        """Function that updates to have the language marks added"""
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
            UPDATE AssementsTbl
            SET LangMark = ?, LangTotal = ?
            WHERE UserID= ?
        """)
        params = (mark_to_add, total_to_add, user_id)
        conn.execute(sql,params) #Finds the record with the same user id and updates the langauge based fields
        conn.commit()


class ExecutiveFunctionInital(object):
    def __init__(self):

        self.animal_allready_said = []
        self.exec_mark = 0
        self.exec_total = 5

        self.time_remaining = 45
        self.words_correct = 0

        #This creates the Tkinter window
        self.root = tk.Tk()
        self.root.title("Executive FUnction Test")

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
        
        self.time_remaining_label.after(45000, self.scoreAllocation)

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


    def logExecutiveFunctionMarks(self,mark_to_add, total_to_add, user_id):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
            UPDATE AssementsTbl
            SET ExecMark = ?, ExecTotal = ?
            WHERE UserID= ?
        """)
        params = (mark_to_add, total_to_add, user_id)
        conn.execute(sql,params) #Finds the record with the same user id and updates the attention based fields
        conn.commit()


