#Imports for tkinter 
import tkinter as tk
from tkinter.messagebox import showinfo
import customtkinter 
from PIL import Image, ImageTk
from tkcalendar import DateEntry

#Module for changing date of last login
from datetime import date

#Databse Module
import pyodbc


class PersonalInfoWindow(object):
    def __init__(self):
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'
        LINK_BLUE = '#CAE4F1'

        self.root = tk.Tk()

        #Defining the size of the window 
        self.root.geometry("500x800")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('TEST2.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)

        #Adding the canvas
        self.canvas = tk.Canvas(self.root,
                                    width = 400, 
                                    height = 650, 
                                    bg =  self.WHITE)
        self.canvas.place(x = 40, y = 60) 

        #Adding the title 
        self.title_label = tk.Label(self.root,
                                    text = "Personal Info", 
                                    font = ("Century Gothic", 24), 
                                    fg = '#210124', 
                                    bg = '#FEFFFE')
        self.title_label.place(x = 140, y = 80)


        #Answer entry label
        self.DoB_label = tk.Label(self.root,
                                    text = "Date of Birth: ", 
                                    font = ("Century Gothic", 12), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.DoB_label.place(x = 75, y = 170)

        #Date of Birth Calander
        self.DoB_cal = DateEntry(self.root, 
            width=12, 
            year=2000, 
            month=1, 
            day=1, 
            background=self.WHITE, 
            disabledbackground=self.PASTEL_BLUE, 
            bordercolor=self.WHITE, 
            headersbackground=self.PASTEL_BLUE, 
            normalbackground= self.PASTEL_BLUE, 
            foreground= self.BLACK, 
            normalforeground= self.BLACK, 
            headersforeground= self.BLACK,
            borderwidth=2,
            font = ("Century Gothic", 14))
        self.DoB_cal.place(x= 75, y =200)

        #Answer entry label
        self.type2_label = tk.Label(self.root,
                                    text = 
                                        "Check the box if the statements apply: ",
                                    font = ("Century Gothic", 12), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.type2_label.place(x = 75, y = 240)

        self.type2_checkbox = customtkinter.CTkCheckBox(self.root, text = "I am diagnosed with Diabetes, Type 2")
        self.type2_checkbox.configure(
            bg_color = self.WHITE,
            fg_color = self.PASTEL_GREEN,
            hover_color = self.PASTEL_BLUE 
        )
        self.type2_checkbox.place(x = 75, y= 280)

        self.heart_checkbox = customtkinter.CTkCheckBox(self.root, text = "I am diagnosed with Heart Disease ")
        self.heart_checkbox.configure(
            bg_color = self.WHITE,
            fg_color = self.PASTEL_GREEN,
            hover_color = self.PASTEL_BLUE 
        )
        self.heart_checkbox.place(x = 75, y= 310)

        #Answer entry label
        self.exercise_label = tk.Label(self.root,
                                    text = 
                                        "I exercise for at least 30 minutes...",
                                    font = ("Century Gothic", 12), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.exercise_label.place(x = 75, y = 350)

                # Tkinter string variable
        # able to store any string value
        self.exercise_variable = tk.IntVar()
        self.exercise_variable.set(1)
        # Dictionary to create multiple buttons


        excercise_amount = [
            ("4+ times a week ", 101),
            ("2-3 times a week", 102),
            ("Once a week or less", 103),
            ("I dont exercise", 104),]
                
        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        inital_y_placement = 370

        for language, val in excercise_amount:
            tk.Radiobutton(self.root, 
                                    text=language,
                                    padx = 20, 
                                    font = ("Century Gothic", 12),
                                    variable=self.exercise_variable, 
                                    bg = self.WHITE,
                                    value=val).place(x= 75, y = inital_y_placement)
            inital_y_placement += 30

        #Answer entry label
        self.concussion_label = tk.Label(self.root,
                                    text = 
                                        "My concussion history: ",
                                    font = ("Century Gothic", 12), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.concussion_label.place(x = 75, y = 500) 

        self.concussion_amount = tk.IntVar()
        self.concussion_amount.set(1)
        # Dictionary to create multiple buttons

        inital_y_placement = 530

        concussion_history = [
            ("No Concussions", 201),
            ("Concussion(s) WITH memory loss", 202),
            ("Concussion(s) WITHOUT memory loss", 203),]

        for language, val in concussion_history:
            tk.Radiobutton(self.root, 
                                    text=language,
                                    padx = 20, 
                                    font = ("Century Gothic", 12),
                                    variable=self.concussion_amount, 
                                    bg = self.WHITE,
                                    value=val).place(x= 75, y = inital_y_placement)
            inital_y_placement += 30

        #Submit button
        self.submit_answer = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Submit",
                                    command = self.getValues,
                                    border_width=5,
                                    corner_radius=10)
        self.submit_answer.place(x =175, y = 625)

        self.root.mainloop()


    def getValues(self):
        valid = False
        
        #Gettign variables from test
        self.exercisise_var = self.exercise_variable.get()
        self.concussions_var = self.concussion_amount.get()
        self.cal_var = self.DoB_cal.get_date()

        #Checkbox
        self.has_diabetes = self.type2_checkbox.get()
        self.has_heart_disease = self.heart_checkbox.get()

        #Checking if above 16
        valid = self.DoBCheck(self.cal_var)
        if valid == False:
            showinfo("Window", "I'm sorry but you are under 16 \nThis test will not be accurate for you")
            return #Stops the function carryign on

        #Pressence check on raiot buttons
        valid = self.raioButtonCheck(self.exercisise_var,self.concussions_var)
        if valid == False:
            showinfo("Window", "Please select on option on the radio buttons")
            return 

        showinfo("Window", "Personal details logged")
        self.root.destroy()
        

    def DoBCheck(self, date_given):
        under_18 = False
        today = date.today()
        if today.year - date_given.year >= 16:
            under_18 = True
            return under_18
        else:
            return under_18


    def raioButtonCheck(self, first_button, second_button):
        pressence = False
        if first_button == 1 or second_button == 1:
            return(pressence)
        pressence = True
        return pressence


    def addDetails(self,ID, cal, exercise, concussion, diabetes, heart_disease,):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
                INSERT INTO HabitsTbl(UserID,DateofBirth,AmountofExerciseDOne,Concussions,Diabetes,HeartDisease) 
                VALUES (?,?,?,?,?,?)""") #This is the SQL Statement that adds a user to the table
        params = (
                ID,
                cal,
                exercise,
                concussion,
                diabetes,
                heart_disease,
                ) #This adds the variables
        cursor.execute(sql,params)
        cursor.commit() #This accutally sends off the command