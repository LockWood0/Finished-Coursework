#GUI Module
import tkinter as tk
from tkinter.messagebox import showinfo
from turtle import update
from PIL import Image, ImageTk
import customtkinter 

#Databse Module
import pyodbc

#Hash Module
from hashlib import sha256

#For going to registration screen
import Registration

#For forgot my password string maker
import random
import string

#Module for changing date of last login
from datetime import date

from main import main


class LogInWindow(object):
    def __init__(self):
        #Gets user ID
        self.user_id= ""

        self.root = tk.Tk()
        self.root.title("Login")

        self.canvas = tk.Canvas(self.root, width = 500, height = 500)
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'
        self.LINK_BLUE = '#CAE4F1'

        #Defining the size of the window 
        self.root.geometry("800x500")
        self.root.resizable(False,False)

        #This makes the background picture
        self.Image = Image.open('backgroundPic.jpg')
        self.background_image = ImageTk.PhotoImage(self.Image)
        self.background_image_label = tk.Label(image= self.background_image)

        self.background_image_label.image = self.Image
        self.background_image_label.place(x=0, y=0)
 
        #Adding the canvas
        self.canvas = tk.Canvas(self.root,
                                    width = 400, 
                                    height = 400, 
                                    bg =  self.WHITE)
        self.canvas.place(x = 200, y = 60)

        #Adding the labels
        self.username_label = tk.Label(self.root,
                                    text = "Login", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.username_label.place(x = 345, y = 80)

        self.title = tk.Label(self.root,
                                    text = "Username:", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.title.place(x = 280, y = 160)

        #Adding username entry with custom tkinter thingy
        self.username_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.username_entry.place(x = 280, y = 180)

        self.password_label = tk.Label(self.root,
                                    text = "Password:", 
                                    font = ("Century Gothic", 10), 
                                    fg = '#210124', 
                                    bg = self.WHITE)
        self.password_label.place(x = 280, y = 220)

        self.forgot_password_label = tk.Label(self.root,
                                    text = "Forgot password?", 
                                    font = ("Century Gothic", 8), 
                                    cursor="hand2",
                                    fg = "blue", 
                                    bg = self.WHITE)
        self.forgot_password_label.place(x = 420, y = 220)
        self.forgot_password_label.bind("<Button-1>",lambda e: self.forgotPassword()) #Calls function on click

        #Adding password entry with custom tkinter thingy
        self.password_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.password_entry.place(x = 280, y = 240)


        #confirm_button using custom
        self.confirm_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Confirm",
                                    command = self.Login, #Calls login function
                                    border_width=5,
                                    corner_radius=10)
        self.confirm_button.place(x =340, y = 280)

        #CLear button
        self.clear_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Clear",
                                    command= self.clearButtonPressed,
                                    border_width=5,
                                    corner_radius=10)
        self.clear_button.place(x =340, y = 320)

        self.allready_account = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text_font= ("Century Gothic", 8),
                                    text="Have you not \nregistered before?",
                                    command= self.moveToRegistration,
                                    border_width=5,
                                    corner_radius=10)
        self.allready_account.place(x =335, y = 360)

        self.root.mainloop()
       

    def clearButtonPressed(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')


    def moveToRegistration(self):
        self.destroy() #This and the other move to Login functions create error for some reason
        main.main()


    def Login(self):
        username_var = self.username_entry.get()
        password_var = self.password_entry.get()
        #Check if username is there
        user_exists = self.ifUsernameExists(username_var)
        if user_exists == False:
            showinfo("Window", "Username cannot be found, \nPlease make an account") #Creates alert box
            self.clearButtonPressed()
            return None 

        #Check if password the same
        password_same = self.checkPassword(username_var, password_var)
        if password_same == False:
            showinfo("Window", "Password incorrect") 
            self.clearButtonPressed()
            return None 
        showinfo("Window", "Login Sucessful") 
        #Update date of last login
        self.updateLastLogin(username_var)
        self.grabUserID(username_var)
        self.root.destroy()
        return None


    def ifUsernameExists(self,item_to_query):
        user_exists = False
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
                SELECT * 
                FROM UsersTbl   
                WHERE Username = ?""") #This is the SQL Statement that adds a user to the table
        params = (item_to_query) #This adds the variables

        record = conn.execute(sql,params) #Does the query
        for row in record:
            x = row

        try: #This try will only work if x could be defined, x can only be define if the for loop could run i.e if there was a record
            if x[0] == None: #Will never go but allows the else condition
                pass
            else: #If a record was found
                user_exists = True
                return user_exists
        except: #If it could not define x, i.e no record
            return user_exists


    def checkPassword(self,username_given, password_given):
        password_correct = False
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
            SELECT UsersTbl.Password
            FROM UsersTbl
            WHERE (((UsersTbl.Username)=?));
        """) #SQL For returning the password of the user
        params = (username_given)
        database_hash = conn.execute(sql,params) #Finds the password of user

        for row in database_hash: #Getting the password to compare
            x = row

        hashed_password_given = self.hashPassword(password_given) #Hashing teh plain text given password to compare

        if hashed_password_given == x[0]: #If the databse password and given hashed password are the same
            password_correct = True
            return password_correct

        else:
            return password_correct


    def hashPassword(self,password_to_hash):
        h = sha256()
        password_to_hash = password_to_hash.encode('UTF-8')
        h.update(password_to_hash)
        hash = h.hexdigest()

        return hash


    def forgotPassword(self):
        self.root.destroy()
        import ForgotPassword
        self.grabUserID(username_given= self.username_entry.get())
        id = self.user_id
        ForgotPassword.ForgotPassowrdWindow(id)
        LOG_IN_WINDOW = LogInWindow()


    def updateLastLogin(self,username_given):
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        today = date.today()

        sql = ("""
            UPDATE UsersTbl
            SET DateofLastLogin = ? 
            WHERE Username= ?
        """)
        params = (today, username_given)
        conn.execute(sql,params) #Finds the password of user
        conn.commit()


    def grabUserID(self, username_given):
        self.username = username_given
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()


        sql = ("""
            SELECT UserID
            FROM UsersTbl
            WHERE Username= ?
        """)
        params = (username_given)
        databse_ID = conn.execute(sql,params) #Finds the password of user

        for row in databse_ID: #Getting the password to compare
            x = row

        self.user_id = x[0]
