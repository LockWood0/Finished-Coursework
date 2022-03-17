import tkinter as tk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
import customtkinter

#Database Module
import pyodbc 

#Module for adding date of last login
from datetime import date

#Validation Module
import re

#Hash module
from hashlib import sha256

class RegWindow(object):
    def __init__(self):
        self.new_user_added = False
        self.root = tk.Tk()
        self.root.title("Registration")

        self.canvas = tk.Canvas(self.root, width = 500, height = 500)
        
        #Defines the colours for the GUI
        self.WHITE = "#FEFFFE"
        self.PASTEL_BLUE = "#E5FCF5"
        self.PASTEL_GREEN = '#B3DEC1'
        self.BLACK = '#210124'

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
                                    bg =  '#FEFFFE')
        self.canvas.place(x = 200, y = 60)

        #Adding the labels
        self.title = tk.Label(self.root,
                                    text = "Registration", 
                                    font = ("Century Gothic", 30), 
                                    fg = '#210124', 
                                    bg ='#FEFFFE')
        self.title.place(x = 285, y = 80)

        #Adding username entry with custom tkinter thingy
        self.username_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.username_entry.place(x = 280, y = 160)
        self.username_entry.insert(0, "Username")

        #Adding password entry with custom tkinter thingy
        self.password_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.password_entry.place(x = 280, y = 200)
        self.password_entry.insert(0, "Password")

        #Adding confirm password entry with custom tkinter thingy
        self.confirm_password_entry = customtkinter.CTkEntry(self.root,
                                    width=240,
                                    height = 30,
                                    fg_color= self.PASTEL_BLUE,
                                    text_color= self.BLACK,
                                    bg_color= self.WHITE,
                                    corner_radius=5)
        self.confirm_password_entry.place(x = 280, y = 240)
        self.confirm_password_entry.insert(0, "Confirm Password")

        #confirm_button using custom
        self.confirm_button = customtkinter.CTkButton(self.root,
                                    border_color=self.PASTEL_BLUE,
                                    fg_color= self.WHITE,
                                    bg_color= self.WHITE,
                                    hover_color=self.PASTEL_GREEN,
                                    text="Confirm",
                                    command = self.Register, #Calls register button
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
                                    text="Do you allready \nhave an account?",
                                    command= self.moveToLogin,
                                    border_width=5,
                                    corner_radius=10)
        self.allready_account.place(x =335, y = 360)

        self.root.mainloop()
       

    def clearButtonPressed(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0,'end')


    def moveToLogin(self):
        self.root.destroy()
    

    def Register(self):
        #Getting variables from the tkinter entry boxes
        username_var = self.username_entry.get()
        password_var = self.password_entry.get()
        confirm_password_var = self.confirm_password_entry.get()

        #Calls  basic validation checks (Pressence, Symbol etc)
        is_valid = self.entryValidation(username_var,password_var)
        if is_valid == True:  #If validation checks are valid
            
            #Calls for password verification
            password_same = self.passwordVerification(password_var,confirm_password_var)
            if password_same == True:  #If passwords are the same

                #Calls the function to check if allready in database    
                in_database = self.allReadyInDatabase(username_var)
                if in_database == False: #If the user is not in the database

                    #Calls the function to hash the password
                    hashed_password = self.hashPassword(password_var)
                    #Calls the function to add the user
                    self.addUser(username_var,hashed_password)
                    self.root.destroy()
                else:
                    self.clearButtonPressed()
            else:
               self.clearButtonPressed() 
        else:
            self.clearButtonPressed()


    def entryValidation(self, user_to_check, password_to_check):
        valid = True
        reason = None
        if user_to_check == "" or password_to_check == "": #Pressence check
            #Failed pressence check
            valid = False
            showinfo("Window", "Please remember to write in the test boxes before submitting.") #Creates alert box
        

        has_number = re.findall("[0-9]",password_to_check) #Check to see if password has a number
        if has_number:
            pass
        else:
            #Failed number check
            valid = False
            reason = "characters_in_password"
        

        special_characters = "!@#$%^&*()-+?_=,<>/"
        if any(c in special_characters for c in password_to_check): #Check for if password has symbols
            pass
        else:
            #Failed symbol check
            valid = False
            reason = "characters_in_password"

        has_number = re.findall("[A-Z]",password_to_check) #Check for one capital letter
        if has_number:
            pass
        else:
            #Failed capital check
            valid = False
            reason = "characters_in_password"


        if reason == None: #To see if the reason was to do with type check
            pass
        elif reason == "characters_in_password":
            showinfo("Window", "A password must contain at least: 1 Number, 1 Lowercase letter, 1 Uppercase letter and 1 symbol")


        return valid


    def allReadyInDatabase(self,user_to_query,):
        in_database = False
        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
                SELECT * 
                FROM UsersTbl   
                WHERE Username = ?""") #This is the SQL Statement that adds a user to the table
        params = (user_to_query) #This adds the variables

        record = conn.execute(sql,params) #Does the query
        for row in record:
            x = row

        try: #This try will only work if x could be defined, x can only be define if the for loop could run i.e if there was a record
            if x[0] == None: #Will never go but allows the else condition
                pass
            else: #If a record was found
                in_database = True
                showinfo("Window", "Username allready in use")
                return in_database
        except: #If it could not define x, i.e no record
            return in_database


    def passwordVerification(self, first_password, second_password):
        valid = True
        if first_password == second_password: #If the passwords are the same
            return True
        else:
            showinfo("Window", "Password and Confirm Password must be the same")
            return False


    def hashPassword(self,password_to_hash):
        h = sha256()
        password_to_hash = password_to_hash.encode('UTF-8')
        h.update(password_to_hash)
        hash = h.hexdigest()

        return hash


    def addUser(self,user_entry,password_entry):
        today = date.today()
        user_to_add = user_entry
        password_to_add = password_entry

        conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\ProjectMain\Database.accdb;')
        cursor = conn.cursor()

        sql = ("""
                INSERT INTO UsersTbl(Username,Password, DateofLastLogin) 
                VALUES (?,?,?)""") #This is the SQL Statement that adds a user to the table
        params = (
                user_to_add,
                password_to_add,
                today) #This adds the variables
        conn.execute(sql,params)
        conn.commit() #This accutally sends of the command

        self.new_user_added = True
        